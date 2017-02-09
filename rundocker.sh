#!/bin/bash

COMMAND="$1"
CLUSTER="py"

function build {
    docker network create $CLUSTER || true
    docker build -t pycore .
    docker pull mysql
}

function reload {
    docker cp . server:/home/server/src
    docker exec -d server supervisorctl restart app-uwsgi
    docker exec -d server supervisorctl restart celery
}

function remove {
    docker kill server || true
    docker kill postgres || true
    docker kill redis || true
    docker rm server || true
    docker rm postgres || true
    docker rm redis || true
}

function shell {
    docker exec -ti server bash
}

${COMMAND}
