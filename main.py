import re
import sys
import os
import traceback
from pathlib import Path
from src.address import Address
from src.utility import Utility
from src.pincode import PinCode
from src.phonenumber import PhoneNumber
from src.msoffice import MsOffice
from src.phone_number_lookup import PhoneNumberLookup
from src.statemapper import StateMapper
from src.districtmapper import DistrictMapper
from src.bookmapper import BookMapper
from src.langmapper import LanguageMapper


class Main:

    def __init__(self):
        self.utility = Utility()
        self.pincode = PinCode()
        self.phone_number_lookup = PhoneNumberLookup()
        self.phone_number = PhoneNumber(self.phone_number_lookup)
        self.output_dir = "output_dir"
        self.ms_office = MsOffice()
        self.utility = Utility()
        self.state_mapper = StateMapper()
        self.district_mapper = DistrictMapper()
        self.book_mapper = BookMapper()
        self.lang_mapper = LanguageMapper()


    def process_addresses(self, addresses_file_text):
        # print("Main:process_addresses")
        address_list = []
        if addresses_file_text is not None and len(addresses_file_text) > 0:
            address_object_list = self.get_address_list(addresses_file_text)
            for address_obj in address_object_list:
                # print("Main:process_addresses")
                try:
                    if not self.utility.is_valid_address(address_obj.address):
                        continue
                    address_string = address_obj.address
                    address_string = self.pincode.pin_code_extender(address_string)
                    address_string = self.utility.clean_stopping_words_and_phrases(address_string)
                    address_string = self.pincode.pad_pin_code(address_string, "*")
                    address_string = self.phone_number.collapse_phone_number(address_string)
                    address_string = self.phone_number.pad_phone_number(address_string, "*")
                    address_string = self.phone_number.mobile_number_text_remover(address_string)
                    address_string = self.pincode.pin_number_text_remover(address_string)
                    address_obj.address = address_string
                    self.pincode.update_pin_number(address_obj)
                    self.phone_number.update_phone_number(address_obj)
                    address_obj.address = self.utility.white_space_cleaner(address_obj.address)
                    address_obj.capitalize_address()

                    #Attribute from address parsing
                    state_add, dist_add, occ_count = self.utility.get_data_from_address(address_obj.address)
                    address_obj.set_state_from_address(state_add)
                    address_obj.set_district_from_address(dist_add)
                    address_obj.set_occ_count(occ_count)

                    address_obj.set_dist_matches_pin_and_addr(
                        self.utility.is_string_same(dist_add, address_obj.district))
                    address_obj.set_state_matches_pin_and_addr(
                        self.utility.is_string_same(state_add, address_obj.state))
                    address_obj.set_book_name(self.book_mapper.get_book_from_address_record(address_string))
                    address_obj.set_book_lang(self.lang_mapper.get_book_lang_from_address_record(address_string))

                    address_list.append(address_obj)
                    # print(address_obj.print_attributes())
                except:
                    # traceback.print_exception(*sys.exc_info())
                    # pass
                    #print("-------------------------")
                    print("Error address: " + address_obj.address)

        address_list.sort(key=lambda x: len(x.address_old), reverse=True)
        self.utility.update_reorder_and_repeat(address_list)
        return address_list

    def main(self):
        arguments = sys.argv[1:]
        key, file = arguments[0].split("=")
        if key == "-file":
            addresses_file_text = self.read_from_file(file)
            address_list = self.process_addresses(addresses_file_text)
            #self.utility.print_address(address_list)
            file_base_name = Path(file).stem

            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            output_file_name_xls = os.path.join(self.output_dir, self.utility.generate_output_file_name(file_base_name, "xls"))
            self.ms_office.export_to_MS_Excel(address_list, output_file_name_xls)

            #output_file_name_docx = self.output_dir + self.utility.generate_output_file_name(file_base_name, "docx")
            #self.ms_office.export_to_MS_word(address_list,output_file_name_docx)

            self.phone_number_lookup.update_phone_numbers()
        elif key == "-name":
            address_list = self.ms_office.import_from_Excel_sheet(file)
            for address in address_list:
                self.utility.update_address_name(address)
            self.ms_office.export_to_MS_Excel(address_list, str(file.split(".")[0] + "_name.xls"))
        else:
            print("Invalid argument!!, -file: for file processing, -name: generate name column")

    def get_address_list(self, text):
        address_list = []
        regex = ['\d{1,2}\/\d{1,2}\/\d{2}, \d+:\d+ - [a-zA-Z-0-9 ]+:',
                 '\d{1,2}\/\d{1,2}\/\d{2}, \d+:\d+ [apAP][mM] - [a-zA-Z-0-9 ]+:',
                 '\[\d{1,2}:\d{1,2}, \d{1,2}\/\d{1,2}\/\d{4}\] [a-zA-Z-0-9 ]+:',
                 '\d{1,2}\/\d{1,2}\/\d{1,4}, \d{1,2}:\d{1,2} [aAPp][Mm] - \+[0-9 ]+:',
                 '\d{1,2}\/\d{1,2}\/\d{2}, \d+:\d+ [apAP][mM] - [a-zA-Z-0-9 ]+:[ 0-9-🪀a-zA-Z:\/\.?]+\s\[',
                 '\d{1,2}\/\d{1,2}\/\d{2}, \d+:\d+ [apAP][mM] - [a-zA-Z-0-9 ]+:[ 0-9-🪀a-zA-Z:\/\.?]+wa\.me\/\d+[ ]{1,4}[^[]',
                 '\d{1,2}\/\d{1,2}\/\d{2}, \d+:\d+ [apAP][mM] - [a-zA-Z-0-9 ]+:[ 0-9-🪀a-zA-Z:\/\.?]+=Hi\s+',
                 '\d{1,2}\/\d{1,2}\/\d{2}, \d+:\d+ - [mM]essages and calls','\d{1,2}\/\d{1,2}\/\d{2}, \d+:\d+ - [yY]ou']

        regex_split_main = re.compile("|".join(regex))
        string_address_list = re.split(regex_split_main, text)
        if len(string_address_list) <= 1:
            string_address_list = re.split("\n", text)

        for address_text in string_address_list:
            address_text = address_text.replace("[\s]+", " ")
            self.utility.white_space_cleaner(address_text)
            if len(address_text.strip()) > 0 and not self.utility.whatsapp_text(address_text):
                address_obj = Address(address_text.lower(), None, None, None, None, None)
                address_list.append(address_obj)
        return address_list

    def read_from_file(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            text = f.read()
        return text



if __name__ == "__main__":
    main_obj = Main()
    main_obj.main()

#c/o d.h.patil
#prasanna kumar m
# 188, sri kanavi siddeshwara nilaya, shivabasava nagar, near arunodaya school,navule,shivamogga -577204, 98459007159
#𝙿𝚑𝚘𝚗𝚎 𝚗𝚘 9964941056 𝙿𝚞𝚝𝚝𝚊 𝚛𝚊𝚓𝚞      𝚜/𝚘 𝚙𝚞𝚝𝚝𝚊𝚜𝚒𝚍𝚍𝚑𝚊 𝚟𝚒𝚕𝚕𝚊𝚐𝚎 𝚔𝚘𝚕𝚊𝚐𝚊𝚕𝚊 𝚑 𝚍 𝚔𝚘𝚝𝚎 𝚑𝚘𝚞𝚜𝚎 𝚗𝚘 231 𝚗𝚎𝚊𝚛 𝚔𝚘𝚕𝚊𝚐𝚊𝚕𝚊 𝚑 𝚍 𝚔𝚘𝚝𝚎 𝚝𝚑𝚊𝚕𝚔𝚞 𝚖𝚢𝚜𝚘𝚛𝚎 𝚍𝚒𝚜𝚝𝚒𝚌 𝚙𝚘𝚜𝚝 𝚌𝚘𝚍𝚎 571125
#Phone no 9964941056 Putta raju S/O Puttasiddhu village Kolagala h d kote house no 231 near kolagala h d kote taluk mysore dist post code 571125
#Putta raju S/O Puttasiddhu village Kolagala H D kote, house no 231 near kolagala H D Kote Tq mysore Dist

