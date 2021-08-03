#!/bin/bash

script=`basename $0`
log_name=`basename $script .sh`.log
kubernetes_run_mode=False
kubernetes_clr_mode=False

function imageClear
{
    project_name=`echo $CI_PROJECT_NAME | awk '{print tolower($0)}'`
    if [ `docker images | grep -ciE "\/${project_name}"` -ne 0 ]; then
        image_ids="`docker images | grep -E "\/${project_name}" | awk '{print $3}'`"
        docker rmi -f $image_ids
    fi
    docker images | grep -E "\/${project_name}"
}

function dockerStop
{
    for opt in kill stop rm
    do
        docker $opt $CONTAINER_NAME 2> /dev/null
    done
}

function dockerRun
{
    docker run -tid \
           --add-host ipt-gitlab.ies.inventec:10.99.104.242 \
           --add-host mailrelay-b.ies.inventec:10.99.2.61 \
           -p ${CONTAINER_PORT}:8000 \
           -p $(( CONTAINER_PORT + 1)):22 \
           --volume /mnt:/mnt:ro \
           --volume ${MOUNT_PATH_1}:/usr/src/storage \
           --volume ${MOUNT_PATH_2}:/usr/src/tmp \
           --volume /etc/localtime:/etc/localtime:ro \
           --privileged=true \
           --restart=always \
           --name $CONTAINER_NAME $CI_REGISTRY_IMAGE:$VERSION \
           bash service.sh --stag
    sleep 10
    docker ps
    if [ `docker ps | grep -c "${CONTAINER_NAME}$"` -eq 0 ]; then
        echo "docker run container $CONTAINER_NAME FAIL."
        exit 1
    fi
    echo "docker run container $CONTAINER_NAME PASS."
}

function kuberneteStop
{
    kubectl delete -f deployments/
    sleep 30
}

function kuberneteRun
{
    # configure deployment settings
    sed -i "s,<MOUNT_PORT>,${MOUNT_PORT},g"         deployments/*-deploy.yml
    sed -i "s,<MOUNT_PATH_1>,${MOUNT_PATH_1},g"     deployments/*-deploy.yml
    sed -i "s,<MOUNT_PATH_2>,${MOUNT_PATH_2},g"     deployments/*-deploy.yml
    sed -i "s,<CONTAINER_NAME>,${CONTAINER_NAME},g" deployments/*-deploy.yml
    sed -i "s,<CI_REGISTRY_IMAGE>,${CI_REGISTRY_IMAGE}:${VERSION},g" deployments/*-deploy.yml

    more << EOF
    Show YAML Configuration:
    ===========================================================================
    $(cat deployments/*-deploy.yml)
    ===========================================================================
EOF

    kubectl apply -f deployments/ --record
    sleep 60
    more << EOF
    ===========================================================================
    Show Deployment Pods Status:
    ===========================================================================
    $(kubectl get pods -n kube-ops | grep -v "\-cron" | grep $CONTAINER_NAME)
    ===========================================================================
EOF
}

function main
{
    if [ "$kubernetes_clr_mode" == "True" ]; then
        kuberneteStop
        imageClear
    elif [ "$kubernetes_run_mode" == "True" ]; then
        kuberneteStop
        imageClear
        kuberneteRun
    else
        dockerStop
        imageClear
        dockerRun
    fi
}

# parse arguments
if [ "$#" -eq 0 ]; then
    echo "Invalid arguments, try '-h/--help' for more information."
    exit 1
fi
while [ "$1" != "" ]
do
    case $1 in
        -v)
            shift
            VERSION=$1
            ;;
        -p)
            shift
            CI_PROJECT_NAME=$1
            ;;
        -n)
            shift
            CONTAINER_NAME=$1
            ;;
        -i)
            shift
            CI_REGISTRY_IMAGE=$1
            ;;
        -r)
            shift
            CI_COMMIT_REF_NAME=$1
            ;;
        -H)
            shift
            CONTAINER_HOST=$1
            ;;
        -P)
            shift
            CONTAINER_PORT=$1
            ;;
        -MP)
            shift
            MOUNT_PORT=$1
            ;;
        -M1)
            shift
            MOUNT_PATH_1=$1
            ;;
        -M2)
            shift
            MOUNT_PATH_2=$1
            ;;
        --k8s-run)
            kubernetes_run_mode=True
            ;;
        --k8s-clr)
            kubernetes_clr_mode=True
            ;;
        * ) echo "Invalid arguments, try '-h/--help' for more information."
            exit 1
            ;;
    esac
    shift
done

main | tee $log_name
