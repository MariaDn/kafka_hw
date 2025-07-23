import csv
import time
import json
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError
from variables import KAFKA_SERVER, TWEETS_TOPIC, TWEETS_CSV_PATH

def read_tweets(file_path):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['created_at'] = datetime.utcnow().isoformat()
            yield row

def main():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        key_serializer=str.encode,
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        acks='all',
        retries=5,
        compression_type='gzip'
    )

    tweets = read_tweets(TWEETS_CSV_PATH)

    for tweet in tweets:
        tweet_id = tweet.get('tweet_id') or tweet.get('id') or str(hash(tweet['text']))
        future = producer.send(TWEETS_TOPIC, key=tweet_id, value=tweet)
        try:
            record_metadata = future.get(timeout=10)
            print(f"Sent tweet to {record_metadata.topic} partition {record_metadata.partition}: {tweet['text'][:50]}...")
        except KafkaError as e:
            print(f"Failed to send tweet: {e}")
        time.sleep(0.08)

if __name__ == '__main__':
    main()
