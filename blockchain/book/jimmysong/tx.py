from helper import hash256, little_endian_to_int, read_varint
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