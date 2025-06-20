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


class Attachment:
    def __init__(self):
        self.content_type = None
        self.upload_timestamp = None
        self.size = None
        self.id = None
        self.filename = None
        self.filepath = None


class Receipt:
    def __init__(self):
        self.delivery = False
        self.read = False
        self.sync = False
        self.call = False
        self.answer = False
        self.hangup = False
        self.offer = False
        self.ice = False


class EnvelopeParser:
    def __init__(self):
        self.sender = Contact()
        self.recipient = Contact()
        self.quote_author = Contact()
        self.receipt = Receipt()
        self.attachment = []
        self.timing = Timestamps()
        self.body = None
        self.quote = None
        self.quoted_timestamp = None
        self.confirmed = []

    def __str__(self):
        from datetime import datetime, timezone

        dt = datetime.fromtimestamp(
            self.timing.sender_initiated / 1000, tz=timezone.utc
        )
        formatted_string = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3] + "Z"

        retval = f"""From: {self.sender.name} ({self.sender.number}) [dev {self.sender.device}]"""

        if self.receipt.call:
            if self.receipt.answer:
                retval += f"""\nTo: {self.recipient.name} ({self.recipient.number}) [dev {self.recipient.device}]"""
            elif self.receipt.ice:
                retval += f"""\nTo: {self.recipient.name} ({self.recipient.number}) [dev {self.recipient.device}]"""
            elif self.receipt.offer:
                retval += f"""\nTo: {self.recipient.name} ({self.recipient.number})"""
            elif self.receipt.hangup:
                retval += f"""\nTo: {self.recipient.name} ({self.recipient.number})"""
            else:
                retval += f"""\nTo: {self.recipient.name} ({self.recipient.number})"""
        else:
            retval += f"""\nTo: {self.recipient.name} ({self.recipient.number})"""

        retval += f"""\nAt: {formatted_string}"""

        if self.quote:
            retval += f'''\nQuote: {self.quote_author.name} said \"{self.quote}\"'''

        for i in self.attachment:
            retval += (
                f"""\nAttachment: {i.filename} ({i.size} bytes) [{i.content_type}]"""
            )

        if self.body:
            retval += f"""\nMessage: {self.body}"""

        if self.receipt.delivery:
            for drts in self.confirmed:
                retval += f"\nDelivery: {drts}"

        if self.receipt.read:
            for rrts in self.confirmed:
                retval += f"\nRead: {rrts}"

        if self.receipt.sync:
            for srts in self.confirmed:
                retval += f"\nSync: {srts}"

        if self.receipt.call:
            if self.receipt.ice:
                retval += f"\nCall: ONGOING"
            elif self.receipt.offer:
                retval += f"\nCall: OFFERING"
            elif self.receipt.hangup:
                retval += f"\nCall: ENDED"
            else:
                retval += f"\nCall: ANSWERED"

        return retval

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
            elif oneline.startswith("- Attachment:"):
                retval.attachment.append(Attachment())
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
                retval.recipient.name = " ".join(sender_name)[1:-1]
                retval.recipient.number = all_words[-1]  # overwrite envelope value
            elif oneline.startswith("Body:"):
                retval.body = oneline[6:]
                is_reading = True
            elif oneline.startswith("Id:"):
                try:
                    retval.quoted_timestamp = int(oneline[4:])
                except ValueError:
                    retval.attachment[-1].id = oneline[4:]
            elif oneline.startswith("Content-Type:"):
                retval.attachment[-1].content_type = oneline.split(" ")[1]
            elif oneline.startswith("Filename:"):
                retval.attachment[-1].filename = oneline.split(" ")[1]
            elif oneline.startswith("Stored plaintext in:"):
                retval.attachment[-1].filepath = oneline[21:]
            elif oneline.startswith("Upload timestamp:"):
                retval.attachment[-1].upload_timestamp = int(oneline[18:].split(" ")[0])
            elif oneline.startswith("Size:"):
                retval.attachment[-1].size = int(oneline[6:].split(" ")[0])
            elif oneline.startswith("Dimensions:"):
                retval.attachment[-1].dimensions = oneline[12:]
            elif oneline.startswith("Author:"):
                all_words = shlex.split(oneline)

                sender_name = list(
                    takewhile(lambda x: "“" in x or "”" in x, all_words[1:])
                )
                retval.quote_author.name = " ".join(sender_name)[1:-1]
                retval.quote_author.number = " ".join(all_words).split(" ")[-1]
            elif oneline.startswith("Text:"):
                retval.quote = oneline[6:]
            elif oneline.startswith("Destination device id:"):
                retval.recipient.device = int(oneline.split(": ")[1])
            elif oneline == "Is delivery receipt":
                retval.receipt.delivery = True
            elif oneline == "Is read receipt":
                retval.receipt.read = True
            elif oneline == "Received a call message":
                retval.receipt.call = True
            elif oneline == "Ice update messages:":
                retval.receipt.ice = True
            elif oneline.startswith("Answer message:"):
                retval.receipt.answer = True
            elif oneline.startswith("Hangup message:"):
                retval.receipt.hangup = True
            elif oneline.startswith("Offer message:"):
                retval.receipt.offer = True
            elif oneline == "Received sync read messages list":
                retval.receipt.sync = True
                retval.recipient.name = retval.sender.name
            elif oneline.startswith("-") and retval.receipt.delivery:
                retval.confirmed.append(int(oneline.split(" ")[1]))
            elif oneline.startswith("-") and retval.receipt.read:
                retval.confirmed.append(int(oneline.split(" ")[1]))
            elif oneline.startswith("-") and retval.receipt.ice:
                retval.confirmed.append(int(oneline.split(" ")[4]))
            elif oneline.startswith("- From:") and retval.receipt.sync:
                all_words = shlex.split(oneline)

                sender_name = list(
                    takewhile(lambda x: "“" in x or "”" in x, all_words[2:])
                )
                timestamp_offset = 2 + len(sender_name) + 3
                retval.confirmed.append(int(all_words[timestamp_offset]))

        for line in envelope_lines:
            parse_line(line.strip())

        return retval


def read_stanzas(filename):
    with open(filename, "r") as file:
        lines = [line.rstrip() for line in file.readlines()]

    stanzas = []
    current_stanza = []

    for line in lines:
        if line.startswith("Envelope") and current_stanza:
            stanzas.append(current_stanza)
            current_stanza = [line]
        elif line.startswith("Envelope"):
            current_stanza = [line]
        else:
            current_stanza.append(line)

    if current_stanza:
        stanzas.append(current_stanza)

    return stanzas


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        stanza_count = 0
        for stanza in read_stanzas(filename):
            stanza_count += 1
            print(f"=== Envelope {stanza_count} ===")
            out = EnvelopeParser.read(stanza)
            print(out)
            print("-" * 50)

        print(f"Processed {stanza_count} stanzas total.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)
