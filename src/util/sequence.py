import hashlib
import uuid
from datetime import datetime


def fetch_unique_uuid_md5_id():
    rand_unique_id = str(datetime.utcnow()) + str(uuid.uuid4())
    return hashlib.md5(rand_unique_id.encode("utf-8")).hexdigest()
