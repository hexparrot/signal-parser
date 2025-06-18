import os
import unittest
from parser import EnvelopeParser


class TestSignalParser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_env1(self):
        with open("examples/env1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Willy D")
        self.assertEqual(inst.sender.number, "+19876543210")
        self.assertEqual(inst.sender.device, 3)
        self.assertEqual(inst.timing.sender_initiated, 1750196888679)

        self.assertEqual(inst.recipient.number, "+10123456789")
        self.assertEqual(inst.recipient.name, "Chimichanga")

        self.assertEqual(inst.timing.server_received, 1750196889148)
        self.assertEqual(inst.timing.server_delivered, 1750196935451)
        self.assertEqual(inst.timing.recipient_read, 1750196889007)

        self.assertEqual(inst.body, "HELLO!")

    def test_read_env2(self):
        with open("examples/env2", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Chimichanga")
        self.assertEqual(inst.sender.number, "+10123456789")
        self.assertEqual(inst.sender.device, 2)
        self.assertEqual(inst.timing.sender_initiated, 1750196937872)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertIsNone(inst.recipient.name)

        self.assertEqual(inst.timing.server_received, 1750196940946)
        self.assertEqual(inst.timing.server_delivered, 1750197168902)
        self.assertIsNone(inst.timing.recipient_read)

        self.assertEqual(inst.body, "dinnertime please")


if __name__ == "__main__":
    unittest.main()
