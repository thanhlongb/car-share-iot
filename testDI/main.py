from container import Readers, Clients, Configs
from agentpi.menu import *

if __name__ == "__main__":
    Configs.config.override({
        "domain_name": "imap.gmail.com",
        "email_address": "YOUR_EMAIL_ADDRESS",
        "password": "YOUR_PASSWORD",
        "mailbox": "INBOX"
    })
    email_reader = Readers.email_reader()
    email_reader.read()