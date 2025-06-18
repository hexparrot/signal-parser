import os
import unittest
from parser import EnvelopeParser


class TestSignalParser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sent_1(self):
        with open("examples/sent_1", "r") as f:
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
        self.assertEqual(inst.timing.expiration_started, 1750196889007)

        self.assertEqual(inst.body, "HELLO!")
        self.assertIsNone(inst.quote)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

    def test_sent_2(self):
        with open("examples/sent_2", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Willy D")
        self.assertEqual(inst.sender.number, "+19876543210")
        self.assertEqual(inst.sender.device, 3)
        self.assertEqual(inst.timing.sender_initiated, 1750197162897)

        self.assertEqual(inst.recipient.number, "+10123456789")
        self.assertEqual(inst.recipient.name, "Chimichanga")

        self.assertEqual(inst.timing.server_received, 1750197163285)
        self.assertEqual(inst.timing.server_delivered, 1750197168902)
        self.assertEqual(inst.timing.expiration_started, 1750197163130)

        self.assertEqual(inst.body, "lets\n\ndo\n\nthis")
        self.assertIsNone(inst.quote)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

    def test_sent_quoted_1(self):
        with open("examples/sent_quoted_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Willy D")
        self.assertEqual(inst.sender.number, "+19876543210")
        self.assertEqual(inst.sender.device, 3)
        self.assertEqual(inst.timing.sender_initiated, 1750257737023)

        self.assertEqual(inst.recipient.number, "+10123456789")
        self.assertEqual(inst.recipient.name, "Chimichanga")

        self.assertEqual(inst.timing.server_received, 1750257737693)
        self.assertEqual(inst.timing.server_delivered, 1750262048547)
        self.assertEqual(inst.timing.expiration_started, 1750257737286)

        self.assertEqual(inst.body, "great!")
        self.assertEqual(inst.quote, "how are you today?")
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

    def test_recv_1(self):
        with open("examples/recv_1", "r") as f:
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
        self.assertIsNone(inst.timing.expiration_started)

        self.assertEqual(inst.body, "dinnertime please")
        self.assertIsNone(inst.quote)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

    def test_receipt_delivery_1(self):
        with open("examples/delivery_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Chimichanga")
        self.assertEqual(inst.sender.number, "+10123456789")
        self.assertEqual(inst.sender.device, 2)
        self.assertEqual(inst.timing.sender_initiated, 1750196886576)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertIsNone(inst.recipient.name)

        self.assertEqual(inst.timing.server_received, 1750196889591)
        self.assertEqual(inst.timing.server_delivered, 1750196935451)
        self.assertIsNone(inst.timing.expiration_started)

        self.assertEqual(inst.body, "Chimichanga device 2 confirming delivery.")
        self.assertIsNone(inst.quote)
        self.assertEqual(inst.delivery_receipt, True)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertTrue(1750196888679 in inst.confirmed)

    def test_receipt_read_1(self):
        with open("examples/read_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Chimichanga")
        self.assertEqual(inst.sender.number, "+10123456789")
        self.assertEqual(inst.sender.device, 2)
        self.assertEqual(inst.timing.sender_initiated, 1750196901166)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertIsNone(inst.recipient.name)

        self.assertEqual(inst.timing.server_received, 1750196904194)
        self.assertEqual(inst.timing.server_delivered, 1750196935451)
        self.assertIsNone(inst.timing.expiration_started)

        self.assertEqual(inst.body, "Chimichanga device 2 confirming message read.")
        self.assertIsNone(inst.quote)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, True)
        self.assertEqual(inst.sync_receipt, False)
        self.assertTrue(1750196898889 in inst.confirmed)
        self.assertTrue(1750196888679 in inst.confirmed)
        self.assertEqual(len(inst.confirmed), 2)

    def test_receipt_sync_1(self):
        with open("examples/sync_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Willy D")
        self.assertEqual(inst.sender.number, "+19876543210")
        self.assertEqual(inst.sender.device, 3)
        self.assertEqual(inst.timing.sender_initiated, 1750198778363)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertEqual(inst.recipient.name, "Willy D")

        self.assertEqual(inst.timing.server_received, 1750198778607)
        self.assertEqual(inst.timing.server_delivered, 1750262044363)
        self.assertIsNone(inst.timing.expiration_started)

        self.assertEqual(inst.body, "Willy D device 3 received message sync.")
        self.assertIsNone(inst.quote)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, True)
        self.assertTrue(1750198595726 in inst.confirmed)
        self.assertTrue(1750198536938 in inst.confirmed)
        self.assertTrue(1750198522423 in inst.confirmed)
        self.assertEqual(len(inst.confirmed), 3)


if __name__ == "__main__":
    unittest.main()
