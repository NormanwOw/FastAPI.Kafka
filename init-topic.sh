#!/bin/bash
set -e

while ! nc -z localhost 9092; do
  sleep 1
done

TOPIC="my-topic"

if ! /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list | grep -q "^${TOPIC}$"; then
  /opt/kafka/bin/kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 3 \
    --partitions 3 \
    --topic ${TOPIC}
fi