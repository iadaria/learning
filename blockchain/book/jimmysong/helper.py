BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

# TODO Сделать отладку и посмотреть по шагам работу этой функции

def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
        num = int.from_bytes(s, 'big')
        prefix = '1' * count
        result = ''
        while num > 0:
            num, mod = divmod(num, 58)
            result = BASE58_ALPHABET[mod] + result
    return prefix + result
      