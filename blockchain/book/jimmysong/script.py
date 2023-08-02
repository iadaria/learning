from helper import read_varint, little_endian_to_int, int_to_little_endian, encode_varint
from logging import getLogger

from op import (
    OP_CODE_FUNCTIONS,
    OP_CODE_NAMES
)

LOGGER = getLogger(__name__)

class Script:
    # cmds - Каждая команда является исполняемым кодом или элементов размещаемым в стеке
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds

    def __repr__(self):
        result = []
        for cmd in self.cmds:
            if isinstance(cmd, int):
                if OP_CODE_NAMES.get(cmd):
                    name = OP_CODE_NAMES.get(cmd)
                else:
                    name = 'OP_[{}]'.format(cmd)
                result.append(name)
            else:
                result.append(cmd.hex())
        return ' '.join(result)

    @classmethod
    def parse(cls, stream):
        # Сериализация сценария всегда начинается с длины всего сценария
        length = read_varint(stream)
        cmds = []
        count = 0
        while count < length: # до тех пор пока не обработаем все байты
            current = stream.read(1) # в этом байте опред. код операции или элемента
            count += 1
            current_byte = current[0] # байт преобразуется в целое число
            # для числа в пределах от 1 до 75 известно, что следующие n-байтов содержит элемент
            if current_byte >= 1 and current_byte <= 75:
                n = current_byte
                cmds.append(stream.read(n))
                count += n
            # = 76, выполняем операцию OP_PUSHDATA1,
            # а в след байте читаем сколько байтов еще прочитать
            elif current_byte == 76:
                data_length = little_endian_to_int(stream.read(1))
                cmds.append(stream.read(data_length))
                count += data_length + 1
            elif current_byte == 77:
                data_length = little_endian_to_int(stream.read(2))
                cmds.append(stream.read(data_length))
                count += data_length + 2
            else:
                op_code = current_byte # получен код операции который сохраняется
                cmds.append(op_code)
        if count != length:
            raise SyntaxError('parsing script failed')
        return cls(cmds)
    
    # Преобразуем 20-байтовый хеш-код в сценарий ScriptPubKey.
    # 0x76=OP_DUP, 0xa9=OP_HASH160, h160=20-байтовый элемент, 0x88=OP_EQUALVERIFY, 0xac=OP_CHECKSIG
    @classmethod
    def p2pkh_script(cls, h160):
        '''Принимаем хеш-код hash160 и возвращаем сценарий ScriptPubKey для p2pkh'''
        return cls([0x76, 0xa9, h160, 0x88, 0xac])

    def raw_serialize(self):
        # initialize what we'll send back
        result = b''
        # go through each cmd
        for cmd in self.cmds:
            # if the cmd is an integer, it's an opcode
            if type(cmd) == int:
                # turn the cmd into a single byte integer using int_to_little_endian
                result += int_to_little_endian(cmd, 1)
            else:
                # otherwise, this is an element
                # get the length in bytes
                length = len(cmd)
                # for large lengths, we have to use a pushdata opcode
                if length < 75:
                    # turn the length into a single byte integer
                    result += int_to_little_endian(length, 1)
                elif length > 75 and length < 0x100:
                    # 76 is pushdata1
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                elif length >= 0x100 and length <= 520:
                    # 77 is pushdata2
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                else:
                    raise ValueError('too long an cmd')
                result += cmd
        return result

    def serialize(self):
        result = self.raw_serialize()
        total = len(result)
        return encode_varint(total) + result

    def __add__(self, other):
        return Script(self.cmds + other.cmds)
    
    def logger(self, cmd):
        LOGGER.info('bad op: {}'. format(OP_CODE_NAMES[cmd]))

    def evaluate(self, z):
        cmds = self.cmds[:] # сделаем копию списка команд, тк он изменится
        stack = []
        altstack = []
        while len(cmds) > 0:
            cmd = cmds.pop(0)
            if isinstance(cmd, int):
                operation = OP_CODE_FUNCTIONS[cmd]
                if cmd in (99, 100):
                    if not operation(stack, cmds):
                        self.logger(cmd)
                        return False
                elif cmd in (107, 108):
                    if not operation(stack,  altstack):
                        self.logger(cmd)
                        return False
                elif cmd in (172, 173, 174, 175):
                    if not operation(stack, z):
                        self.logger(cmd)
                        return False
                else:
                    if not operation(stack):
                        self.logger(cmd)
                        return False
            else:
                # Если команда не является кодом операции, то она является элементом
                # И этот элемент размещается в стеке
                stack.append(cmd)
        if len(stack) == 0:
            return False
        if stack.pop() == b'':
            return False
        return True
# class ScriptTest(TestCase):
#     # Преобразование объекта типа Script из шестнадцатеричной формы в форму Python
#     def test_5_1(self):
#         script_hex = ('6b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
#         stream = BytesIO(bytes.fromhex(script_hex))
#         script_sig = Script.parse(stream)
#         print(script_sig)