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
        self.recipient_read = None


class EnvelopeParser:
    def __init__(self):
        self.sender = Contact()
        self.recipient = Contact()
        self.timing = Timestamps()
        self.body = ""

    @staticmethod
    def read(envelope_lines):
        import shlex
        from itertools import takewhile

        retval = EnvelopeParser()

        def parse_line(oneline):
            if oneline.startswith("Envelope from:"):
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
                retval.timing.recipient_read = int(oneline.split(" ")[3])
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
            elif oneline.startswith("Body:"):
                retval.body = oneline[6:]

        for line in envelope_lines:
            parse_line(line.strip())

        return retval
