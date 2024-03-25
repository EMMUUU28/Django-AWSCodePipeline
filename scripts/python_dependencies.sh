#!/usr/bin/env bash

virtualenv -p /usr/bin/python3.9 /home/ubuntu/env
source /home/ubuntu/env/bin/activate
pip install -r /home/ubuntu/Django-AWSCodePipeline/requirements.txt