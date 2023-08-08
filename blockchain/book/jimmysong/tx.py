from helper import (
    hash256, little_endian_to_int, read_varint, encode_varint, int_to_little_endian,
    SIGHASH_ALL,
    )
from io import BytesIO
import json
import requests
from script import Script

class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False):
        # Версия обозначает, какие дополнительные средства применяются в транзакции
        self.version = version
        # Вводы определяют затрачиваемые биткоины
        self.tx_ins = tx_ins
        # Выводы - куда биткоины направляются
        self.tx_outs = tx_outs
        # Время блокировки - момент, с которого данная транзакция становится действительной
        self.locktime = locktime
        #
        self.testnet = testnet
    # Display
    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'

        return 'tx: {}\nversion: {}\ntx_ins:\n{}tx_outs:\n{}locktime: {}'.format(
            self.id(),
            self.version,
            tx_ins,
            tx_outs,
            self.locktime
        )

    def id(self):
        '''Хеш транзакции в удобночитаемой шестнадцатеричной форме'''
        return self.hash().hex()

    def hash(self):
        '''Хэш устаревшей сериализации в двоичной форме'''
        return hash256(self.serialize())[::-1]

    @classmethod
    def parse(cls, stream, testnet=False):
        version = little_endian_to_int(stream.read(4))
        # Количество вводов
        num_inputs = read_varint(stream)
        # Вводы
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(stream))
        # Выводы
        num_outputs = read_varint(stream)
        outputs = []
        for _ in range(num_outputs):
            outputs.append(TxOut.parse(stream))
        # Время блокировки
        locktime = little_endian_to_int(stream.read(4))
        return cls(version, inputs, outputs, locktime, testnet=testnet)

    def serialize(self):
        '''Возвращает результат сериализации транзакции
            в последовательность байтов'''
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)
        return result

    # Рассчитываем плату за транзакцию
    def fee(self, testnet=False):
        input_sum, output_sum = 0, 0
        for tx_in in self.tx_ins:
            input_sum += tx_in.value(testnet=testnet)
        for tx_out in self.tx_outs:
            output_sum += tx_out.amount
        return input_sum - output_sum
    
    # Реализуем вычисление хэша подписи
    def sig_hash(self, input_index, redeem_script=None):
        '''Returns the integer representation of the hash that needs to get
        signed for index input_index'''
        # start the serialization with version
        # use int_to_little_endian in 4 bytes
        s = int_to_little_endian(self.version, 4)
        # add how many inputs there are using encode_varint
        s += encode_varint(len(self.tx_ins))
        # loop through each input using enumerate, so we have the input index
        for i, tx_in in enumerate(self.tx_ins):
            # if the input index is the one we're signing
            if i == input_index:
                # if the RedeemScript was passed in, that's the ScriptSig
                if redeem_script:
                    script_sig = redeem_script
                # otherwise the previous tx's ScriptPubkey is the ScriptSig
                else:
                    script_sig = tx_in.script_pubkey(self.testnet)
            # Otherwise, the ScriptSig is empty
            else:
                script_sig = None
            # add the serialization of the input with the ScriptSig we want
            s += TxIn(
                prev_tx=tx_in.prev_tx,
                prev_index=tx_in.prev_index,
                script_sig=script_sig,
                sequence=tx_in.sequence,
            ).serialize()
        # add how many outputs there are using encode_varint
        s += encode_varint(len(self.tx_outs))
        # add the serialization of each output
        for tx_out in self.tx_outs:
            s += tx_out.serialize()
        # add the locktime using int_to_little_endian in 4 bytes
        s += int_to_little_endian(self.locktime, 4)
        # add SIGHASH_ALL using int_to_little_endian in 4 bytes
        s += int_to_little_endian(SIGHASH_ALL, 4)
        # hash256 the serialization
        h256 = hash256(s)
        # convert the result to an integer using int.from_bytes(x, 'big')
        return int.from_bytes(h256, 'big')

    def verify_input(self, input_index):
        '''Returns whether the input has a valid signature'''
        # get the relevant input
        tx_in = self.tx_ins[input_index]
        # grab the previous ScriptPubKey
        script_pubkey = tx_in.script_pubkey(testnet=self.testnet)
        # check to see if the ScriptPubkey is a p2sh using
        # Script.is_p2sh_script_pubkey()
        if script_pubkey.is_p2sh_script_pubkey():
            # the last cmd in a p2sh is the RedeemScript
            cmd = tx_in.script_sig.cmds[-1]
            # prepend the length of the RedeemScript using encode_varint
            raw_redeem = encode_varint(len(cmd)) + cmd
            # parse the RedeemScript
            redeem_script = Script.parse(BytesIO(raw_redeem))
        # otherwise RedeemScript is None
        else:
            redeem_script = None
        # get the signature hash (z)
        # pass the RedeemScript to the sig_hash method
        z = self.sig_hash(input_index, redeem_script)
        # combine the current ScriptSig and the previous ScriptPubKey
        combined = tx_in.script_sig + script_pubkey
        # evaluate the combined script
        return combined.evaluate(z)
    
    # Верифицируем всю транзакцию
    def verify(self):
        '''Произвести верификацию данной транзакции'''
        if self.fee() < 0: # Проверяем, не создаются ли биткойны в данной транзакции
            return False
        for i in range(len(self.tx_ins)):
        # Проверяем, имеется ли у каждого ввода правильное поле ScriptSig
            if not self.verify_input(i):
                return False
        return True
    
    # Реализуем подписание вводов транзакций
    def sign_input(self, input_index, private_key):
        z = self.sig_hash(input_index)
        der = private_key.sign(z).der()
        sig = der + SIGHASH_ALL.to_bytes(1, 'big')
        sec = private_key.point.sec()
        self.tx_ins[input_index].script_sig = Script([sig, sec])
        return self.verify_input(input_index)
    # Определяем является ли транзакция монетизирующей
    def is_coinbase(self):
        if len(self.tx_ins) != 1:
            return False
        first_input = self.tx_ins[0]
        if first_input.prev_tx != b'\x00' * 32:
            return False
        if first_input.prev_index != 0xffffffff
            return False
        return True

