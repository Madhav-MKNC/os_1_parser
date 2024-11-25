import math
import bisect
import os
from os import path

class PhoneNumberLookup:

    def __init__(self):
        self.number_file = os.getcwd() + "/src/phone_number_lookup.txt"
        self.numbers = []
        if path.exists(self.number_file):
            with open(self.number_file, 'r') as f:
                phone_number_text = f.read()
                phone_number_list = phone_number_text.split("\n")
            for number in phone_number_list:
                if len(number.strip()) > 0:
                    self.numbers.append(int(number.strip()))
        list(set(self.numbers)).sort()

    def search_phone_number(self, number_string):
        return self.binary_search_for_phone_number(0, len(self.numbers), int(number_string))

    def binary_search_for_phone_number(self, start, end, number):
        if start <= end:
            mid = math.floor((end + start) / 2)
            mid_phone_number = self.get_item_at_index(self.numbers, mid)
            if mid_phone_number is not None:
                if number == mid_phone_number:
                    return True
                elif mid_phone_number < number:
                    return self.binary_search_for_phone_number(mid + 1, end, number)
                else:
                    return self.binary_search_for_phone_number(start, mid - 1, number)
        return False

    def get_item_at_index(self, number_list, position):
        # print("PhoneNumberLookup:get_item_at_index")
        try:
            index_value = number_list[position]
            # print(index_value)
        except IndexError:
            index_value = None
        return index_value

    def save_phone_number(self, number):
        #print("PhoneNumberLookup:save_phone_number")
        #print(number)
        if not self.search_phone_number(int(number)):
            bisect.insort(self.numbers, number)
        #print(self.numbers)

    def update_phone_numbers(self):
        # print("PhoneNumberLookup:update_phone_numbers")
        # print(self.numbers)
        with open(self.number_file, 'w') as f:
            number_string = list(map(str, self.numbers))
            #print("Phone numbers : %s " % self.numbers)
            f.write('\n'.join(number_string))
