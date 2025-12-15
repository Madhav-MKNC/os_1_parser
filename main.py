
import re
import sys
import os
from pathlib import Path
from typing import List, Dict

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import os

from src.address import Address
from src.utils import Utils
from src.mknc_utils import MKNCUtils
from src.emails_handler import Email
from src.numbers_handler import NumbersHandler
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

email = Email()
numbers_handler = NumbersHandler()
pincode = PinCode()
phone_number_lookup = PhoneNumberLookup()
phone_number = PhoneNumber()
ms_office = MsOffice()
utils = Utils()
mknc_utils = MKNCUtils()
state_mapper = StateMapper()
district_mapper = DistrictMapper()
book_mapper = BookMapper()
lang_mapper = LanguageMapper()


def get_address_list(chat_log: str, flag='-f') -> list:
    if flag == '-m':
        string_address_list = [i.strip() for i in chat_log.split('\n') if i.strip()]
    
    else:
        # NOTE: notes.md note 01
        # Remove the first line from the text
        newline_index = chat_log.find('\n')
        print(f"{BLUE}*** Removing first line from the input file ***{RESET}")
        print(f"*** First line: [{YELLOW}{chat_log[0:newline_index]}{RESET}]")
        if newline_index != -1:
            chat_log = chat_log[newline_index + 1:]

        # I dont know am/pm wale format me "\u202f" kahan se aajata hai (eg: "10:18\u202fam" instead of "10:18 am")
        # actually... i know, that's some special char that looks like a space but is not a space
        # so replacing it with normal space
        chat_log = chat_log.replace('\u202f', ' ')

        pattern = r"(?i)(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}(?: (?:am|pm))? -)"
        split_log = re.split(pattern, chat_log)
        print(f"{GREEN}*** len(split_log): [{len(split_log)}]{RESET}")
        print(f"*** Splitted input: {YELLOW}{str(split_log)[0:100]}..., ...]{RESET}")
        
        # for i in split_log:
        #     print(f"{RED}=============================================={RESET}")
        #     print(f"{BLUE}log = {i}{RESET}")
        #     print(f"{YELLOW}=============================================={RESET}\n")
    
        # NOTE: notes.md note 02
        # relevant log format: DD/MM/YY, HH:MM - CONTACT: MESSAGE
        # split around "DD/MM/YY HH:MM (AM/PM)" -> ['', 'date, time', 'contact: message', ...] 
        # so only append alternate logs skipping '' and logs that excludes ':' (not a relevant message log)
        # rest of the part after first ":" is the message.
        string_address_list = []
        for i in range(0, len(split_log), 2):
            log = split_log[i]
            if log and ":" in log:
                message = log[log.find(':') + 1:].strip()
                string_address_list.append(message.lower())

    address_list = []
    for address_text in string_address_list:
        if utils.valid_text(address_text):
            address_obj = Address(
                # NOTE: remove non printable characters like "☺"
                utils.remove_non_printable_chars(address_text.lower().strip()),
                None,
                None,
                None,
                None,
                None
            )
            address_list.append(address_obj)
    
    print(f"{GREEN}*** Total addresses found: [{len(address_list)}]{RESET}")
    # if not os.path.exists('tmp'): os.makedirs('tmp')
    # with open('tmp/addresses_fetched.txt', 'w', encoding='utf-8') as file:
    #     addresses_fetched = ""
    #     for i in address_list:
    #         addresses_fetched += "\n\n" + str(i.address) + "\n\n"
    #     file.write(addresses_fetched.strip())

    return address_list

