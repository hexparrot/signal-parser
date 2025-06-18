class Contact:
    def __init__(self):
        self.number = None
        self.name = None
        self.device = None


class Timestamps:
    def __init__(self):
        self.sender_initiated = None
        self.server_received = None
        self.server_delivered = None
        self.expiration_started = None


class EnvelopeParser:
    def __init__(self):
        self.sender = Contact()
        self.recipient = Contact()
        self.timing = Timestamps()
        self.body = None
        self.quote = None
        self.delivery_receipt = False
        self.read_receipt = False
        self.sync_receipt = False
        self.confirmed = []

    @staticmethod
    def read(envelope_lines):
        import shlex
        from itertools import takewhile

        retval = EnvelopeParser()
        is_reading = False

        def parse_line(oneline):
            nonlocal is_reading

            if is_reading is True:
                if oneline == "With profile key":
                    is_reading = False
                else:
                    retval.body = retval.body + "\n" + oneline
            elif oneline.startswith("Envelope from:"):
                all_words = shlex.split(oneline)

                sender_name = list(
                    takewhile(lambda x: "“" in x or "”" in x, all_words[2:])
                )
                sender_number = all_words[
                    2 + len(sender_name) : 2 + len(sender_name) + 1
                ]

                device_offset = 2 + len(sender_name) + 2

                retval.sender.name = " ".join(sender_name)[1:-1]
                retval.sender.number = sender_number[0]
                retval.sender.device = int(all_words[device_offset].strip(")"))

                retval.recipient.number = all_words[-1]
            elif oneline.startswith("Timestamp:"):
                retval.timing.sender_initiated = int(oneline.split(" ")[1])
            elif oneline.startswith("Expiration started at:"):
                retval.timing.expiration_started = int(oneline.split(" ")[3])
            elif oneline.startswith("Server timestamps:"):
                retval.timing.server_received = int(
                    oneline.split("received: ")[1].split(" ")[0]
                )
                retval.timing.server_delivered = int(
                    oneline.split("delivered: ")[1].split(" ")[0]
                )
            elif oneline.startswith("To:"):
                all_words = shlex.split(oneline)

                sender_name = list(
                    takewhile(lambda x: "“" in x or "”" in x, all_words[1:])
                )
                retval.recipient.name = sender_name[0][1:-1]
                retval.recipient.number = all_words[2]  # overwrite envelope value
            elif oneline.startswith("Body:"):
                retval.body = oneline[6:]
                is_reading = True
            elif oneline.startswith("Text:"):
                retval.quote = oneline[6:]
            elif oneline == "Is delivery receipt":
                retval.delivery_receipt = True
                retval.body = f"{retval.sender.name} device {retval.sender.device} confirming delivery."
            elif oneline == "Is read receipt":
                retval.read_receipt = True
                retval.body = f"{retval.sender.name} device {retval.sender.device} confirming message read."
            elif oneline == "Received sync read messages list":
                retval.sync_receipt = True
                retval.recipient.name = retval.sender.name
                retval.body = f"{retval.sender.name} device {retval.sender.device} received message sync."
            elif oneline.startswith("-") and retval.delivery_receipt:
                retval.confirmed.append(int(oneline.split(" ")[1]))
            elif oneline.startswith("-") and retval.read_receipt:
                retval.confirmed.append(int(oneline.split(" ")[1]))
            elif oneline.startswith("- From:") and retval.sync_receipt:
                retval.confirmed.append(int(oneline.split(" ")[6]))

        for line in envelope_lines:
            parse_line(line.strip())

        return retval
