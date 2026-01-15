import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.celery_worker.tasks import celery_app

if __name__ == "__main__":
    celery_app.start()
