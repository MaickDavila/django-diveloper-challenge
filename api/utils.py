import os
import re
from divelopers_backend.settings import MEDIA_ROOT


def save_pet_image(instance, file_name):
    _, ext = file_name.split(".")
    path = f"pets/{instance.pk}.{ext}"
    if os.path.exists(MEDIA_ROOT / path):
        os.remove(MEDIA_ROOT / path)
    return path


def short_name_is_valid(short_name: str):
    return (
        short_name is not None
        and len(short_name.split(" ")) == 1
        and len(re.findall(r"^[a-zA-Z0-9]+$", short_name)) == 1
    )
