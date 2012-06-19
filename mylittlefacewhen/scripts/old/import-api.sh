#!/usr/bin/env bash
if ps -ef |grep -v grep |grep import-api.py ; then
    echo "already running"
    exit 0
else
    echo "not running"
    python /home/inopia/webapps/mylittlefacewhen/mylittlefacewhen/scripts/import_api.py > /home/inopia/import.log
    exit 0
fi
