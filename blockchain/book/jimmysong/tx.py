from io import BytesIO
import json
import requests
from helper import hash256, little_endian_to_int, read_varint, encode_varint, int_to_little_endian
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

class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
            self.sequence = sequence

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

class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script = script_pubkey

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_publickey)

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
            url = '{}/tx/{}.hex'.format(cls.get_url(testnet), tx_id)
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError('unexpected response: {}', format(response.text))
            if raw[4] == 0:
                raw = raw[:4] + raw[:6]
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
            if tx.id() != tx_id:
                raise ValueError('not hte same id: {} vs {}'.format(tx.id(), tx_id))
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
        