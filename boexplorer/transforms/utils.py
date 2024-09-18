import datetime
import hashlib
import random
import string
import uuid

import dateutil
import pytz


def random_string(length):
    """Generate random string of specified length"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def format_date(d):
    """Format date in ISO 8601"""
    if "." in d:
        return datetime.datetime.strptime(d, "%d.%m.%Y").strftime("%Y-%m-%d")
    else:
        return dateutil.parser.isoparse(d).strftime("%Y-%m-%d")


def current_date_iso():
    """Generate current date in ISO 8601"""
    return datetime.datetime.now(pytz.timezone('Europe/London')).strftime("%Y-%m-%d")


def generate_statement_id(name, role, version=None):
    """Generate statement ID deterministically"""
    if version:
        seed = '-'.join([name, role, version])
    else:
        seed = '-'.join([name, role])
    m = hashlib.md5()
    m.update(seed.encode('utf-8'))
    return str(uuid.UUID(m.hexdigest()))
