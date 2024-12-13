class Address:
    def __init__(self, address, state, district, block, pin, phone, is_reorder=False, name=None,
                 state_from_address=None,
                 district_from_address=None, count=None, dist_matches_pin_and_addr=None,
                 state_matches_pin_and_addr=None, book_name=None, book_lang=None, is_repeat=None, email=None):
        self.address = address
        self.address_old = address
        self.state = state
        self.district = district
        self.block = block
        self.pin = pin
        self.phone = phone
        self.is_reorder = is_reorder
        self.name = name
        self.state_from_address = state_from_address
        self.district_from_address = district_from_address
        self.occ_count = count
        self.dist_matches_pin_and_addr = dist_matches_pin_and_addr
        self.state_matches_pin_and_addr = state_matches_pin_and_addr
        self.book_name = book_name
        self.book_lang = book_lang
        self.is_repeat = is_repeat
        self.email = email

    def __lt__(self, other):
        val1, val2 = self.__evaluate(other)
        if val1 < val2:
            return True
        else:
            return False

    def __evaluate(self, other):
        val1 = len(self.address)
        val2 = len(other.address)
        return val1, val2

    def print_attributes(self):
        data = ""
        if self.name is not None:
            data = data + " Name:" + self.name
        if self.state is not None:
            data = data + ",State:" + self.state
        if self.district is not None:
            data = data + ",District:" + self.district
        if self.block is not None:
            data = data + ",Block:" + self.block
        if self.pin is not None:
            data = data + ",Pin:" + self.pin
        if self.phone is not None:
            data = data + ",Phone:" + self.phone
        if self.address is not None:
            data = data + " Address:" + self.address
        if self.book_name is not None:
            data = data + " Book Name:" + self.book_name
        if self.book_lang is not None:
            data = data + " Book Language:" + self.book_lang
        if self.is_repeat is not None:
            data = data + " repeat : " + str(self.is_repeat)
        data = data + " Is reorder: " + str(self.is_reorder)
        print(data)

    def print_address_old(self):
        print(self.address_old)
        return

    def print_address_new(self):
        print(self.address)
        return

    def capitalize_address(self):
        address_tokens = self.address.split(" ")
        capital_word_array = []
        for address_token in address_tokens:
            if len(address_token.strip()) > 0:
                capital_word_array.append(address_token.strip().capitalize())
        self.address = " ".join(capital_word_array)

    def set_state(self, state):
        self.state = state

    def set_dist(self, dist):
        self.district = dist

    def set_state_from_address(self, state):
        self.state_from_address = state

    def set_district_from_address(self, dist):
        self.district_from_address = dist

    def set_occ_count(self, count):
        self.occ_count = count

    def set_dist_matches_pin_and_addr(self, value):
        self.dist_matches_pin_and_addr = value

    def set_state_matches_pin_and_addr(self, value):
        self.state_matches_pin_and_addr = value

    def set_book_name(self, value):
        self.book_name = value

    def set_book_lang(self, value):
        self.book_lang = value

    def set_is_repeat(self, value):
        self.is_repeat = value
    
    def set_email(self, value):
        self.email = value
