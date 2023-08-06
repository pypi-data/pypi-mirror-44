# !/bin/bash

# run celery worker
celery -A oracle.celery.task worker -l info