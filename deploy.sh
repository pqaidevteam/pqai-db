# This script pull the latest code from the Github repo and the assets required
# by this service, then will create and run a docker container running the
# service
#
# Run it with `bash deploy.sh`
#
# Please make sure your environment variables are properly set up in the
# .env file (see README) before running this script
#
# You might need to give this file executable permission prior to running:
# `chmod +x deploy.sh`
#

git checkout main
git pull origin main

docker build . -t pqai_db:latest
docker-compose down
docker-compose up -d