class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        self.sequence = sequence
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig

    def __repr__(self):
        return '{}:{}'.format(
            self.prev_tx.hex(),
            self.prev_index,
        )

    # Делаем синтаксический анализ вводов транзакций
    @classmethod
    def parse(cls, stream):
        '''Этот метод принимает поток байтов и сначала синтаксически
            анализирует ввод транзакции, а затем
            возвращает объект типа TxIn'''
        # read(n=-1) Read up to n bytes from the stream.
        # if n is set to -1, read until EOF, then return all read bytes.
        prev_tx = stream.read(32)[::-1]
        prev_index = little_endian_to_int(stream.read(4))
        script_sig = Script.parse(stream)
        sequence = little_endian_to_int(stream.read(4))
        return cls(prev_tx, prev_index, script_sig, sequence)

    def serialize(self):
        '''Возвращаем рузультат вериализации вввода транзакции
            в последовательность байтов'''
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result

    # Тперь можно получить предыдущую траназакцию по идентификатору предтранзакции из ввода
    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    def value(self, testnet=False):
        '''Получаем сумму из вывода, просматриваем хеш транзакции.
            Возвращаем сумму в сатоши'''
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].amount

    def script_pubkey(self, testnet=False):
        '''Получаем сценарий ScriptPubKey просматривая хеш транзакции.
            Возвращаем объект типа Script'''
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].script_pubkey

class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)

    @classmethod
    def parse(cls, stream):
        '''Этот метод принимает поток байтов и сначала синтаксически
            анализирует вывод транзакции а затем
            возвращает объект типа TxOut'''
        # 64 бита или 8 байт занимает сумма
        amount = little_endian_to_int(stream.read(8))
        script_pubkey = Script.parse(stream)
        return cls(amount, script_pubkey)

    def serialize(self):
        '''Возвращаем результат вериализации вывода транзакции
            в последовательность байтов'''
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result

class TxFetcher:
    cache = {}

    @classmethod
    def get_url(cls, testnet=False):
        if testnet:
            return 'https://blockstream.info/testnet/api/'
        else:
            return 'https://blockstream.info/api/'

    @classmethod
    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cls.cache):
            url = '{}/tx/{}/hex'.format(cls.get_url(testnet), tx_id)
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError('unexpected response: {}'.format(response.text))
            # make sure the tx we got matches to the hash we requested
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
            if tx.id() != tx_id:
                raise ValueError('not the same id: {} vs {}'.format(tx.id(), tx_id))
            cls.cache[tx_id] = tx
        cls.cache[tx_id].testnet = testnet
        return cls.cache[tx_id]

    @classmethod
    def load_cache(cls, filename):
        disk_cache = json.loads(open(file=filename, mode='r').read())
        for k, raw_hex in disk_cache.items():
            raw = bytes.fromhex(raw_hex)
            if raw[4] == 0:
                raw = raw[:4] + raw[:6]
                tx = Tx.parse(BytesIO(raw))
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Tx.parse(BytesIO(raw))
            cls.cache[k] = tx

    @classmethod
    def dump_cache(cls, filename):
        with open(filename, 'w') as f:
            to_dump = {k: tx.serialize().hex() for k, tx in cls.cache.items()}
            s = json.dumps(to_dump, sort_keys=True, index=4)
            f.write(s)

