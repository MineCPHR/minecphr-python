import transport
from hypothesis import given, strategies as st


@given(data=st.binary())
def test_roundtrip_encode_decode(data: bytes):
    chunks = transport.encode(data)
    r = b''.join(transport.decode(ch) for ch in chunks)
    assert r == data


@given(data=st.binary())
def test_chunk_length(data: bytes):
    '''Ensure we don't go over the maximum length of MC chat messages'''
    MAX = 255
    chunks = transport.encode(data)
    for ch in chunks:
        assert len(ch) <= MAX


def test_empty():
    '''if there is no data, we send 0 chunks'''
    assert transport.encode(b'') == []


def test_samples():
    SAMPLES = [
            (b'hello', 'cphr0dpjkcmr0'),
            (b'OP', 'cphr0fagq'),
            (b'O1`', 'cphr0fuckq'),
            ]

    for data, msg in SAMPLES:
        assert transport.decode(msg) == data
        assert transport.encode(data) == [msg]
