#!/bin/bash
BLUE="\033[1;34m"
YELLOW="\033[0;33m"
NC1="\033[0m"

function chkReqs
{
    if [ "$(command -v docker 2> /dev/null)" == "" ]; then
        echo "'docker' command not found."
        exit 1
    fi
}

function main
{
    chkReqs
    echo -e "${BLUE}
===========================================================================${NC1}
${YELLOW}List docker exited containers:${NC1}
${BLUE}===========================================================================${NC1}"

    docker ps -a -f "status=exited"
    if [ $(docker ps -a -q -f "status=exited" | wc -l) -eq 0 ]; then
        echo "None"
    fi
    echo -e "${BLUE}
===========================================================================${NC1}
${YELLOW}List docker untagged/dangling images:${NC1}
${BLUE}===========================================================================${NC1}"

    docker images -f "dangling=true"
    if [ $(docker images -f "dangling=true" -q | wc -l) -eq 0 ]; then
        echo -e "${YELLOW}None${NC1}"
    fi
    echo -e "${BLUE}===========================================================================${NC1}"
    if [ $(docker ps -a -q -f "status=exited" | wc -l) -ne 0 ]; then
        echo -e "\n${YELLOW}Starting clear 'Exited' containers...${NC1}\n"
        docker rm $(docker ps -a -q -f "status=exited")
    fi
    if [ $(docker images -f "dangling=true" -q | wc -l) -ne 0 ]; then
        echo -e "\nStarting clear 'Untagged/Dangling' images...\n"
        docker image rmi $(docker images -f "dangling=true" -q)
    fi
    echo -e "\n${YELLOW}Clear docker cache done.${NC1}"
}

# main
main
