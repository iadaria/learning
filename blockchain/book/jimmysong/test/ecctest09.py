from io import BytesIO
from script import Script
from helper import little_endian_to_int
import unittest


class ECCTest09(unittest.TestCase):
    def exercise_1(self):
        stream = BytesIO(bytes.fromhex('4d04ffff001d0104455468652054696d6573203033\
2f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64\
206261696c6f757420666f722062616e6b73'))
        s = Script.parse(stream)
        print(s.cmds[2])

    # синтаксический анализ высоты блока
    def example_2(self):
        stream = BytesIO(bytes.fromhex('5e03d71b07254d696e656420627920416e74506f6f\
6c20626a31312f4542312f4144362f43205914293101fabe6d6d678e2c8c34afc36896e7d94028\
24ed38e856676ee94bfdb0c6c4bcd8b2e5666a0400000000000000c7270000a5e00e00'))
        script_sig = Script.parse(stream)
        print(little_endian_to_int(script_sig.cmds[0]))