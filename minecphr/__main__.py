'''
simple demo utility to either decode or encode data from standard input.
'''

from minecphr import transport

TEXT_ENCODING = 'utf8'  # good default

while True:
    try:
        line = input('> ')
    except EOFError:
        break
    if (data := transport.decode(line)) is not None:
        print(data.decode(TEXT_ENCODING, errors='replace'))
    else:
        for msg in transport.encode(line.encode(TEXT_ENCODING)):
            print(msg)
