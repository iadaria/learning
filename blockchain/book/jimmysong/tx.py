from helper import hash256, little_endian_to_int

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
        return cls(version, None, None, None, testnet=testnet)