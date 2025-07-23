# Tweet Streamer to Kafka

This project demonstrates how to stream tweet data into Apache Kafka using Python. 

### Setup

Create .env

KAFKA_SERVER=
TWEETS_TOPIC=
TWEETS_CSV_PATH=

Build the Docker image

docker-compose build

Start the Kafka stack and tweet streamer

docker-compose up

In a new terminal, consume messages from the tweets topic

docker exec -it kafka kafka-console-consumer \
  --bootstrap-server kafka:9092 \
  --topic tweets \
  --from-beginning
