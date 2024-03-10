default_config = {
    "vision_key": "default_vision_key",
    "vision_endpoint": "default_vision_endpoint",
    "translator_key": "default_translator_key",
    "translator_endpoint": "https://api.cognitive.microsofttranslator.com/",
    "log_dir": "logs",
    "log_level": "DEBUG",
    "target_language": "ja", #https://learn.microsoft.com/ja-jp/azure/ai-services/translator/language-support
    "ocr_interval": 10,
    "ocr_read_operation_check_interval": 0.3,
    "enable_datasaver": False, #resize
    "debug_mode": False, #画面をフルスクリーンじゃなくて半分サイズのウィンドで表示
    "font_path": "C:\\Windows\\Fonts\\msgothic.ttc",
}

valid_values = {
    "log_level": ["FRAME", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
}