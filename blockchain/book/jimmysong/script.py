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
        # create a copy as we may need to add to this list if we have a
        # RedeemScript
        cmds = self.cmds[:]
        stack = []
        altstack = []
        while len(cmds) > 0:
            cmd = cmds.pop(0)
            if type(cmd) == int:
                # do what the opcode says
                operation = OP_CODE_FUNCTIONS[cmd]
                if cmd in (99, 100):
                    # op_if/op_notif require the cmds array
                    if not operation(stack, cmds):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (107, 108):
                    # op_toaltstack/op_fromaltstack require the altstack
                    if not operation(stack, altstack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (172, 173, 174, 175):
                    # these are signing operations, they need a sig_hash
                    # to check against
                    if not operation(stack, z):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                else:
                    if not operation(stack):
                        LOGGER.info('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
            else:
                # add the cmd to the stack
                stack.append(cmd)
                if len(cmds) == 3 and cmds[0] == 0xa9 \
                    and type(cmds[1]) == bytes and len(cmds[1]) == 20 \
                    and cmds[2] == 0x87:
                    # we execute the next three opcodes
                    cmds.pop()
                    h160 = cmds.pop()
                    cmds.pop()
                    if not op_hash160(stack):
                        return False
                    stack.append(h160)
                    if not op_equal(stack):
                        return False
                    # final result should be a 1
                    if not op_verify(stack):
                        LOGGER.info('bad p2sh h160')
                        return False
                    # hashes match! now add the RedeemScript
                    redeem_script = encode_varint(len(cmd)) + cmd
                    stream = BytesIO(redeem_script)
                    cmds.extend(Script.parse(stream).cmds)
        if len(stack) == 0:
            return False
        if stack.pop() == b'':
            return False
        return True
