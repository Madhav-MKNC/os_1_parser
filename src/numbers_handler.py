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

    def pad_numbers(self, address_string, address_obj):
        # return address_string
        new_text = address_string
        pad_char = "*"
        expected_chars = [" ", "-", "_"]

        pin_code = ""
        phone_nums = []
        faulty_nums = []

        number_str = ""
        temp_text = new_text
        digit_begin = True
        padded_text = str("#" + address_string + "#") # temp padding with "#" for inclusivity of corner digits (if there).

        for i in range(len(padded_text)):
            char = padded_text[i]
            if char.isdigit():
                number_str += char
                number_str = str(int(number_str)) # For removing preceding 0's
                if digit_begin:
                    temp_text = padded_text[:i] + pad_char + padded_text[i:] # beginning pad_char
                    digit_begin = False
            elif char in expected_chars:
                temp_text = padded_text[:i] + padded_text[i+1:] # skip/remove this char
                continue
            else:
                if number_str:
                    if len(number_str) == 10:
                        phone_nums.append(number_str)
                        temp_text = padded_text[:i] + pad_char + padded_text[i:] # ending pad_char
                        new_text = temp_text
                    elif len(number_str) == 12 and number_str[:2] == "91":
                        if len(str(int(number_str[2:]))) == 10:
                            phone_nums.append(number_str[2:])
                            temp_text = padded_text[:i] + pad_char + padded_text[i:] # ending pad_char
                            new_text = temp_text
                        else: faulty_nums.append(number_str)
                    elif len(number_str) == 6:
                        if not pin_code:
                            pin_code = number_str
                            temp_text = padded_text[:i] + pad_char + padded_text[i:] # ending pad_char
                            temp_text = new_text
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

        return new_text
