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
                    for char in self.typo_chars:
                        grp = grp.replace(char, self.typo_chars[char])
            new_splits.append(grp)

        text = " ".join(new_splits)
        return text


    def find_valid_nums(self, input_string):
        # Create a regex pattern to match substrings containing only digits or expected_chars
        pattern = re.compile(f'[\\d{"".join(self.expected_chars)}]+')
        potential_substrings = pattern.findall(input_string)
        
        for potential_string in potential_substrings:
            for char in potential_string:
                if char not in self.expected_chars and not char.isdigit():
                    potential_substrings.remove(potential_string)
                    break   

        valid_nums = dict()
        invalid_nums = dict()
        phone_nums = []
        pin_code = ""

        for substring in potential_substrings:
            digits_only = re.sub(f'[^\\d]', '', substring) # Remove any non-digit characters
            digits_only = digits_only.lstrip('0') # Remove leading zeros

            if len(digits_only) == 6:
                if not pin_code:
                    valid_nums[substring] = digits_only
                    pin_code = digits_only
                    continue

            if len(digits_only) == 10:
                valid_nums[substring] = digits_only
                phone_nums.append(digits_only)
                continue

            if len(digits_only) == 12:
                if digits_only[:2] == '91' and digits_only[2:].lstrip('0') == digits_only[2:]:
                    valid_nums[substring] = digits_only
                    phone_nums.append(digits_only[2:])
                continue
            
            if len(digits_only) in [6, 8, 9, 11] or len(digits_only) > 12:
                invalid_nums[substring] = digits_only
        
        # print(valid_nums)
        # print(f"\033[31m{invalid_nums}\033[0m")
        return valid_nums, invalid_nums, phone_nums, pin_code


    def pad_numbers(self, address_string, address_obj):
        # Pad pincode and phonoe number(s) with "*" characters
        address_string = self.fix_digit_typos(address_string)

        new_text = address_string
        valid_nums, invalid_nums, phone_nums, pin_code = self.find_valid_nums(new_text)

        for valid_substring in valid_nums:
            new_text = new_text.replace(valid_substring, f" *{valid_nums[valid_substring]}* ") # padded with "*"

        if new_text == address_string: address_obj.faulty = "FAULTY"
        if not phone_nums: address_obj.faulty = "FAULTY"
        if len(invalid_nums): address_obj.faulty = "FAULTY"
        # print(new_text)
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
