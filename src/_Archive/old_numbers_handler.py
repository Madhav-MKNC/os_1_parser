class OldNumbersHandler():

    def is_valid_phone_number_or_valid_pin(self, inp):
        try:
            if len(str(int(inp))) == 10 or len(inp) == 6:
                return True
        except:
            pass 
        return False

    def this_is_a_valid_digit(self, text, index, reverse_direction=None):
        for i in self.expected_chars:
            text = text.replace(i, "")

        begin = None
        end = None
        print(text, index)
        if reverse_direction is None or reverse_direction == False:
            print('frwd')
            if index == len(text) - 1: end = text[index] not in self.typo_chars 
            elif index < len(text) - 1:
                if text[index+1].isdigit(): end = True
                elif text[index+1] in self.typo_chars: end = self.this_is_a_valid_digit(text, index+1, reverse_direction=False)
                else: end = False
            else: end = False

        if reverse_direction is None or reverse_direction == True:
            print('rev')
            if index == 0: begin = text[index] not in self.typo_chars
            elif index > 0:
                if text[index-1].isdigit(): begin = True
                elif text[index-1] in self.typo_chars: begin = self.this_is_a_valid_digit(text, index-1, reverse_direction=False)
                else: begin = False
            else: begin = False

        return begin or end
