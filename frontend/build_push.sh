#!/bin/bash
npm install
npm run build
sudo docker build -t konglsh96/rain-forecast-mlops:front . 
sudo docker push konglsh96/rain-forecast-mlops:front
