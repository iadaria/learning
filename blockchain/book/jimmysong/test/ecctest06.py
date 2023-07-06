import unittest
from io import BytesIO
from tx import Tx
from script import Script

class ECCTest06(unittest.TestCase):
    def exercise_0(self):
        z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        sec = bytes.fromhex('04887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34')
        sig = bytes.fromhex('3045022000eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c022100c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab601')
        # Сценарий ScriptPubkey для p2pk состоит из открытого ключа в формате sec и
        # операции OP_CHECKSIG с кодом 0xac или 172"""
        script_pubkey = Script([sec, 0xac])
        script_sig = Script([sig])
        combined_script = script_sig + script_pubkey
        # Вычисляем команды и проверяем сценарий на достоверность
        print(combined_script.evaluate(z))