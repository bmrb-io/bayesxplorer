#!/bin/sh

sudo docker stop explorer
sudo docker rm explorer


if [ $# -eq 0 ]
  then
    sudo docker build -t explorer .
    echo "Running in development mode."
  else
    sudo docker build --build-arg configfile=$1 -t explorer .
    echo "Running with configuration file: $1"
fi


sudo docker run -d --name explorer  -p 9090:9090 -v /zfs/git/bayesexplorer/app/uploads:/opt/wsgi/uploads --restart=always explorer