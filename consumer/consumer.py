#!/usr/bin/env python

import os
import logging
import sys
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING
import time
import json
import re
from slack_sdk.rtm_v2 import WebClient, SlackApiError

token = os.environ.get("SLACK_BOT_TOKEN")

client = WebClient(token=token)
logger = logging.getLogger()

def sendSlackMessage(json):
    try:
        response = client.chat_postMessage(
            channel="logs",
            text=f"""It seems the application is down!

            `{json}`
            
            :disappointed_relieved:"""
        
        )
    except SlackApiError as e:
        logger.error("Error", e)


if __name__ == '__main__':

    # Wait for broker to come online
    time.sleep(30)

    # Parse the configuration.
    config_parser = ConfigParser()

    with open("config.ini") as f:
        config_parser.read_file(f)
        config = dict(config_parser['default'])
        config.update(config_parser['consumer'])

    # Create Consumer instance
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if os.environ.get("RESET_OFFSET"):
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topic
    topic = "logs"
    consumer.subscribe([topic], on_assign=reset_offset)

    # Poll for new orders from Kafka and add them to the database.
    try:
        while True:
            msg = consumer.poll(5.0)
            if msg is None:
                logger.warning("Waiting...")
            elif msg.error():
                logger.error(f"ERROR: {msg.error()}")
            else:
                data = json.loads(msg.value())
                if data["ok"] != True:
                    sendSlackMessage(data)
                # Extract the (optional) key and value, and print.
                logger.warning(data)

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
