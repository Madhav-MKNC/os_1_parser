class LanguageMapper:
    def __init__(self):
        self.dictionary = {
            "hindi": "Hindi",
            "-hindi": "Hindi",
            "हिंदी": "Hindi",
            "हिन्दी": "Hindi",
            "assamese": "Assamese",
            "asames": "Assamese",
            "bengali": "Bengali",
            "bangali": "Bengali",
            "english": "English",
            "gujrati": "Gujarati",
            "gujarati": "Gujarati",
            "ગુજરાતી": "Gujarati",
            "kannada": "Kannada",
            "kannad": "Kannada",
            "kaanad": "Kannada",
            "urdu": "Urdu",
            "उर्दू": "Urdu",
            "marathi": "Marathi",
            "मराठी": "Marathi",
            "nepali": "Nepali",
            "नेपाली": "Nepali",
            "oriya": "Odia",
            "orria": "Odia",
            "odia": "Odia",
            "odiya": "Odia",
            "oddia": "Odia",
            "punjabi": "Punjabi",
            "panjabi": "Punjabi",
            "पंजाबी": "Punjabi",
            "malyalam": "Malayalam",
            "malayalam": "Malayalam",
            "telugu": "Telugu",
            "thelugu": "Telugu",
            "thalagu": "Telugu",
            "thalugu": "Telugu",
            "talugu": "Telugu"
        }

    def get_book_lang_from_address_record(self, address_string):
        address_list_token = address_string.split(" ")
        if address_list_token is not None and len(address_list_token) > 0:
            for token in address_list_token:
                if token is not None and len(token) > 0 and self.dictionary.get(token.lower()) is not None:
                    return self.dictionary.get(token.lower())