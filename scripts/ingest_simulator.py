# ingest_simulator.py
import time
import requests
import random

SAMPLES = [
    ("post1", "This is a short human-written post about local events."),
    ("post2", "Breaking: The government has announced a new policy that will change the market."),
    ("post3", "Buy now! Limited offer, click here to get your reward instantly."),
    ("post4", "According to sources, the prime minister will resign next week. Read more..."),
    ("post5", "The new AI model outperforms humans on many tasks and writes beautiful text effortlessly."),
]

URL = 'http://localhost:8000/detect'

if __name__ == '__main__':
    while True:
        id_, text = random.choice(SAMPLES)
        payload = {'id': id_ + str(random.randint(0,9999)), 'text': text, 'source': 'simulator'}
        try:
            r = requests.post(URL, json=payload, timeout=5)
            print('Sent', payload['id'], '->', r.json())
        except Exception as e:
            print('Error', e)
        time.sleep(2)
