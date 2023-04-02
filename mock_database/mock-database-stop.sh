#!/usr/bin/bash

RED="\e[0;31m"
NC="\e[0m"

echo "${RED}>> STOPPING MOCK DATABASE ON PORT 3306 ${NC}"
docker-compose down
