# Extract, collapse and pad phone numbers and pincode

import re


class NumbersHandler:
    def __init__(self):
        pass

    def is_valid_phone_number_or_valid_pin(self, inp):
        try:
            if len(str(int(inp))) == 10 or len(inp) == 6:
                return True
        except:
            pass 
        return False

    def process_numbers(self, address_string, address_obj):
        return address_string
        text = address_obj.address
        old_text = text
        pad_char = "*"
        phone_nums = []
        faulty_nums = []
        expected_chars = [" ", "-", "_"]
        phone_num = ""

        for char in str("#" + text + "#"): # temp padding with "#" for inclusivity of corner digits (if there).
            if char.isdigit():
                phone_num += char
                phone_num = str(int(phone_num)) # For removing preceding 0's
            elif char in expected_chars: continue
            else:
                if phone_num:
                    if len(phone_num) == 10: phone_nums.append(phone_num)
                    elif len(phone_num) == 12 and phone_num[:2] == "91":
                        if len(str(int(phone_num[2:]))) == 10: phone_nums.append(phone_num[2:])
                        else: faulty_nums.append(str(int(phone_num[2:])))
                    else: faulty_nums.append(str(int(phone_num)))
                    phone_num = ""
        if not phone_nums:
            address_obj.faulty = "FAULTY"
        for i in faulty_nums:
            if len(i) in [7, 8, 9, 11] or len(i) > 12:
                address_obj.faulty = "FAULTY"
                break

        for ph_num in set(phone_nums):
            replacer = f" {pad_char}{ph_num}{pad_char} "
            text = text.replace(ph_num, replacer)

        pattern = r'\*(\d+)\*'
        matches = re.findall(pattern, text)
        if not matches: address_obj.faulty = "FAULTY"
        for phone in matches:
            if not self.is_valid_phone_number_or_valid_pin(phone):
                address_obj.faulty = "FAULTY"
        if old_text == text: address_obj.faulty = "FAULTY"

        return text
