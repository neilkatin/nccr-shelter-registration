#! /bin/bash

#
# do minimual bootstraping of mysql environment
#
#

DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}" )" )"


$DIR/connect --execute "create database shelterreg;"
$DIR/connect --execute "grant all privileges on shelterreg.* to 'shelterreg'@'%' identified by 'shelterreg';"
$DIR/connect --execute "grant all privileges on shelterreg.* to 'shelterreg'@'localhost' identified by 'shelterreg';"
