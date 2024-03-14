from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials


from array import array
import os
from PIL import Image, ImageDraw
import sys
import time
import json
import util.logger as logger
import util.config as config


class TextOcrVisionRead:
    def __init__(self, azure_services):
        self.azure_services = azure_services

    async def run(self, image_stream):
        read_response = self.azure_services.vision_client.read_in_stream(image_stream, raw=True)
        logger.debug(read_response)
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]
        logger.info(f"ocr operation_id {operation_id}")

        read_result = self.azure_services.vision_client.get_read_result(operation_id)
        while read_result.status not in ['succeeded', 'failed']:
            logger.debug(f"ocr operation status: {read_result.status}")
            time.sleep(config.value_of("ocr_read_operation_check_interval"))
            read_result = self.azure_services.vision_client.get_read_result(operation_id)

        if read_result.status == OperationStatusCodes.succeeded:
            return read_result
