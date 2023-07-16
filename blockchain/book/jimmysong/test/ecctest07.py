#from helper import decode_base58
from ecc import PrivateKey
from helper import hash256, lettle_endian_to_int
import unittest
from tx import Tx, TxIn, TxOut
from script import p2pkh_script

class ECCTest06(unittest.TestCase):
    def exercise_0(self):
        secret = lettle_endian_to_int(hash256(b'Dasha Iakimova'))

    # def exercise_1(self):
    #   '''Создадим транзакцию с одним вводом и двумя выводами'''
    #   # prev_tx = bytes.fromhex('0d6fe5213c0b3291f208cba8bfb59b7476dffacc4e5cb66f6eb20a080843a299')
    #   # prev_index=3
    #   # tx_in = TxIn(prev_tx, prev_index)
    #   # tx_outs = []
    #   # change_amount = int(0.33*100000000)
    #   # change_h160 = decode_base58('mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2')
    #   # change_script = p2pkh_script(change_h160)
    #   # change_output = TxOut(amount=change_amount, script_pubkey=change_script)

    #   # target_amount = int(0.1*100000000)
    #   # target_h160 = decode_base58('mnrVtF8DWjMu839VW3rBfgYaAfKk8983Xf')
    #   # target_script = p2pkh_script(target_h160)
    #   # target_output = TxOut(amount=target_amount, script_pubkey=target_script)
    #   # tx_obj = Tx(1, [tx_in], [change_output, target_output], 0, True)
    #   # print(tx_obj)