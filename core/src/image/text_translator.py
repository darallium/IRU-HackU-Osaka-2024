import json
from azure.ai.translation.text.models import InputTextItem

class TextTranslator:
    def __init__(self, azure_services):
        self.azure_services = azure_services
        self.translation_cache = {}
        self.user_dictionary = {}
        self.cache_file = "translation_cache.json"
        self.dictionary_file = "user_dictionary.json"
        self.load_cache()
        self.load_dictionary()

    def translate(self, text, source_language, target_language):
        if (source_language, target_language, text) in self.user_dictionary:
            return self.user_dictionary[(source_language, target_language, text)]
        elif (source_language, target_language, text) in self.translation_cache:
            return self.translation_cache[(source_language, target_language, text)]

        input_text_elements = [InputTextItem(text=text)]

        response = self.azure_services.translator_client.translate(content=input_text_elements, to=target_language, from_parameter=source_language)
        translation = response[0] if response else None
        if translation:
            for translated_text in translation.translations:
                print(f"Text was translated to: '{translated_text.to}' and the result is: '{translated_text.text}'.")
                translated_text = translated_text.text

        self.translation_cache[(source_language, target_language, text)] = translated_text
        self.save_cache()

        return translated_text

    def add_to_dictionary(self, source_language, target_language, text, translation):
        self.user_dictionary[(source_language, target_language, text)] = translation
        self.save_dictionary()

    def remove_from_dictionary(self, source_language, target_language, text):
        if (source_language, target_language, text) in self.user_dictionary:
            del self.user_dictionary[(source_language, target_language, text)]
            self.save_dictionary()

    def clear_dictionary(self):
        self.user_dictionary = {}
        self.save_dictionary()

    def load_cache(self):
        try:
            with open(self.cache_file, 'r') as f:
                self.translation_cache = json.load(f)
        except FileNotFoundError:
            self.translation_cache = {}

    def save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.translation_cache, f)

    def load_dictionary(self):
        try:
            with open(self.dictionary_file, 'r') as f:
                self.user_dictionary = json.load(f)
        except FileNotFoundError:
            self.user_dictionary = {}

    def save_dictionary(self):
        with open(self.dictionary_file, 'w') as f:
            json.dump(self.user_dictionary, f)
