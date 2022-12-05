
def toUnicode(ascii):
    unicode = ascii.encode().decode('idna')
    return unicode

def toPunycode(unicode):
    ascii = unicode.encode('idna').decode()
    return ascii