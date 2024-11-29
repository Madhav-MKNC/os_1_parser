from src.utils import Utils
from src.address import Address
from main import get_address_list
import re 

utils = Utils()


file_text = utils.read_input_file("whatsapp.txt")
addresses = get_address_list(file_text)
# print(addresses[0].print_attributes())

output = ""
for i in addresses:
    output += "\n\n" + str(i.address) + "\n\n"

with open('output.txt', 'w', encoding='utf-8') as file:
    file.write(output)
