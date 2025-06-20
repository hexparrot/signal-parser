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
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
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
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

    def test_sent_3(self):
        with open("examples/sent_3", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Willy D")
        self.assertEqual(inst.sender.number, "+19876543210")
        self.assertEqual(inst.sender.device, 3)
        self.assertEqual(inst.timing.sender_initiated, 1750266383657)

        self.assertEqual(inst.recipient.number, "+11213430909")
        self.assertEqual(inst.recipient.name, "Mohammed (Ali)")

        self.assertEqual(inst.timing.server_received, 1750266384235)
        self.assertEqual(inst.timing.server_delivered, 1750277517352)
        self.assertEqual(inst.timing.expiration_started, 1750266384022)

        self.assertEqual(inst.body, "for my group play")
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
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
        self.assertEqual(inst.quoted_timestamp, 1750257104156)
        self.assertEqual(inst.quote_author.name, "Chimichanga")
        self.assertEqual(inst.quote_author.number, "+10123456789")
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

    def test_send_attc_1(self):
        with open("examples/sent_attc_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Willy D")
        self.assertEqual(inst.sender.number, "+19876543210")
        self.assertEqual(inst.sender.device, 3)
        self.assertEqual(inst.timing.sender_initiated, 1750279523411)

        self.assertEqual(inst.recipient.number, "+10123456789")
        self.assertEqual(inst.recipient.name, "Chimichanga")

        self.assertEqual(inst.timing.server_received, 1750279526170)
        self.assertEqual(inst.timing.server_delivered, 1750279555712)
        self.assertEqual(inst.timing.expiration_started, 1750279525777)

        self.assertEqual(inst.body, "here you go")
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

        self.assertEqual(inst.attachment[0].content_type, "image/png")
        self.assertIsNone(inst.attachment[0].upload_timestamp)
        self.assertEqual(inst.attachment[0].size, 476939)
        self.assertEqual(inst.attachment[0].id, "g_8PODNoazv-d_BbMFy8.png")
        self.assertEqual(inst.attachment[0].filename, "chars.png")
        self.assertEqual(inst.attachment[0].dimensions, "1122x518")
        self.assertEqual(
            inst.attachment[0].filepath,
            "/home/user/.local/share/signal-cli/attachments/g_8PODNoazv-d_BbMFy8.png",
        )

        self.assertEqual(inst.attachment[1].content_type, "image/jpeg")
        self.assertIsNone(inst.attachment[1].upload_timestamp)
        self.assertEqual(inst.attachment[1].size, 18502)
        self.assertEqual(inst.attachment[1].id, "jPw2mTEdWDJzceFAyq2S.jpg")
        self.assertEqual(inst.attachment[1].filename, "shinobu.jpg")
        self.assertEqual(inst.attachment[1].dimensions, "276x183")
        self.assertEqual(
            inst.attachment[1].filepath,
            "/home/user/.local/share/signal-cli/attachments/jPw2mTEdWDJzceFAyq2S.jpg",
        )

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
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

    def test_recv_quoted_1(self):
        with open("examples/recv_quoted_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Chimichanga")
        self.assertEqual(inst.sender.number, "+10123456789")
        self.assertEqual(inst.sender.device, 2)
        self.assertEqual(inst.timing.sender_initiated, 1750199058670)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertIsNone(inst.recipient.name)

        self.assertEqual(inst.timing.server_received, 1750199061804)
        self.assertEqual(inst.timing.server_delivered, 1750262044366)
        self.assertIsNone(inst.timing.expiration_started)

        self.assertEqual(inst.body, "lets check activity history and logs")
        self.assertEqual(inst.quote, "how can we track this down?")
        self.assertEqual(inst.quoted_timestamp, 1750198952954)
        self.assertEqual(inst.quote_author.name, "Willy D")
        self.assertEqual(inst.quote_author.number, "+19876543210")
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

    def test_recv_attc_1(self):
        with open("examples/recv_attc_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Chimichanga")
        self.assertEqual(inst.sender.number, "+10123456789")
        self.assertEqual(inst.sender.device, 1)
        self.assertEqual(inst.timing.sender_initiated, 1750197565182)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertIsNone(inst.recipient.name)

        self.assertEqual(inst.timing.server_received, 1750197566144)
        self.assertEqual(inst.timing.server_delivered, 1750262044358)
        self.assertIsNone(inst.timing.expiration_started)

        self.assertIsNone(inst.body)
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

        self.assertEqual(inst.attachment[0].content_type, "image/jpeg")
        self.assertEqual(inst.attachment[0].upload_timestamp, 1750197565251)
        self.assertEqual(inst.attachment[0].size, 447806)
        self.assertEqual(inst.attachment[0].id, "RDJEm5uYXHmlGrcAIMrn.jpeg")
        self.assertEqual(inst.attachment[0].filename, "signal-2025-06-17-175925.jpeg")
        self.assertEqual(inst.attachment[0].dimensions, "1323x1995")
        self.assertEqual(
            inst.attachment[0].filepath,
            "/home/user/.local/share/signal-cli/attachments/RDJEm5uYXHmlGrcAIMrn.jpeg",
        )

    def test_recv_attc_2(self):
        with open("examples/recv_attc_2", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Chimichanga")
        self.assertEqual(inst.sender.number, "+10123456789")
        self.assertEqual(inst.sender.device, 1)
        self.assertEqual(inst.timing.sender_initiated, 1750277331288)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertIsNone(inst.recipient.name)

        self.assertEqual(inst.timing.server_received, 1750277332528)
        self.assertEqual(inst.timing.server_delivered, 1750277518230)
        self.assertIsNone(inst.timing.expiration_started)

        self.assertIsNone(inst.body)
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

        self.assertEqual(inst.attachment[0].content_type, "image/jpeg")
        self.assertEqual(inst.attachment[0].upload_timestamp, 1750277331400)
        self.assertEqual(inst.attachment[0].size, 558499)
        self.assertEqual(inst.attachment[0].id, "Yfpc46_PIdBgR6fYw3fB.jpeg")
        self.assertEqual(inst.attachment[0].filename, "signal-2025-06-18-160851.jpeg")
        self.assertEqual(inst.attachment[0].dimensions, "1835x2048")
        self.assertEqual(
            inst.attachment[0].filepath,
            "/home/user/.local/share/signal-cli/attachments/Yfpc46_PIdBgR6fYw3fB.jpeg",
        )

        self.assertEqual(inst.attachment[1].content_type, "image/jpeg")
        self.assertEqual(inst.attachment[1].upload_timestamp, 1750277331399)
        self.assertEqual(inst.attachment[1].size, 336253)
        self.assertEqual(inst.attachment[1].id, "O97z7JNnftBDSZkWqKfK.jpg")
        self.assertEqual(inst.attachment[1].filename, "IMG_1563.jpg")
        self.assertEqual(inst.attachment[1].dimensions, "1165x2048")
        self.assertEqual(
            inst.attachment[1].filepath,
            "/home/user/.local/share/signal-cli/attachments/O97z7JNnftBDSZkWqKfK.jpg",
        )

        self.assertEqual(inst.attachment[2].content_type, "image/jpeg")
        self.assertEqual(inst.attachment[2].upload_timestamp, 1750277331386)
        self.assertEqual(inst.attachment[2].size, 364181)
        self.assertEqual(inst.attachment[2].id, "A6Cp_O_3ScdDCv5F2mLR.jpg")
        self.assertEqual(inst.attachment[2].filename, "IMG_1567.jpg")
        self.assertEqual(inst.attachment[2].dimensions, "2048x1224")
        self.assertEqual(
            inst.attachment[2].filepath,
            "/home/user/.local/share/signal-cli/attachments/A6Cp_O_3ScdDCv5F2mLR.jpg",
        )

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

        self.assertIsNone(inst.body)
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
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

        self.assertIsNone(inst.body)
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
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

        self.assertIsNone(inst.body)
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, True)
        self.assertTrue(1750198595726 in inst.confirmed)
        self.assertTrue(1750198536938 in inst.confirmed)
        self.assertTrue(1750198522423 in inst.confirmed)
        self.assertEqual(len(inst.confirmed), 3)

    def test_receipt_sync_2(self):
        with open("examples/sync_2", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Willy D")
        self.assertEqual(inst.sender.number, "+19876543210")
        self.assertEqual(inst.sender.device, 1)
        self.assertEqual(inst.timing.sender_initiated, 1750208532150)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertEqual(inst.recipient.name, "Willy D")

        self.assertEqual(inst.timing.server_received, 1750208532068)
        self.assertEqual(inst.timing.server_delivered, 1750262044376)
        self.assertIsNone(inst.timing.expiration_started)

        self.assertIsNone(inst.body)
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, True)
        self.assertTrue(1750208530522 in inst.confirmed)
        self.assertEqual(len(inst.confirmed), 1)

    def test_call_1(self):
        with open("examples/call_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Chimichanga")
        self.assertEqual(inst.sender.number, "+10123456789")
        self.assertEqual(inst.sender.device, 2)
        self.assertEqual(inst.timing.sender_initiated, 1750394977259)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertIsNone(inst.recipient.name)
        self.assertEqual(inst.recipient.device, 1)

        self.assertEqual(inst.timing.server_received, 1750394977418)
        self.assertEqual(inst.timing.server_delivered, 1750398074057)
        self.assertIsNone(inst.timing.expiration_started)

        self.assertIsNone(inst.body)
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(inst.call_receipt, True)
        self.assertEqual(inst.answer_receipt, True)
        self.assertEqual(inst.ice_receipt, False)
        self.assertEqual(len(inst.confirmed), 0)

    def test_call_2(self):
        with open("examples/call_2", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Chimichanga")
        self.assertEqual(inst.sender.number, "+10123456789")
        self.assertEqual(inst.sender.device, 2)
        self.assertEqual(inst.timing.sender_initiated, 1750394977288)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertIsNone(inst.recipient.name)
        self.assertEqual(inst.recipient.device, 1)

        self.assertEqual(inst.timing.server_received, 1750394977445)
        self.assertEqual(inst.timing.server_delivered, 1750398074118)
        self.assertIsNone(inst.timing.expiration_started)

        self.assertIsNone(inst.body)
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(inst.call_receipt, True)
        self.assertEqual(inst.ice_receipt, True)
        self.assertTrue(107 in inst.confirmed)
        self.assertTrue(134 in inst.confirmed)
        self.assertTrue(132 in inst.confirmed)
        self.assertTrue(142 in inst.confirmed)
        self.assertTrue(166 in inst.confirmed)
        self.assertTrue(165 in inst.confirmed)
        self.assertTrue(142 in inst.confirmed)
        self.assertEqual(len(inst.confirmed), 7)

    def test_call_3(self):
        with open("examples/call_3", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Chimichanga")
        self.assertEqual(inst.sender.number, "+10123456789")
        self.assertEqual(inst.sender.device, 1)
        self.assertEqual(inst.timing.sender_initiated, 1750395271133)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertIsNone(inst.recipient.name)
        self.assertIsNone(inst.recipient.device)

        self.assertEqual(inst.timing.server_received, 1750395271245)
        self.assertEqual(inst.timing.server_delivered, 1750398074243)
        self.assertIsNone(inst.timing.expiration_started)

        self.assertIsNone(inst.body)
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(inst.call_receipt, True)
        self.assertEqual(inst.ice_receipt, False)
        self.assertEqual(inst.hangup_receipt, True)
        self.assertEqual(len(inst.confirmed), 0)

    def test_call_4(self):
        with open("examples/call_4", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(inst.sender.name, "Chimichanga")
        self.assertEqual(inst.sender.number, "+10123456789")
        self.assertEqual(inst.sender.device, 1)
        self.assertEqual(inst.timing.sender_initiated, 1750395268304)

        self.assertEqual(inst.recipient.number, "+19876543210")
        self.assertIsNone(inst.recipient.name)
        self.assertIsNone(inst.recipient.device)

        self.assertEqual(inst.timing.server_received, 1750395268328)
        self.assertEqual(inst.timing.server_delivered, 1750398074182)
        self.assertIsNone(inst.timing.expiration_started)

        self.assertIsNone(inst.body)
        self.assertIsNone(inst.quote)
        self.assertIsNone(inst.quoted_timestamp)
        self.assertIsNone(inst.quote_author.name)
        self.assertIsNone(inst.quote_author.number)
        self.assertEqual(inst.delivery_receipt, False)
        self.assertEqual(inst.read_receipt, False)
        self.assertEqual(inst.sync_receipt, False)
        self.assertEqual(inst.call_receipt, True)
        self.assertEqual(inst.ice_receipt, False)
        self.assertEqual(inst.hangup_receipt, False)
        self.assertEqual(inst.offer_receipt, True)
        self.assertEqual(len(inst.confirmed), 0)

    def test_sent_1_str(self):
        with open("examples/sent_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Willy D (+19876543210) [dev 3]
To: Chimichanga (+10123456789)
At: 2025-06-17T21:48:08.6790Z
Message: HELLO!""",
        )

    def test_sent_attc_1_str(self):
        with open("examples/sent_attc_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Willy D (+19876543210) [dev 3]
To: Chimichanga (+10123456789)
At: 2025-06-18T20:45:23.4110Z
Attachment: chars.png (476939 bytes) [image/png]
Attachment: shinobu.jpg (18502 bytes) [image/jpeg]
Message: here you go""",
        )

    def test_sent_quoted_1_str(self):
        with open("examples/sent_quoted_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Willy D (+19876543210) [dev 3]
To: Chimichanga (+10123456789)
At: 2025-06-18T14:42:17.0230Z
Quote: Chimichanga said "how are you today?"
Message: great!""",
        )

    def test_recv_1_str(self):
        with open("examples/recv_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Chimichanga (+10123456789) [dev 2]
To: None (+19876543210)
At: 2025-06-17T21:48:57.8720Z
Message: dinnertime please""",
        )

    def test_recv_quoted_1_str(self):
        with open("examples/recv_quoted_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Chimichanga (+10123456789) [dev 2]
To: None (+19876543210)
At: 2025-06-17T22:24:18.6700Z
Quote: Willy D said "how can we track this down?"
Message: lets check activity history and logs""",
        )

    def test_receipt_delivery_1_str(self):
        with open("examples/delivery_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Chimichanga (+10123456789) [dev 2]
To: None (+19876543210)
At: 2025-06-17T21:48:06.5760Z
Delivery: 1750196888679""",
        )

    def test_receipt_read_1_str(self):
        with open("examples/read_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Chimichanga (+10123456789) [dev 2]
To: None (+19876543210)
At: 2025-06-17T21:48:21.1660Z
Read: 1750196898889
Read: 1750196888679""",
        )

    def test_receipt_sync_1_str(self):
        with open("examples/sync_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Willy D (+19876543210) [dev 3]
To: Willy D (+19876543210)
At: 2025-06-17T22:19:38.3630Z
Sync: 1750198595726
Sync: 1750198536938
Sync: 1750198522423""",
        )

    def test_receipt_call_1_str(self):
        with open("examples/call_1", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Chimichanga (+10123456789) [dev 2]
To: None (+19876543210) [dev 1]
At: 2025-06-20T04:49:37.2590Z
Call: ANSWERED""",
        )

    def test_receipt_call_2_str(self):
        with open("examples/call_2", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Chimichanga (+10123456789) [dev 2]
To: None (+19876543210) [dev 1]
At: 2025-06-20T04:49:37.2880Z
Call: ONGOING""",
        )

    def test_receipt_call_3_str(self):
        with open("examples/call_3", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Chimichanga (+10123456789) [dev 1]
To: None (+19876543210)
At: 2025-06-20T04:54:31.1330Z
Call: ENDED""",
        )

    def test_receipt_call_4_str(self):
        with open("examples/call_4", "r") as f:
            lines = f.readlines()

        inst = EnvelopeParser.read(lines)

        self.assertEqual(
            str(inst),
            """From: Chimichanga (+10123456789) [dev 1]
To: None (+19876543210)
At: 2025-06-20T04:54:28.3040Z
Call: OFFERING""",
        )


if __name__ == "__main__":
    unittest.main()
