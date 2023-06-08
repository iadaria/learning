from unittest import TestCase
from io import BytesIO

class Script:
    def __init__(self):
        self.init = True

    @classmethod
    def parse(cls, stream):
        cmds = []
        return cls()

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