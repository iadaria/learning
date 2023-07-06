from unittest import TestCase
from io import BytesIO
from helper import read_varint, little_endian_to_int

class Script:
    # cmds - Каждая команда является исполняемым кодом или элементов размещаемым в стеке
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds

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

    @classmethod
    def raw_serialize(self):
        result = b''
        for cmd in self.cmds:
            # Если команда - целое число, значит, это код операции
            if type(cmd) == int:


    @classmethod
    def serialize(cls):
        return cls()

class ScriptTest(TestCase):
    # Преобразование объекта типа Script из шестнадцатеричной формы в форму Python
    def test_5_1(self):
        script_hex = ('6b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
        stream = BytesIO(bytes.fromhex(script_hex))
        script_sig = Script.parse(stream)
        print(script_sig)