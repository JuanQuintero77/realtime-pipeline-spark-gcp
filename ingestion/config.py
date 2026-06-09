import os

BATCH_SIZE = int(os.getenv("BATCH_SIZE", "50"))
SLEEP_TIME = int(os.getenv("SLEEP_TIME", "10"))
MAX_RUNTIME_SECONDS = int(os.getenv("MAX_RUNTIME_SECONDS", "300"))  # 5 minutes default

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
TOPIC_NAME = os.getenv("PUBSUB_TOPIC", "events")