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

class TextOcrVisionRead:
    def __init__(self, azure_services):
        self.vision_client = azure_services.vision_client

    def read_async(self, image_stream):
        read_response = self.vision_client.read_in_stream(image_stream, raw=True)

        print(read_response)
        # Get the operation location (URL with an ID at the end) from the response
        read_operation_location = read_response.headers["Operation-Location"]
        # Grab the ID from the URL
        operation_id = read_operation_location.split("/")[-1]
        logger.info(f"operation_id = {operation_id}")
        # Call the "GET" API and wait for it to retrieve the results 
        while True:
            read_result = self.vision_client.get_read_result(operation_id)
            logger.debug(f"Status: {read_result.status}")
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(0.1)

        # Open the image file again to draw on
        image = Image.open(read_image_path)
        draw = ImageDraw.Draw(image)

        # Print the detected text, line by line
        if read_result.status == OperationStatusCodes.succeeded:

            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    print(line.text)
                    print(line.bounding_box)
                    # Draw a yellow rectangle around the text
                    draw.polygon(line.bounding_box, outline='yellow')