# azure_services.py
from azure.cognitiveservices.vision.computervision import ComputerVisionClient, models
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

class AzureServices:
    def __init__(self, vision_key, vision_endpoint, translator_key, translator_endpoint):
        vision_credentials = CognitiveServicesCredentials(vision_key)
        self.vision_client = ComputerVisionClient(vision_endpoint, vision_credentials)
        self.translator_client = TextTranslationClient(credential=TranslatorCredential(translator_key, "japaneast"))
        self.analyze_results = models._models_py3.AnalyzeResults
        self.read_operation_result = models._models_py3.ReadOperationResult
