#!/bin/bash
npm install
npm run build
sudo docker build -t konglsh96/fraud-detection:front . 
sudo docker push konglsh96/fraud-detection:front
