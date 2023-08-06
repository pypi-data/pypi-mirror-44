import datetime
import hashlib
import json
from decimal import Decimal


def md5(txt: str):
    hash_id = hashlib.md5()
    hash_id.update(txt.encode("utf-8"))
    return hash_id.hexdigest()


def get_unsafe_hash(d: dict, ignored_fields=None):
    if ignored_fields is None:
        ignored_fields = []
    d = {k: v for k, v in d.items() if k not in ignored_fields}
    txt = repr(d)  # Python Environment dependent hashing
    return md5(txt)


def _json_default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, Decimal):
        return str(o)
    raise NotImplementedError()


def get_hash(d: dict, ignored_fields=None):
    if ignored_fields is None:
        ignored_fields = []
    d = {k: v for k, v in d.items() if k not in ignored_fields}
    txt = json.dumps(d, sort_keys=True, default=_json_default)
    return md5(txt)
