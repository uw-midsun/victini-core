#!/bin/bash

GREEN="\e[0;32m"
RED="\e[0;31m"
NC="\e[0m"

# Check if in virtual env and install requirements
if python3 check_in_venv.py ; then
    echo "${GREEN}>> VIRTUAL ENV DETECTED. INSTALLING/UPDATING REQUIRED PACKAGES ${NC}"
    pip install -r requirements.txt
else
    echo "${RED}>> NOT IN PYTHON VIRTUAL ENV. PLEASE ACTIVATE YOUR VIRTUAL ENV ${NC}"
    exit 1
fi

# Create database
echo "${GREEN}>> CREATING MOCK DATABASE ON PORT 3306 ${NC}"
docker-compose up -d
sleep 1s

# Seed database
RETRIES=3
echo "${GREEN}>> SEEDING DATABASE... ${NC}"
i=1
while [ "$i" -le $RETRIES ]; do
    if python3 seed_database.py ; then
        echo "ATTEMPT ${i}/${RETRIES} ${GREEN}>> SUCCESSFULLY SEEDED MOCK DATABASE ${NC}"
        exit 0
    else
        echo "ATTEMPT ${i}/${RETRIES} ${RED}>> FAILED TO SEED MOCK DATABASE${NC}"
        sleep 2s
    fi
    i=$(( i + 1 ))
done 
echo "${RED}>> FAILED TO SEED MOCK DATABASE AFTER ${RETRIES} RETRIES"
exit 1
