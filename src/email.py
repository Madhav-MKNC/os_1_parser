import re 

from src.utils import Utils

class Email:

    def __init__(self):
        self.utility = Utils()

    def extract_and_update_email(self, address_obj):
        address_string = address_obj.address
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", address_string)
        if len(emails) > 1:
            for email in emails:
                address_obj.address = address_obj.address.replace(email, "").strip()
            address_obj.address = self.utility.text_cleaner(address_obj.address)
            address_obj.email = " , ".join(emails)

        elif len(emails) > 0:
            email = emails[0]
            address_obj.address = address_obj.address.replace(email, "").strip()
            address_obj.address = self.utility.text_cleaner(address_obj.address)
            address_obj.email = email

        return address_obj

    
    def update_emails(self, address_obj):
        emails = list(set(re.findall(r'\*\*(.*?)\*\*', address_obj.address)))

        if emails is not None and len(emails) > 0:
            if len(emails) > 1:
                for email in emails:
                    address_obj.address = address_obj.address.replace(email, "").strip()
                address_obj.address = self.utility.text_cleaner(address_obj.address)
                address_obj.email = " , ".join(emails)

            elif len(emails) > 0:
                email = emails[0]
                address_obj.address = address_obj.address.replace(email, "").strip()
                address_obj.address = self.utility.text_cleaner(address_obj.address)
                address_obj.email = email

            return address_obj
