import json
import util.logger as logger
import util.config as config
from azure.ai.translation.text.models import InputTextItem

class TextTranslator:
    def __init__(self, azure_services):
        self.azure_services = azure_services
        self.translation_cache = {}
        self.user_dictionary = {}
        self.cache_file = "translation_cache.json"
        self.dictionary_file = "user_dictionary.json"
        self.target_language = config.value_of("target_language")
        self.load_cache()
        self.load_dictionary()

    def translate_ocr_result(self, ocr_result):
        self.target_language = config.value_of("target_language")
        
        # 翻訳するテキストのリストを初期化
        texts_to_translate = []

        if type(ocr_result) == self.azure_services.read_operation_result:
            for read_results in ocr_result.analyze_result.read_results:
                for line in read_results.lines:
                    text = line.text  # テキストを取得
                    key = f"{self.target_language}_{text}"
                    # キャッシュが存在しない場合のみリストに追加
                    if key not in self.translation_cache:
                        texts_to_translate.append([key, text])
        else:
            for region in ocr_result.regions:
                for line in region.lines:
                    text = ' '.join([word.text for word in line.words])  # 単語を一文に結合
                    key = f"{self.target_language}_{text}"
                    # キャッシュが存在しない場合のみリストに追加
                    if key not in self.translation_cache:
                        texts_to_translate.append([key, text])

        if texts_to_translate:
            # Azure Translateの上限に達するまで、または全てのテキストを翻訳する
            translated_texts = self.azure_services.translator_client.translate(content=[InputTextItem(text=item[1]) for item in texts_to_translate], to=[self.target_language])

            # 翻訳結果をキャッシュに追加
            for (key, _), translated_text in zip(texts_to_translate, translated_texts):
                self.translation_cache[key] = (translated_text.translations[0].text, translated_text.detected_language.language)
                logger.info(f"Translator: key:'{key}' detected_language:'{self.translation_cache[key][1]}' translated_text:'{self.translation_cache[key][0]}'")
            self.save_cache()
        return
    
    def translate(self, text, source_language):
        self.target_language = config.value_of("target_language")
        key = f"{self.target_language}_{text}"

        if source_language == self.target_language:
            return (text, source_language)
        
        if key in self.user_dictionary:
            logger.frame("Using user dictionary.")
            return self.user_dictionary[key]
        elif key in self.translation_cache:
            logger.frame("Using translation cache.")
            return self.translation_cache[key]
        
        logger.warning(f"All text should be pre-cached, but {text} is not cached.")

        input_text_elements = [InputTextItem(text=text)]

        response = self.azure_services.translator_client.translate(content=input_text_elements, to=[self.target_language], from_parameter=source_language)
        translation = response[0] if response else None
        if translation:
            for translated_text in translation.translations:
                logger.info(f"'{text}' was translated to: '{translated_text.to}' and the result is: '{translated_text.text}'.")
                self.translation_cache[key] = (translated_text.text, translation.detected_language.language)
        self.save_cache()

        return self.translation_cache[key]

    def add_to_dictionary(self, source_language, text, translation):
        key = f"{source_language}_{self.target_language}_{text}"
        self.user_dictionary[key] = translation
        self.save_dictionary()

    def remove_from_dictionary(self, source_language, text):
        key = f"{source_language}_{self.target_language}_{text}"
        if key in self.user_dictionary:
            del self.user_dictionary[key]
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
