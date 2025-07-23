import os

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")
TWEETS_TOPIC = os.getenv("TWEETS_TOPIC", "tweets")
TWEETS_CSV_PATH = os.getenv("TWEETS_CSV_PATH", "/app/data/twcs.csv")
