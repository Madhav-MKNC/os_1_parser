# Number mapper for langs other than english

# from googletrans import Translator


class LangConverter:
    def __init__(self):
        # self.translator = Translator()
        self.digit_maps = {
            'english': {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'},
            'hindi': {'०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'},
            'tamil': {'௦': '0', '௧': '1', '௨': '2', '௩': '3', '௪': '4', '௫': '5', '௬': '6', '௭': '7', '௮': '8', '௯': '9'},
            'telugu': {'౦': '0', '౧': '1', '౨': '2', '౩': '3', '౪': '4', '౫': '5', '౬': '6', '౭': '7', '౮': '8', '౯': '9'},
            'kannada': {'೦': '0', '೧': '1', '೨': '2', '೩': '3', '೪': '4', '೫': '5', '೬': '6', '೭': '7', '೮': '8', '೯': '9'},
            'malayalam': {'൦': '0', '൧': '1', '൨': '2', '൩': '3', '൪': '4', '൫': '5', '൬': '6', '൭': '7', '൮': '8', '൯': '9'},
            'bengali': {'০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4', '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9'},
            'gujarati': {'૦': '0', '૧': '1', '૨': '2', '૩': '3', '૪': '4', '૫': '5', '૬': '6', '૭': '7', '૮': '8', '૯': '9'},
            'punjabi': {'੦': '0', '੧': '1', '੨': '2', '੩': '3', '੪': '4', '੫': '5', '੬': '6', '੭': '7', '੮': '8', '੯': '9'},
            'odia': {'୦': '0', '୧': '1', '୨': '2', '୩': '3', '୪': '4', '୫': '5', '୬': '6', '୭': '7', '୮': '8', '୯': '9'}
        }

    def normalize_other_lang_numbers(self, input_string):
        """
        Converts numbers in the input string from different languages to English digits.
        
        The method loops through the input and identifies digits in different scripts, 
        converting them to English digits.
        """
        result = []
        
        # Loop through each character in the input string
        for char in input_string:
            # Check if the character is a digit from any non-English numeral system
            converted = char  # Default to the original character

            for language, digit_map in self.digit_maps.items():
                if char in digit_map:
                    converted = digit_map[char]
                    break  # Once a match is found, no need to check further maps

            result.append(converted)

        return ''.join(result)


    def translate_text(self, text):
        # translated = self.translator.translate(text, src='auto', dest='en')
        # return translated.text
        return text


# Example usage
if __name__ == "__main__":
    converter = LangConverter()

    # Test with mixed language numbers
    text = "hello mknc"
    print(f"Original Text: {text}")
    print(f"Converted Text: {converter.normalize_other_lang_numbers(text)}")
    print(f"Translated Text: {converter.translate_text(converter.normalize_other_lang_numbers(text))}")

