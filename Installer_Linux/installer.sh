#!/bin/bash
set -e
set -x

bash install.sh 2>&1 | tee logfile.txt
