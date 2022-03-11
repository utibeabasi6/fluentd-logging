#!/bin/sh

# app_url="http://app:5001"
# fluentd_url="http://fluentd:9880"

apk add curl

while true;
    do
        curl http://app:5001/logs || curl -X POST http://fluentd:9880/httplogs.log -d 'json={"ok": false}';
        sleep 3;
    done