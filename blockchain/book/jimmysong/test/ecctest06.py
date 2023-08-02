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

    # Создайте сценаий ScriptSig, способный разблокировать открытый ключ по
    # Следующему сценарию ScriptPubKey = 767695935687
    # 56=OP_6, 76=OP_DUP, 87=OP_EQUAL, 93=OP_ADD, 95=OP_MUL
    # Операция OP_2 с кодом 52 удволетворит уравнениею x^2 + x - 6 = 0
    def exercise_3(self):
        script_pubkey = Script([0x76, 0x76, 0x95, 0x93, 0x56, 0x87])
        script_sig = Script([0x52])
        combined_script = script_sig + script_pubkey
        print(combined_script.evaluate(0))

    # Высните назанчение следующего сценария
    # 6e879169a77ca787
    # Кодвы в этом сценарии обозначают следующие операции
    # 69=OP_VERIFY, 6e=OP_2DUP, 7c=OP_SWAP, 87=OP_EQUAL, 91=OP_NOT, a7=OP_SHA1
    def exercise_4(self):
        script_pubkey = Script([0x6e, 0x87, 0x91, 0x69, 0xa7, 0x7c, 0xa7, 0x87])
        c1 = '255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f576964746820\
32203020522f4865696768742033203020522f547970652034203020522f537562747970652035\
203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e67\
74682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8\
fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1ff\
fe017f46dc93a6b67e013b029aaa1db2560b45ca67d688c7f84b8c4c791fe02b3df614f86db169\
0901c56b45c1530afedfb76038e972722fe7ad728f0e4904e046c230570fe9d41398abe12ef5bc\
942be33542a4802d98b5d70f2a332ec37fac3514e74ddc0f2cc1a874cd0c78305a215664613097\
89606bd0bf3f98cda8044629a1'
        c2 = '255044462d312e330a25e2e3cfd30a0a0a312030206f626a0a3c3c2f576964746820\
32203020522f4865696768742033203020522f547970652034203020522f537562747970652035\
203020522f46696c7465722036203020522f436f6c6f7253706163652037203020522f4c656e67\
74682038203020522f42697473506572436f6d706f6e656e7420383e3e0a73747265616d0affd8\
fffe00245348412d3120697320646561642121212121852fec092339759c39b1a1c63c4c97e1ff\
fe017346dc9166b67e118f029ab621b2560ff9ca67cca8c7f85ba84c79030c2b3de218f86db3a9\
0901d5df45c14f26fedfb3dc38e96ac22fe7bd728f0e45bce046d23c570feb141398bb552ef5a0\
a82be331fea48037b8b5d71f0e332edf93ac3500eb4ddc0decc1a864790c782c76215660dd3097\
91d06bd0af3f98cda4bc4629b1'
        collision1 = bytes.fromhex(c1)
        collision2 = bytes.fromhex(c2)
        script_sig = Script([collision1, collision2])
        combined_script = script_sig + script_pubkey
        print(combined_script.evaluate(0))