# --- ADD HELPER (place above process_addresses) ---
def _process_one_address(address_obj: Address, flag: str) -> Address | None:
    try:
        address_obj = email.extract_and_update_email(address_obj)
        address_string = address_obj.address
        # address_string = pincode.pin_code_extender(address_string)
        address_string = utils.text_cleaner(address_string, flag_for_translate=flag)
        address_string = utils.clean_stopping_words_and_phrases(address_string)

        # We are handling numbers below
        address_string = numbers_handler.fix_digit_typos(address_string)
        # address_string = phone_number.collapse_phone_number_and_pin(address_string)
        address_string = pincode.pad_pin_code(address_string, "*", address_obj)
        address_string = phone_number.pad_phone_number(address_string, "*", address_obj)
        # address_string = numbers_handler.pad_numbers(address_string, address_obj) # this replaces above 3 lines of code

        address_string = phone_number.mobile_number_text_remover(address_string)
        address_string = pincode.pin_number_text_remover(address_string)
        address_obj.address = address_string
        pincode.update_pin_number(address_obj)
        # print(f"{address_obj.pin}")
        phone_number.update_phone_number(address_obj, phone_number_lookup)
        # print(f"{address_obj.phone}")
        address_obj.address = utils.last_text_cleaner(address_obj.address)

        #Attribute from address parsing
        state_add, dist_add, occ_count = utils.get_data_from_address(address_obj.address)
        address_obj.set_state_from_address(state_add)
        address_obj.set_district_from_address(dist_add)
        address_obj.set_occ_count(occ_count)

        address_obj.set_dist_matches_pin_and_addr(utils.is_string_same(dist_add, address_obj.district))
        address_obj.set_state_matches_pin_and_addr(utils.is_string_same(state_add, address_obj.state))
        address_obj.set_book_name(book_mapper.get_book_from_address_record(address_string))
        address_obj.set_book_lang(lang_mapper.get_book_lang_from_address_record(address_string))

        address_obj.address = address_obj.address.title()
        return address_obj
    except Exception as err:
        print(f"\n{RED}[ERROR] {address_obj.address[0:100]}{RESET}")
        print(f'{YELLOW}str{err}{RESET}\n')
        return None

