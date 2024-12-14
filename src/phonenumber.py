import re
from src.utils import Utils
from src.phone_number_lookup import PhoneNumberLookup


class PhoneNumber:

    def __init__(self, phone_lookup):
        self.utility = Utils()
        phone_number_prefixes = [" contact no ", " mobile, no ", " mobail no ", " mobile no ", " mobal nbr ", "mobail",
                                 "mobail no",
                                 " phone no ", " mobil no ", " cell no ", " cell ", " noumber ", " contact ",
                                 " mobile/", " mob no*", " wtsp ", " mobile ", " mb nbr ", " mob no ", " m no/*",
                                 " phone ", ",ph no ", " po no ", " mobil ", " ph no ", " m no_*", " m no/ ",
                                 " mob/*", " c no ", " phon ", " m no ", "phone ", " mob,", ",no *", " mob ", " mb ",
                                 " mob*",
                                 " no *", ",mo *", " pn ", " po ", " ph ", " nm ", " mo ", " m *", " number ", " nub ",
                                 " mob nub-", "no,",
                                 "phn num,", "phn num"]
        self.phone_number_prefixes = self.utility.reverse_list(sorted(list(set(phone_number_prefixes)), key=len))
        self.phone_lookup = phone_lookup

    def collapse_phone_number(self, text):
        regex_1 = r'\d+[ ]\d+[ ]\d+'
        regex_2 = r'\d[iIoO]\d'
        regex_3 = r'\d[iIoO]+$'

        match_1 = re.findall(regex_1, text)
        if len(match_1) > 0:
            for match in match_1:
                match_replacer = match.replace(" ", "")
                text = text.replace(match, match_replacer)

        match_2 = re.findall(regex_2, text)
        if len(match_2) > 0:
            for match in match_2:
                match_replacer = match.replace("i", "1")
                match_replacer = match_replacer.replace("I", "1")
                match_replacer = match_replacer.replace("o", "0")
                match_replacer = match_replacer.replace("O", "0")
                text = text.replace(match, match_replacer)

        match_3 = re.findall(regex_3, text)
        if len(match_3) > 0:
            for match in match_3:
                match_replacer = match.replace("i", "1")
                match_replacer = match_replacer.replace("I", "1")
                match_replacer = match_replacer.replace("o", "0")
                match_replacer = match_replacer.replace("O", "0")
                text = text.replace(match, match_replacer)

        text = self.utility.text_cleaner(text)
        return text

    def is_valid_phone_number_or_valid_pincode(self, phone):
        try:
            if len(str(int(phone))) == 10 or len(phone) == 6:
                return True
        except:
            pass 
        return False

    def pad_phone_number(self, text, pad_word, address_obj):
        space = " "
        self.collapse_phone_number(text)

        regex_1 = r"[6-9]\d{9}"  # phone number at the beginning
        regex_2 = r"[ ][6-9]\d{9}[ ]|[ ][6-9]\d{9}$"  # " 7534564334 "
        regex_3 = r"[6-9]\d{4}[ ]\d{5}"  # "65345 64334"
        regex_4 = r"[^*0-9][6-9]\d{9}|[^*0-9][6-9]\d{9}$"  # "n4534564334"
        regex_5 = r"91\d{10}"  # "914534564334"
        regex_6 = r"91-\d{10}"  # "91-4534564334"
        regex_7 = r"[6-9] \d{9}" #   "7 217696915"
        regex_8 = r"[6-9]\d{8} \d{1} " #"721769691 5"
        regex_9 = r"[6-9]\d{1} \d{4} \d{4} "  # "72 1769 6915"
        regex_10 = r"[6-9]\d{5} \d{4} "  # "721769 6915"
        regex_11 = r"[6-9]\d{2} \d{2} \d{2} \d{3}"  # "721 76 96 915"
        regex_12 = r" [6-9][0-9 ]+"  # "7 2 1 7 6 9 6 9 1 5"
        regex_13 = r"[6-9]\d{2} \d{2} \d{5}" #"721 76 96915"
        regex_14 = r"[6-9]\d{4}_\d{5}" #98151_32964


        regex_1_matches = re.findall(regex_1, text)
        if len(regex_1_matches) > 0:
            for match in set(regex_1_matches):
                ph_num = match
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_1_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_1_replacer)

        regex_2_matches = re.findall(regex_2, text)
        if len(regex_2_matches) > 0:
            for match in set(regex_2_matches):
                ph_num = match.strip()
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_2_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_2_replacer)

        regex_3_matches = re.findall(regex_3, text)
        if len(regex_3_matches) > 0:
            for match in set(regex_3_matches):
                ph_num = match.replace(" ", "").strip()
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_3_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_3_replacer)

        regex_4_matches = re.findall(regex_4, text)
        if len(regex_4_matches) > 0:
            for match in set(regex_4_matches):
                ph_num = match[1:]
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                left_outer_char = match[0]
                regex_4_replacer = left_outer_char + space + pad_word + ph_num + pad_word + space
                regex_4_replacer = regex_4_replacer.replace(" ", "")
                match = match.replace(" ", "")
                text = text.replace(match, regex_4_replacer)

        regex_5_matches = re.findall(regex_5, text)
        if len(regex_5_matches) > 0:
            for match in set(regex_5_matches):
                ph_num = match.replace("91", "")
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_5_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_5_replacer)

        regex_6_matches = re.findall(regex_6, text)
        if len(regex_6_matches) > 0:
            for match in set(regex_6_matches):
                ph_num = match.replace("91-", "")
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_6_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_6_replacer)

        regex_7_matches = re.findall(regex_7, text)
        if len(regex_7_matches) > 0:
            for match in set(regex_7_matches):
                ph_num = match.replace(" ", "")
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_7_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_7_replacer)

        regex_8_matches = re.findall(regex_8, text)
        if len(regex_8_matches) > 0:
            for match in set(regex_8_matches):
                ph_num = match.replace(" ", "")
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_8_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_8_replacer)
        regex_9_matches = re.findall(regex_9, text)
        if len(regex_9_matches) > 0:
            for match in set(regex_9_matches):
                ph_num = match.replace(" ", "")
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_9_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_9_replacer)

        regex_10_matches = re.findall(regex_10, text)
        if len(regex_10_matches) > 0:
            for match in set(regex_10_matches):
                ph_num = match.replace(" ", "")
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_10_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_10_replacer)

        regex_11_matches = re.findall(regex_11, text)
        if len(regex_11_matches) > 0:
            for match in set(regex_11_matches):
                ph_num = match.replace(" ", "")
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_11_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_11_replacer)

        regex_12_matches = re.findall(regex_12, text)
        if len(regex_12_matches) > 0:
            for match in set(regex_12_matches):
                if len(match.replace(" ", "")) >= 10:
                    ph_num = match.replace(" ", "")
                    if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                    regex_12_replacer = space + pad_word + ph_num + pad_word + space
                    text = text.replace(match, regex_12_replacer)

        regex_13_matches = re.findall(regex_13, text)
        if len(regex_13_matches) > 0:
            for match in set(regex_13_matches):
                ph_num = match.replace(" ", "")
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_13_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_13_replacer)

        regex_14_matches = re.findall(regex_14, text)
        if len(regex_14_matches) > 0:
            for match in set(regex_14_matches):
                ph_num = match.replace("_", "") 
                if len(ph_num) == 12 and ph_num.startswith("91"): ph_num = ph_num[2:]
                regex_14_replacer = space + pad_word + ph_num + pad_word + space
                text = text.replace(match, regex_14_replacer)

        # check if the phone number and pincode is valid
        # NOTE: we check for both, as pincode is expected to be already padded here. NOTE(NEW): Not anymore
        pattern = r'\*(\d+)\*'
        matches = re.findall(pattern, text)
        for phone in matches:
            if not self.is_valid_phone_number_or_valid_pincode(phone):
                address_obj.faulty = "FAULTY"
        return text

    def mobile_number_text_remover(self, text):
        if text is not None:
            address = text.lower()
            for prefix in self.phone_number_prefixes:
                if address.find(prefix) != -1 and prefix.find(",") != -1 and prefix.find("*") != -1:
                    address = address.replace(prefix, ", *")
                if address.find(prefix) != -1 and prefix.find("*") != -1:
                    address = address.replace(prefix, " *")
                if address.find(prefix) != -1:
                    address = address.replace(prefix, " ")
            return address

    def get_hilighted_phone_number_from_address(self, address_obj):
        highlighted_phone_number_regex = r"[*]\d{10,12}[*]"
        return list(set(re.findall(highlighted_phone_number_regex, address_obj.address)))

    def update_phone_number(self, address_obj):
        highlighted_phone_list = self.get_hilighted_phone_number_from_address(address_obj)
        if highlighted_phone_list is not None and len(highlighted_phone_list) > 0:
            if len(highlighted_phone_list) > 1:
                phone_list = []
                for highlighted_phone in highlighted_phone_list:
                    phone = highlighted_phone.replace("*", "")
                    phone_list.append(phone)
                    address_obj.address = address_obj.address.replace(highlighted_phone, "").strip()
                    is_reorder = self.phone_lookup.search_phone_number(phone)
                    if is_reorder:
                        address_obj.is_reorder = is_reorder
                    else:
                        self.phone_lookup.save_phone_number(int(phone))
                phones_as_string = " , ".join(phone_list)
                address_obj.phone = phones_as_string
                address_obj.address = address_obj.address + " PH " + phones_as_string
                address_obj.address = self.utility.text_cleaner(address_obj.address)
                return address_obj.is_reorder
            elif len(highlighted_phone_list) > 0:
                highlighted_phone = highlighted_phone_list[0]
                phone = highlighted_phone.replace("*", "")
                address_obj.address = (address_obj.address.replace(highlighted_phone, "").strip() + " PH " + phone)
                address_obj.address = self.utility.text_cleaner(address_obj.address)
                address_obj.phone = phone
                is_reorder = self.phone_lookup.search_phone_number(phone)
                address_obj.is_reorder = is_reorder
                if not is_reorder:
                    self.phone_lookup.save_phone_number(int(phone))
                return is_reorder

    def update_phone_numbers_lookup(self, numbers=[]):
        self.phone_lookup.update_phone_numbers(numbers)