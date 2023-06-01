import unittest
from ecc import G, Signature, PrivateKey
from helper import encode_base58, hash256,little_endian_to_int

class ECCTest04(unittest.TestCase):
    # ex. 7 Сформируейте самостоятельно адрес для сети testnet, используя самые длинные
    # секретные данные, котоыре вам только известны
    def exercise_7(self):
        passphrase = b'dasha@programmingblockchain.com my secret'
        secret = little_endian_to_int(hash256(passphrase))
        pk = PrivateKey(secret)
        print(pk.point.address(testnet=True))

    # Сформулируйте секретный ключ в формате WIF, исходя из следующих секретных данных
    def exercise_6(self):
        # Сжатый формат SEC для сети testnet
        pk = PrivateKey(5003)
        print(pk.wif(True, True))

        # Несжатый формат SEC для сети testnet
        pk = PrivateKey(2021**5)
        print(pk.wif(False, True))

        # Сжатый формат SEC для сети mainnet
        pk = PrivateKey(0x54321deadbeef)
        print(pk.wif(True, False))

    # Найти адреса, соответствующие открытым ключам, которым отвечают
    # следующие секретные ключи
    def exercise_5(self):
        # использовать несжатый формат SEC в сети testnet
        e = 5002
        point = e * G
        print(point.address(False, True))
        print()

        # использовать сжатый формат SEC в сети testnet
        e = 2020 ** 5
        point = e * G
        print(point.address(True, True))
        print()

        #использовать сжатый формат SEC в сети mainet
        e = 0x12345deadbeef
        point = e * G
        print(point.address())

    def exercise_4(self):
        digits = ( 
        '7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d',
        'eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c',
        'c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6'
        )
        for digit in digits:
            print('digit: {} ->'.format(digit))
            print(encode_base58(bytes.fromhex(digit)))
            print()

    
    # Представьте в формате DER подпись со следующими величинами r и s:
    def exercise_3(self):
        r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
        s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        signature = Signature(r, s)
        print(signature)
        der = signature.der()
        print(der)
        print(der.hex())

    # Представляем открытый ключ в несжатом формате SEC,
    # если имеются следующие секретные ключи
    def exercise_1(self):
        e = 5000
        point = e * G
        print(point.sec(False).hex())
        print(point, '\n')

        e = 2018 ** 5
        point = e * G
        print(point.sec(False).hex())
        print(point, '\n')

        e = 0xdeadbeef12345
        point = e * G
        print(point.sec(False).hex())
        print(point, '\n')

    # Находим открытый ключ в сжатом формате SEC
    # если имеются следующие секретные ключи
    def exercise_2(self):
        e = 5001
        point = e * G
        print(point.sec().hex())
        print(point, '\n')

        e = 2019 ** 5
        point = e * G
        print(point.sec().hex())
        print(point, '\n')

        e = 0xdeadbeef54321
        point = e * G
        print(point.sec().hex())
        print(point, '\n')
        