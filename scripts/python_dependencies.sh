#!/usr/bin/env bash

virtualenv -p /usr/bin/python3.11 myenv
source /home/ubuntu/env/bin/activate
pip install -r /home/ubuntu/Django-AWSCodePipeline/requirements.txt