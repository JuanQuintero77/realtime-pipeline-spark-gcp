import json
import time

from google.cloud import pubsub_v1

import config
from event_builder import build_event


def generate_events():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(config.PROJECT_ID, config.TOPIC_NAME)

    start_time = time.time()
    total_published = 0

    print(f"Starting generator — max runtime: {config.MAX_RUNTIME_SECONDS}s, batch size: {config.BATCH_SIZE}, topic: {topic_path}")

    while time.time() - start_time < config.MAX_RUNTIME_SECONDS:
        events = [build_event() for _ in range(config.BATCH_SIZE)]

        futures = [
            publisher.publish(topic_path, json.dumps(event).encode("utf-8"))
            for event in events
        ]
        for future in futures:
            future.result()

        total_published += len(events)
        elapsed = time.time() - start_time
        print(f"Batch published: {len(events)} events | total: {total_published} | elapsed: {elapsed:.1f}s")

        time.sleep(config.SLEEP_TIME)

    print(f"Generator finished. Total events published: {total_published}")


if __name__ == "__main__":
    generate_events()
            
        


   