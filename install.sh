#!/usr/bin/env bash

virtualenv -p python3 .env

./.env/bin/pip install -r pip-dep.txt
