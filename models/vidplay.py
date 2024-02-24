import requests
from typing import Union
from . import subtitle
import re
import base64

def decode_data(key: str, data: Union[bytearray, str]) -> bytearray:
    key_bytes = bytes(key, 'utf-8')
    s = bytearray(range(256))
    j = 0

    for i in range(256):
        j = (j + s[i] + key_bytes[i % len(key_bytes)]) & 0xff
        s[i], s[j] = s[j], s[i]

    decoded = bytearray(len(data))
    i = 0
    k = 0

    for index in range(len(data)):
        i = (i + 1) & 0xff
        k = (k + s[i]) & 0xff
        s[i], s[k] = s[k], s[i]
        t = (s[i] + s[k]) & 0xff

        if isinstance(data[index], str):
            decoded[index] = ord(data[index]) ^ s[t]
        elif isinstance(data[index], int):
            decoded[index] = data[index] ^ s[t]
        else:
            return None

    return decoded

async def handle_vidplay(url) -> str:
    furl = url
    url = url.split("?")
    subtitles = {}
    subtitles = await subtitle.vscsubs(url[1])
    cleaned_subtitles = [{"file": sub["file"], "label": sub["label"], "kind": sub["kind"]} for sub in subtitles]
    return cleaned_subtitles
