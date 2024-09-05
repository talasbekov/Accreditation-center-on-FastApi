import base64
import datetime

import re

from fastapi import HTTPException


def is_valid_phone_number(phone_number: str):

    validate_phone_number_pattern = "^\+?77([0124567][0-8]\d{7})$"
    result = re.match(validate_phone_number_pattern, phone_number)

    return result


def is_owner(user_role: str):
    if user_role != "OWNER":
        raise HTTPException(status_code=403, detail="You don't have permission!")


def is_valid_uuid(uuid_str):
    try:
        uuid_obj = str(uuid_str, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_str


def convert_str_to_datetime(date: str):
    return datetime.datetime.strptime(date, "%Y-%m-%d")

def correct_base64_padding(data: str) -> str:
    """Add padding to Base64 string if necessary."""
    # Remove existing padding
    data = data.rstrip("=")
    # Calculate necessary padding
    padding_needed = -len(data) % 4
    return data + "=" * padding_needed


def is_valid_base64(data: str) -> bool:
    """Check if a string is a valid base64 encoded string."""
    try:
        if isinstance(data, str):
            base64.b64decode(data, validate=True)
            return True
    except base64.binascii.Error:
        return False
    return False
