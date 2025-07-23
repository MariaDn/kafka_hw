import os
import json
from kafka import KafkaConsumer
from datetime import datetime
import pytz
from variables import KAFKA_SERVER, TWEETS_TOPIC

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

consumer = KafkaConsumer(
  TWEETS_TOPIC,
  bootstrap_servers=[KAFKA_SERVER],
  auto_offset_reset='latest',
  enable_auto_commit=True,
  value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def get_filename_from_timestamp(ts_str):
  if ts_str.endswith("Z"):
    dt = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%fZ")
  else:
    dt = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%f")
  
  dt = dt.replace(tzinfo=pytz.UTC)
  local_dt = dt.astimezone(pytz.timezone("Europe/Kyiv"))
  return local_dt.strftime("tweets_%d_%m_%Y_%H_%M.csv")


file_handles = {}

print("Starting consumer...")

try:
  for message in consumer:
    data = message.value
    author_id = data.get("author_id")
    created_at = data.get("created_at")
    text = data.get("text")

    if not all([author_id, created_at, text]):
      continue

    filename = get_filename_from_timestamp(created_at)
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "a", encoding="utf-8") as f:
      f.write(f'"{author_id}","{created_at}","{text.replace(chr(10), " ").replace(chr(13), " ")}"\n')

except KeyboardInterrupt:
    print("Stopping consumer...")