default_config = {
    "vision_key": "default_vision_key",
    "vision_endpoint": "default_vision_endpoint",
    "translator_key": "default_translator_key",
    "translator_endpoint": "https://api.cognitive.microsofttranslator.com/",
    "log_dir": "logs",
    "log_level": "DEBUG",
    "target_language": "ja", #https://learn.microsoft.com/ja-jp/azure/ai-services/translator/language-support
    "always_ocr": False,    #無料版は毎分20回までとかの制限があるので非推奨
    "ocr_method": "vision_read",
    "ocr_interval": 10,
    "ocr_read_operation_check_interval": 0.3,
    "enable_datasaver": False, #enable_resize
    "camera_device_id": 0, #ラズパイでやるなら固定だと思いたい
    "debug_mode": False, #画面をフルスクリーンじゃなくて半分サイズのウィンドで表示
    "font_path": "C:\\Windows\\Fonts\\msgothic.ttc",
    "audio_channels": 2,
    "audio_sample_rate": 48000,
    "input_device_index": 0,
    "output_device_index": 1,
    "audio_buffer_size": 1024,
}

valid_values = {
    "log_level": ["FRAME", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    "ocr_method": ["vision_read", "vision_ocr", "document"],
}