from helper import decode_base58, SIGHASH_ALL, hash256, little_endian_to_int
from ecc import PrivateKey
import unittest
from tx import Tx, TxIn, TxOut
from script import Script
from io import BytesIO

class ECCTest07(unittest.TestCase):
    def exercise_1(self):
      '''Создадим транзакцию с одним вводом и двумя выводами'''
      prev_tx = bytes.fromhex('0d6fe5213c0b3291f208cba8bfb59b7476dffacc4e5cb66f6eb20a080843a299')
      prev_index=3
      tx_in = TxIn(prev_tx, prev_index)
      tx_outs = []
      change_amount = int(0.33*100000000)
      change_h160 = decode_base58('mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2')
      change_script = Script.p2pkh_script(change_h160)
      change_output = TxOut(amount=change_amount, script_pubkey=change_script)

      target_amount = int(0.1*100000000)
      target_h160 = decode_base58('mnrVtF8DWjMu839VW3rBfgYaAfKk8983Xf')
      target_script = Script.p2pkh_script(target_h160)
      target_output = TxOut(amount=target_amount, script_pubkey=target_script)
      tx_obj = Tx(1, [tx_in], [change_output, target_output], 0, True)
      print(tx_obj)
      
    def exercise_2(self):
        raw_tx = ('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf830\
3c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccf\
cf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8\
e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278\
afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88a\
c99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(bytes.fromhex(raw_tx))
        transaction = Tx.parse(stream)
        print(transaction.fee() >= 0)
        z = transaction.sig_hash(0)
        private_key = PrivateKey(secret=8675309)
        der = private_key.sign(z).der()
        sig = der + SIGHASH_ALL.to_bytes(1, 'big')
        sec = private_key.point.sec()
        script_sig = Script([sig, sec])
        transaction.tx_ins[0].script_sig = script_sig
        print(transaction.serialize().hex())
    
    # https://live.blockcypher.com/btc-testnet/tx/2da50abdf11dd1b640203e12dc9a8d0fa1500549893f2bc9963252327def1b35/
    # mwfiJftYNCzUiwZimHAXpacd1gvMFkiKa9
    def exercise_3(self):
       secret = little_endian_to_int(hash256(b'Daria Andreevna secret'))
       private_key = PrivateKey(secret)
       print(private_key.point.address(testnet=True))

    def exercise_4(self):
        prev_tx = bytes.fromhex('2da50abdf11dd1b640203e12dc9a8d0fa1500549893f2bc9963252327def1b35')
        prev_index = 1
        target_address = 'mwfiJftYNCzUiwZimHAXpacd1gvMFkiKa9'
        target_amount = 0.001
        change_address = 'miKegze5FQNCnGw6PKyqUbYUeBa4x2hFeM'
        # >>> target_address = 'miKegze5FQNCnGw6PKyqUbYUeBa4x2hFeM'
        # >>> target_amount = 0.01
        # >>> change_address = 'mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2'   
        change_amount = 0.009
        secret = 8675309
        priv = PrivateKey(secret=secret)
        tx_ins = []
        tx_ins.append(TxIn(prev_tx, prev_index))
        
        tx_outs = []
        h160 = decode_base58(target_address)
        script_pubkey = Script.p2pkh_script(h160)
        target_satoshis = int(target_amount * 100000000)
        tx_outs.append(TxOut(target_satoshis, script_pubkey))
        
        h160 = decode_base58(change_address)
        script_pubkey = Script.p2pkh_script(h160)
        target_satoshis = int(change_amount * 100000000)
        tx_outs.append(TxOut(target_satoshis, script_pubkey))

        tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)
        
        print(tx_obj.sign_input(0, priv))

        print(tx_obj.serialize().hex())

    def exercise_5(self):
        prev_tx_1 = bytes.fromhex('11d05ce707c1120248370d1cbf5561d22c4f83aeba04367\
92c82e0bd57fe2a2f')
        prev_index_1 = 1
        prev_tx_2 = bytes.fromhex('51f61f77bd061b9a0da60d4bedaaf1b1fad0c11e65fdc74\
4797ee22d20b03d15')
        prev_index_2 = 2
        target_address = 'mwJn1YPMq7y5F8J3LkC5Hxg9PHyZ5K4cFv'
        target_amount = 0.0429
        secret = 8675309
        priv = PrivateKey(secret=secret)
        tx_ins = []
        tx_ins.append(TxIn(prev_tx_1, prev_index_1))                     
        tx_ins.append(TxIn(prev_tx_2, prev_index_2))
        tx_outs = []
        h160 = decode_base58(target_address)
        secret_pubkey = Script.p2pkh_script(h160)
        target_satoshis = int(target_amount * 100000000)
        tx_outs.append(TxOut(target_satoshis, secret_pubkey))
        tx_obj = Tx(1, tx_ins, tx_outs, 0, testnet=True)
        print(tx_obj.sign_input(0, priv))
        #True
        print(tx_obj.sign_input(1, priv))
        #True
        print(tx_obj.serialize().hex(0))