# class TxTest(TestCase):
#     cache_file = './tx.cache'

#     @classmethod
#     def setUpClass(cls):
#         # fill with cache so we don't have to be online to run these tests
#         TxFetcher.load_cache(cls.cache_file)

#     def test_parse_version(self):
#         raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
#         stream = BytesIO(raw_tx)
#         tx = Tx.parse(stream)
#         self.assertEqual(tx.version, 1)

#     def test_parse_inputs(self):
#         raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
#         stream = BytesIO(raw_tx)
#         tx = Tx.parse(stream)
#         self.assertEqual(len(tx.tx_ins), 1)
#         want = bytes.fromhex('d1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81')
#         self.assertEqual(tx.tx_ins[0].prev_tx, want)
#         self.assertEqual(tx.tx_ins[0].prev_index, 0)
#         want = bytes.fromhex('6b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
#         self.assertEqual(tx.tx_ins[0].script_sig.serialize(), want)
#         self.assertEqual(tx.tx_ins[0].sequence, 0xfffffffe)

#     def test_parse_outputs(self):
#         raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
#         stream = BytesIO(raw_tx)
#         tx = Tx.parse(stream)
#         self.assertEqual(len(tx.tx_outs), 2)
#         want = 32454049
#         self.assertEqual(tx.tx_outs[0].amount, want)
#         want = bytes.fromhex('1976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac')
#         self.assertEqual(tx.tx_outs[0].script_pubkey.serialize(), want)
#         want = 10011545
#         self.assertEqual(tx.tx_outs[1].amount, want)
#         want = bytes.fromhex('1976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac')
#         self.assertEqual(tx.tx_outs[1].script_pubkey.serialize(), want)

#     def test_parse_locktime(self):
#         raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
#         stream = BytesIO(raw_tx)
#         tx = Tx.parse(stream)
#         self.assertEqual(tx.locktime, 410393)

#     def test_fee(self):
#         raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
#         stream = BytesIO(raw_tx)
#         tx = Tx.parse(stream)
#         self.assertEqual(tx.fee(), 40000)
#         raw_tx = bytes.fromhex('010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e148a1fc61c6ed7a069e010000006a47304402204585bcdef85e6b1c6af5c2669d4830ff86e42dd205c0e089bc2a821657e951c002201024a10366077f87d6bce1f7100ad8cfa8a064b39d4e8fe4ea13a7b71aa8180f012102f0da57e85eec2934a82a585ea337ce2f4998b50ae699dd79f5880e253dafafb7feffffffeb8f51f4038dc17e6313cf831d4f02281c2a468bde0fafd37f1bf882729e7fd3000000006a47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937feffffff567bf40595119d1bb8a3037c356efd56170b64cbcc160fb028fa10704b45d775000000006a47304402204c7c7818424c7f7911da6cddc59655a70af1cb5eaf17c69dadbfc74ffa0b662f02207599e08bc8023693ad4e9527dc42c34210f7a7d1d1ddfc8492b654a11e7620a0012102158b46fbdff65d0172b7989aec8850aa0dae49abfb84c81ae6e5b251a58ace5cfeffffffd63a5e6c16e620f86f375925b21cabaf736c779f88fd04dcad51d26690f7f345010000006a47304402200633ea0d3314bea0d95b3cd8dadb2ef79ea8331ffe1e61f762c0f6daea0fabde022029f23b3e9c30f080446150b23852028751635dcee2be669c2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e563ff2722eb4cff0ad6006e86ee20dfe7520d55feffffff0251430f00000000001976a914ab0c0b2e98b1ab6dbf67d4750b0a56244948a87988ac005a6202000000001976a9143c82d7df364eb6c75be8c80df2b3eda8db57397088ac46430600')
#         stream = BytesIO(raw_tx)
#         tx = Tx.parse(stream)
#         self.assertEqual(tx.fee(), 140500)