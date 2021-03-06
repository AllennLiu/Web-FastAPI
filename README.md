Web-FastAPI
==================

## Version
`Rev: 1.0.0`

[![Release Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/AllennLiu/0bf7d0bf3675b35eaa46fffc60b4ade0/raw/Web-FastAPI-release.json)](https://github.com/AllennLiu/Web-FastAPI/releases) [![Package Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/AllennLiu/ab6dc65e1bc6049b57a18f32124f2ce7/raw/Web-FastAPI-package.json)](https://github.com/AllennLiu/Web-FastAPI/pkgs/container/web-fastapi)

---

## Requirement Version
![Python Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/AllennLiu/ff710dd6f378c7d82792f9429f65ab31/raw/Python%2520Version&logoColor=violet) ![Kubernetes Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/AllennLiu/afa8c412f07d7457a79fc0697b816c67/raw/3c75f9fbb513a8ded6d37a83d600422667a6644f/Kubernetes%2520Badge)

---

## Status

[![Pipeline Status](https://github.com/AllennLiu/Web-FastAPI/actions/workflows/docker-image.yml/badge.svg)](https://github.com/AllennLiu/Web-FastAPI/actions/workflows/docker-image.yml) ![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/AllennLiu/cdc11bececff228f66cebd39b8b588dc/raw/Web-FastAPI__heads_main.json&logoColor=9cf)

---

## Description

Using **`FastAPI` web framework** with _Python_ to build API services, this is **more faster** than `Flask`.

---

## Script Process

  1. **Staging** service `start.sh` will be run with **`ansible-playbook`** in CI pipeline job.

      ```bash
      $ vim hosts
      $ vim ./variables/common.yaml
      $ ansible-playbook -i hosts deploy-staging.yaml
      ```

  2. **Production** service `start.sh` will be run with **_Docker_ `kubectl` tool image** in CI pipeline job.

      ```bash
      $ docker run --rm --name tool-kubectl-deploymen \
          ghcr.io/allennliu/tool-kubectl-deployment:1.0.4 \
          bash start.sh --k8s-run -v 1.0.0 -p Web-FastAPI -n web-fastapi \
                        -i ghcr.io/allennliu/web-fastapi \
                        -MP 8787 -M1 /mnt/storage -M2 /mnt/tmp
      ```

---

## When to use ?

??????????????? **Python** ?????? **Web ??????**??????????????????????????????????????????????????????????????????????????????

---

## Usage

  - **????????????????????????????????????????????????????????????????????????????????????????????? `VPN` ?????????**

  - **Production ??????**

    - **FastAPI Home - [http://web-fastapi.cloudnative.ies.inventec](http://web-fastapi.cloudnative.ies.inventec)**

  - **Staging ??????**

    - **FastAPI Home - [http://10.99.104.251:8787/login](http://10.99.104.251:8787/login)**

  - More API usage please refer to following url:

    - **FastAPI Docs  - [http://web-fastapi.cloudnative.ies.inventec/docs](http://web-fastapi.cloudnative.ies.inventec/docs)**

    - **FastAPI Redoc - [http://web-fastapi.cloudnative.ies.inventec/redoc](http://web-fastapi.cloudnative.ies.inventec/redoc)**


---

## Reports

  - Run as below command in production for `container's log`:

    ```bash
    $ docker logs --tail 50 --follow --timestamps web-fastapi
    ```

  - View logs via tool `kubectl`:

    ```bash
    $ kubectl logs -n kube-ops $(kubectl get pods -n kube-ops | awk '{print $2}' | grep -E '^web-fastapi\-[a-zA-Z0-9]+\-[a-zA-Z0-9]+$')
    ```

---

## Attention

  - Build image.

    ```bash
    $ docker build --no-cache -t ghcr.io/allennliu/web-fastapi:${VERSION} .
    ```

  - Login _Github_ registry and **Push** image.

    ```bash
    $ echo $ACCESS_TOKEN | docker login ghcr.io -u AllennLiu --password-stdin
    $ docker push ghcr.io/allennliu/web-fastapi:${VERSION}
    ```

  - Run image on **Docker** container.

    ```bash
    docker run -tid \
           --add-host ipt-gitlab.ies.inventec:10.99.104.242 \
           --add-host mailrelay-b.ies.inventec:10.99.2.61 \
           -p 8787:8000 \
           -p 8788:22 \
           --volume /etc/localtime:/etc/localtime:ro \
           --privileged=true \
           --restart=always \
           --name web-fastapi \
           ghcr.io/allennliu/web-fastapi:${VERSION} \
           uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

  - Create **Docker Registry Secret** before deploy pod if it `not exists` in **Kubernetes**.

    ```bash
    $ kubectl create secret docker-registry github-registry \
              --docker-server=ghcr.io \
              --docker-username=AllennLiu \
              --docker-password=$GITHUB_ACCESS_TOKEN \
              --docker-email=seven6306@icloud.com \
              -n kube-ops
    ```

  - Run web service on **Kubernetes** cluster.

    ```bash
    $ kubectl apply -f deployments/ --record
    ```

  - Run cronjobs on **Kubernetes** cluster, currently no any cronjobs in project.

    ```bash
    $ kubectl apply -f crond/cronjobs.yml
    ```

---

## Associates

  - **Tester**
    - Liu.AllenJH

  - **Developer**
    - Liu.AllenJH

---

## Validation

<details>
<summary>????????????/???????????????????????????</summary>
<ul>
  <li>None.</li>
</ul>
</details>

  - **Latest script has been validated by Liu.AllenJH on K8S-Cluster at 2021-08-05.**

---

## Reference

  - FastAPI - [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
  - fastapi-mail - [https://sabuhish.github.io/fastapi-mail](https://sabuhish.github.io/fastapi-mail)
  - fastapi-login - [https://fastapi-login.readthedocs.io/reference](https://fastapi-login.readthedocs.io/reference)
