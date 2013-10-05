from datetime import datetime

from django.utils.timezone import utc


def get_current_time():
    try:
        now = datetime.utcnow().replace(tzinfo=utc)
    except ImportError:
        now = datetime.utcnow()
    return now