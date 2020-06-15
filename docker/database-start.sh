#! /bin/bash

# start a mariadb database

DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}" )" )"

NAME=shelterreg
VOLUME="${NAME}-db"
TAG="mariadb:10.4-focal"

function F() {
    echo "$0: Fatal Error: $*" 1>&2
    exit 1
}


if docker volume inspect $VOLUME > /dev/null 2>&1; then
    # volume exists
    true
else
    echo "Creating new volume $VOLUME"
    docker volume create "$VOLUME" || F "Could not create volume $VOLUME"
fi



docker run \
    --rm \
    --publish "3306:3306" \
    --name "$NAME" \
    --volume "$VOLUME:/var/lib/mysql" \
    -e MYSQL_ALLOW_EMPTY_PASSWORD=1 \
    -d "$TAG"

$DIR/connect --execute "SET GLOBAL time_zone = 'UTC'"

