# Extract, collapse and pad phone numbers and pincode

import re


class NumbersHandler:
    def __init__(self):
        self.expected_chars = [" ", "-", "_"]
        self.typo_chars = {"i": "1", "I": "1", "o": "0", "O": "0"}

    def fix_digit_typos(self, text):
        # Rule: split texts around space
        # iff a group contains atleast one 0-9 and only typo chars
        # group has atlest 3 chars

        splits = text.split(" ")
        new_splits = []
        for grp in splits:
            if len(grp) >= 3:
                # Check if the string contains at least one digit and only 'i', 'o', and digits (no other characters)
                if re.match(r'^[io0-9]*$', grp) and re.search(r'\d', grp):
                # if re.match(r'^[io0-9]*$', grp) and re.search(r'\d', grp): # add self.expected_chars in the check
                    for char in self.typo_chars:
                        grp = grp.replace(char, self.typo_chars[char])
            new_splits.append(grp)

        text = " ".join(new_splits)
        return text


    def pad_numbers(self, address_string, address_obj):
        # address_string = phone_number.collapse_phone_number_and_pin(address_string)
        # address_string = phone_number.pad_phone_number(address_string, "*", address_obj)
        # address_string = pincode.pad_pin_code(address_string, "*", address_obj)
        # return address_string

        address_string = self.fix_digit_typos(address_string)
        new_text = address_string
        pad_char = "*"

        pin_code = ""
        phone_nums = []
        faulty_nums = []

        number_str = ""
        # temp_text = new_text
        digit_begin = True
        padded_text = str("#" + address_string + "#") # temp padding with "#" for inclusivity of corner digits (if there).
        temp_text = padded_text

        i = -1
        while True:
            i += 1
            if i >= len(padded_text): break

            char = padded_text[i]
            if char.isdigit():
                number_str += char
                number_str = str(int(number_str)) # For removing preceding 0's
                if digit_begin:
                    temp_text = padded_text[:i] + pad_char + padded_text[i:] # beginning pad_char
                    # i += 1 # due to adding "*" the str[i] shifts to str[i+1] so we have to skip it
                    digit_begin = False
            elif char in self.expected_chars:
                temp_text = padded_text[:i] + padded_text[i+1:] # skip/remove this char
                # i -= 1 # due to deleting str[i], str[i+1] shifts to str[i] so we have to reread it
                continue
            else:
                if number_str:
                    if len(number_str) == 10:
                        phone_nums.append(number_str)
                        temp_text = padded_text[:i] + pad_char + padded_text[i:] # ending pad_char
                        # i += 1 # due to adding "*" the str[i] shifts to str[i+1] so we have to skip it   
                        new_text = temp_text
                    elif len(number_str) == 12 and number_str[:2] == "91":
                        if len(str(int(number_str[2:]))) == 10:
                            phone_nums.append(number_str[2:])
                            temp_text = padded_text[:i] + pad_char + padded_text[i:] # ending pad_char
                            # i += 1 # due to adding "*" the str[i] shifts to str[i+1] so we have to skip it   
                            new_text = temp_text
                        else: faulty_nums.append(number_str)
                    elif len(number_str) == 6:
                        if not pin_code:
                            pin_code = number_str
                            temp_text = padded_text[:i] + pad_char + padded_text[i:] # ending pad_char
                            # i += 1 # due to adding "*" the str[i] shifts to str[i+1] so we have to skip it   
                            new_text = temp_text
                        else: # i.e. entry with more than 1 pincode -> faulty
                            faulty_nums.append(number_str) # so faulty_nums might also have len 6 nums
                    else: faulty_nums.append(str(int(number_str)))
                # reset all temp variables
                temp_text = new_text
                number_str = ""
                digit_begin = True

        new_text = new_text[1:-1] # removing the padded "#"'s from the ends
        
        # if pin_code: address_obj.pin = pin_code
        # for phn_num in phone_nums: pass

        if address_string == new_text: address_obj.faulty = "FAULTY"
        if not phone_nums: address_obj.faulty = "FAULTY"
        for i in faulty_nums:
            if len(i) in [6, 8, 9, 11] or len(i) > 12:
                address_obj.faulty = "FAULTY"
                break
        print(new_text)
        return new_text


if __name__ == "__main__":
    x = NumbersHandler()
    tests = """
iiii-oooi1      2
iiiiooo i 1     2 
iiiirooo i 1    2
bii5
    """.strip()
    for i in tests.split('\n'):
        if 'off' in i: continue
        i = i.strip()
        inp, index = i[:-2], int(i[-1])-1 # only one digit indexes
        print(x.valid_digit(inp, index))
