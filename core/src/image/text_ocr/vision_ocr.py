class TextOcrVisionOcr:
    def __init__(self, azure_services):
        self.azure_services = azure_services

    async def run_async(self, image_stream):
        read_response = self.azure_services.vision_client.recognize_printed_text_in_stream(image_stream)
        return read_response

        