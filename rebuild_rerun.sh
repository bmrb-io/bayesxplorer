#!/bin/sh

sudo docker stop explorer
sudo docker rm explorer
sudo docker build -t explorer .
sudo docker run -d --name explorer  -p 9090:9090 -v /zfs/git/bayesexplorer/app/uploads:/wsgi/uploads --restart=always explorer
