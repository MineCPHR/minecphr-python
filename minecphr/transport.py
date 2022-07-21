'''
A bech32-based method for transmitting arbitrary streams of data over Minecraft
chat messages.
'''

from typing import Optional

import bech32

# results in 240 bech32 characters, fits in a MC chat message
CHUNK_LEN = 150

# Distinctive prefix for the chat messages
PREFIX = 'cphr1'


def encode(payload: bytes) -> list[str]:
    messages = []

    for i in range(0, len(payload), 150):
        chunk = payload[i:][:150]
        chunk = bech32.convertbits(chunk, 8, 5)
        messages.append(PREFIX+''.join(bech32.CHARSET[d] for d in chunk))

    return messages


def decode(msg: str) -> Optional[bytes]:
    msg = msg.lower()
    if not msg.startswith(PREFIX):
        return None
    msg = msg[len(PREFIX):]

    if not all(c in bech32.CHARSET for c in msg):
        return None
    data = (bech32.CHARSET.find(c) for c in msg)

    if (data := bech32.convertbits(data, 5, 8, pad=False)) is not None:
        return bytes(data)