def process_addresses(file_text, flag='-f', verbose_mode=False, enable_sorting=None):
    if file_text is None or not len(file_text):
        return []

    address_list = get_address_list(file_text, flag=flag)

    # NOTE: If there is no "# " in front of "address_list.sort" then the code will sort the address in descending order
    # 🙏 NOTE: For enabling the sorting remove the "# " (the hash and the trailing space) from the below line 👇
    if enable_sorting:
        address_list.sort(reverse=True) # sort by length of address

    address_obj_list: List[Address] = []
    # phone_numbers = []

    print(f"{BLUE}*** Processing Addresses ***{RESET}")

    # NOTE START: MultiThreaded
    total = len(address_list)
    
    # Check if running locally (speed) or on Render (memory safety)
    is_local = os.getenv('NOT_RUNNING_ON_RENDER', 'yes').lower() in ['yes', 'true', '1']
    if is_local:
        Executor = ProcessPoolExecutor
        max_workers = os.cpu_count() or 4
    else:
        Executor = ThreadPoolExecutor
        max_workers = min(32, (os.cpu_count() or 4))

    with Executor(max_workers=max_workers) as ex:
        futs = [ex.submit(_process_one_address, ao, flag) for ao in address_list]
        BATCH_SIZE = 200
        for i, fut in enumerate(as_completed(futs), 1):
            res = fut.result()
            if res is not None:
                address_obj_list.append(res)
            if not verbose_mode and (i % BATCH_SIZE == 0 or i == total or i==0):
                progress = (i / total) * 100
                filled = int(progress // 2)
                bar = '█' * filled + '-' * (50 - filled)
                color = GREEN if progress == 100 else YELLOW
                print(
                    f"\r{color}[{bar}] {progress:.2f}% Complete  ({i}/{total}){RESET}",
                    end='',
                    flush=True
                )
    # NOTE END: MultiThreaded

    # NOTE START: Single Threaded
    # try:
    #     for itr, address_obj in enumerate(address_list):
    #         try:
    #             address_obj = email.extract_and_update_email(address_obj)
    #             address_string = address_obj.address
    #             # address_string = pincode.pin_code_extender(address_string)
    #             address_string = utils.text_cleaner(address_string, flag_for_translate=flag)
    #             address_string = utils.clean_stopping_words_and_phrases(address_string)

    #             # We are handling numbers below
    #             address_string = numbers_handler.fix_digit_typos(address_string)
    #             # address_string = phone_number.collapse_phone_number_and_pin(address_string)
    #             address_string = pincode.pad_pin_code(address_string, "*", address_obj)
    #             address_string = phone_number.pad_phone_number(address_string, "*", address_obj)
    #             # address_string = numbers_handler.pad_numbers(address_string, address_obj) # this replaces above 3 lines of code

    #             if verbose_mode: print(f"{BLUE}{address_string}{RESET}")
    #             if verbose_mode: print(address_string)

    #             address_string = phone_number.mobile_number_text_remover(address_string)
    #             address_string = pincode.pin_number_text_remover(address_string)
    #             address_obj.address = address_string
    #             pincode.update_pin_number(address_obj)
    #             # print(f"{address_obj.pin}")
                # phone_number.update_phone_number(address_obj, phone_number_lookup)
    #             # print(f"{address_obj.phone}")
    #             address_obj.address = utils.last_text_cleaner(address_obj.address)

    #             #Attribute from address parsing
    #             state_add, dist_add, occ_count = utils.get_data_from_address(address_obj.address)
    #             address_obj.set_state_from_address(state_add)
    #             address_obj.set_district_from_address(dist_add)
    #             address_obj.set_occ_count(occ_count)

    #             address_obj.set_dist_matches_pin_and_addr(utils.is_string_same(dist_add, address_obj.district))
    #             address_obj.set_state_matches_pin_and_addr(utils.is_string_same(state_add, address_obj.state))
    #             address_obj.set_book_name(book_mapper.get_book_from_address_record(address_string))
    #             address_obj.set_book_lang(lang_mapper.get_book_lang_from_address_record(address_string))

    #             address_obj.address = address_obj.address.title()
    #             address_obj_list.append(address_obj)
    #             if verbose_mode:
    #                 print(f"\n{GREEN}[DONE {itr+1}] {WHITE}{address_obj.address}{RESET}\n") # verbose mode
    #             else:
    #                 print(f"{GREEN}[DONE {itr+1}] {WHITE}{address_obj.address[0:100]}{RESET}", end='\r')
    #         except Exception as err:
    #             print(f"\n{RED}[ERROR] {address_obj.address[0:100]}{RESET}")
    #             print(f'{YELLOW}str{err}{RESET}\n')
    # except KeyboardInterrupt:
    #     print(f"\n{RED}[!] Process interrupted by user!{RESET}")
    # NOTE END: Single Threaded

    # address_obj_list.sort(key=lambda x: len(x.address_old), reverse=True) # sort by length of address
    utils.update_reorder_and_repeat(address_obj_list, phone_lookup=phone_number_lookup)
    if os.getenv('NOT_RUNNING_ON_RENDER', 'yes').lower() in ['yes', 'true', '1']:
        phone_number.update_phone_numbers_lookup(phone_number_lookup)

    # Post processing (one more iteration)
    try:
        for adr in address_obj_list:
            adr_str_updated = adr.address
            if mknc_utils.has_name(adr_str_updated):
                adr.name = mknc_utils.get_name(adr_str_updated)
            if mknc_utils.has_book_name(adr_str_updated):
                adr.book_name = mknc_utils.get_book_name(adr_str_updated)
            if mknc_utils.has_book_lang(adr_str_updated):
                adr.book_lang = mknc_utils.get_book_lang(adr_str_updated)
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Post-processing interrupted by user!{RESET}")

    print(f"\n{BLUE}[ phone_number_lookup ✔ ]{RESET}")
    return address_obj_list

def main():
    if not os.path.exists(output_dir): 
        os.makedirs(output_dir)

    flag = sys.argv[1].lower()
    fname = sys.argv[2]
    verbose_mode = False
    if ' -v ' in " "+' '.join(sys.argv)+" ":
        verbose_mode = True

    if flag in ['-f', '-file', '--f', '--file']:
        file_text = utils.read_input_file(fname)
        address_list = process_addresses(file_text, verbose_mode=verbose_mode)

        output_file_path_xls = utils.generate_output_file_path(output_dir, Path(fname).stem, "xlsx")
        ms_office.export_to_MS_Excel(address_list=address_list, file_name=output_file_path_xls)
    
    elif flag in ['-t', '-translate', '--t', '--translate']:
        file_text = utils.read_input_file(fname)
        address_list = process_addresses(file_text, flag=flag, verbose_mode=verbose_mode)

        output_file_path_xls = utils.generate_output_file_path(output_dir, Path(fname).stem, "xlsx")
        ms_office.export_to_MS_Excel(address_list=address_list, file_name=output_file_path_xls)

    elif flag in ['-n', '-name', '--n', '--name']:
        address_list = ms_office.import_from_Excel_sheet(fname)
        for address in address_list:
            utils.update_address_name(address)
        ms_office.export_to_MS_Excel(address_list, str(fname.split(".")[0] + "_name.xls"))
    
    elif flag in ['-m', '-modified', '-modify', '--m', '--modified', '--modify', '-mod', '--mod']:
        file_text = utils.read_input_file(fname)
        address_list = process_addresses(file_text, flag='-m', verbose_mode=verbose_mode)

        output_file_path_xls = utils.generate_output_file_path(output_dir, Path(fname).stem, "xlsx")
        ms_office.export_to_MS_Excel(address_list=address_list, file_name=output_file_path_xls)

    else:
        print(f"{RED}[!] Invalid argument{RESET}")
        print(f"{RED}[-file, -f, --f, --file]: for file processing \n[-name, -n, --n, --name]: generate name column{RESET}")
        print(f"{RED}[Example]: python main.py -f whatsapp.txt{RESET}")


if __name__ == "__main__":
    main()
