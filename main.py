import re
import sys
import os
from pathlib import Path

from src.address import Address
from src.utils import Utils
from src.pincode import PinCode
from src.phonenumber import PhoneNumber
from src.msoffice import MsOffice
from src.phone_number_lookup import PhoneNumberLookup
from src.statemapper import StateMapper
from src.districtmapper import DistrictMapper
from src.bookmapper import BookMapper
from src.langmapper import LanguageMapper

from src.colors import *


output_dir = "output_dir"

pincode = PinCode()
phone_number_lookup = PhoneNumberLookup()
phone_number = PhoneNumber(phone_number_lookup)
ms_office = MsOffice()
utils = Utils()
state_mapper = StateMapper()
district_mapper = DistrictMapper()
book_mapper = BookMapper()
lang_mapper = LanguageMapper()


def get_address_list(chat_log: str) -> list:
    # NOTE: notes.md note 01
    # Remove the first line from the text
    newline_index = chat_log.find('\n')
    if newline_index != -1:
        chat_log = chat_log[newline_index + 1:]

    # I dont am/pm wale format me "\u202f" kahan se aajata hai (eg: "10:18\u202fam" instead of "10:18 am")
    chat_log = chat_log.replace('\u202f', ' ')

    pattern = r"(?i)(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} (?:am|pm) -)"
    split_log = re.split(pattern, chat_log)
    
    # for i in split_log:
    #     print(f"{RED}===================={RESET}")
    #     print(f"{BLUE}log = {i}{RESET}")
    #     print(f"{YELLOW}===================={RESET}")
    
    # NOTE: notes.md note 02
    # relevant log format: DD/MM/YY, HH:MM - CONTACT: MESSAGE
    # split around "DD/MM/YY HH:MM (AM/PM)" -> ['', 'date, time', 'contact: message', ...] 
    # so only append alternate logs skipping '' and logs that dont contain ':' (not a relevant message log)
    # rest of the part after first ":" is the message.
    string_address_list = []
    for i in range(0, len(split_log), 2):
        log = split_log[i]
        if log and ":" in log:
            message = log[log.find(':') + 1:].strip()
            string_address_list.append(message)

    address_list = []
    for address_text in string_address_list:
        address_text = utils.text_cleaner(address_text)
        if address_text and not utils.whatsapp_text(address_text):
            address_obj = Address(address_text.lower(), None, None, None, None, None)
            address_list.append(address_obj)
    return address_list

def process_addresses(file_text):
    if file_text is None or not len(file_text):
        return []

    address_list = get_address_list(file_text)
    
    output = ""
    for i in address_list:
        output += "\n\n" + str(i.address) + "\n\n"

    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(output)

    print(len(address_list))
    
    address_obj_list = []
    phone_numbers = []
    for itr, address_obj in enumerate(address_list):
        print("Main:process_addresses", itr)
        try:
            address_string = address_obj.address
            address_string = pincode.pin_code_extender(address_string)
            address_string = utils.clean_stopping_words_and_phrases(address_string)
            address_string = pincode.pad_pin_code(address_string, "*")
            address_string = phone_number.collapse_phone_number(address_string)
            address_string = phone_number.pad_phone_number(address_string, "*")
            address_string = phone_number.mobile_number_text_remover(address_string)
            address_string = pincode.pin_number_text_remover(address_string)
            address_obj.address = address_string
            pincode.update_pin_number(address_obj)
            phone_number.update_phone_number(address_obj)
            address_obj.address = utils.text_cleaner(address_obj.address)
            address_obj.capitalize_address()
            
            # phone number
            if address_obj.phone:
                phone_numbers.append(address_obj.phone)

            #Attribute from address parsing
            state_add, dist_add, occ_count = utils.get_data_from_address(address_obj.address)
            address_obj.set_state_from_address(state_add)
            address_obj.set_district_from_address(dist_add)
            address_obj.set_occ_count(occ_count)

            address_obj.set_dist_matches_pin_and_addr(utils.is_string_same(dist_add, address_obj.district))
            address_obj.set_state_matches_pin_and_addr(utils.is_string_same(state_add, address_obj.state))
            address_obj.set_book_name(book_mapper.get_book_from_address_record(address_string))
            address_obj.set_book_lang(lang_mapper.get_book_lang_from_address_record(address_string))

            address_obj_list.append(address_obj)
        except:
            print("Error address: " + address_obj.address)

    address_obj_list.sort(key=lambda x: len(x.address_old), reverse=True)
    utils.update_reorder_and_repeat(address_obj_list)
    phone_number_lookup.update_phone_numbers(phone_numbers)
    return address_obj_list

def main():
    if not os.path.exists(output_dir): 
        os.makedirs(output_dir)

    flag = sys.argv[1].lower()
    fname = sys.argv[2]

    if flag in ['-f', '-file', '--f', '--file']:
        file_text = utils.read_input_file(fname)
        address_list = process_addresses(file_text)

        output_file_path_xls = utils.generate_output_file_path(output_dir, Path(fname).stem, "xls")
        print(output_file_path_xls)
        ms_office.export_to_MS_Excel(address_list=address_list, file_name=output_file_path_xls)

    elif flag in ['-n', '-name', '--n', '--name']:
        address_list = ms_office.import_from_Excel_sheet(fname)
        for address in address_list:
            utils.update_address_name(address)
        ms_office.export_to_MS_Excel(address_list, str(fname.split(".")[0] + "_name.xls"))

    else:
        print("[!] Invalid argument")
        print("[-file, -f, --f, --file]: for file processing \n[-name, -n, --n, --name]: generate name column")
        print("[Example]: python main.py -f whatsapp.txt")


if __name__ == "__main__":
    main()
