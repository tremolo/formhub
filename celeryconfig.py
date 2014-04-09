BROKER_URL = 'amqp://formhub:12345678@localhost:5672/formhub_vhost'
CELERY_RESULT_BACKEND = 'amqp'
CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours.


