import fs from "fs";
//import fs from "node:fs/promises";
import path from "path";

import addFormats from 'ajv-formats';
import { Ajv, JSONSchemaType } from "ajv";
import * as jctt from "json-schema-to-ts";
import {wrapCompilerAsTypeGuard} from "json-schema-to-ts";

const schema = {
  "type": "object",
  "additionalProperties": false,
  "required": [
    "vision_key",
    "vision_endpoint",
    "translator_key",
    "translator_endpoint",
    "log_dir",
    "log_level",
    "target_language",
    "always_ocr",
    "ocr_method",
    "ocr_interval",
    "ocr_read_operation_check_interval",
    "enable_datasaver",
    "camera_device_id",
    "debug_mode",
    "font_url",
    "font_path",
    "overlay_alpha",
    "audio_channels"
  ],
  "properties": {
    "vision_key": {
      "type": "string" ,
      "pattern": "^[a-f0-9]{32}$",
      "default": "default_vision_key"
    },
    "vision_endpoint": {
      "type": "string" ,
      "pattern": "^https://[a-z0-9-]+.cognitiveservices.azure.com/$",
      "default": "default_vision_endpoint"
    },
    "translator_key": { 
      "type": "string",
      "pattern": "^[a-f0-9]{32}$",
      "default": "default_translator_key"
    },
    "translator_endpoint": { 
      "type": "string" ,
      "pattern": "^https://api.cognitive.microsofttranslator.com/$",
      "default": "https://api.cognitive.microsofttranslator.com/"
    },
    "log_dir": { 
      "type": "string",
      "default": "logs"
    },
    "log_level": {
      "type": "string", 
      "enum": [
        "FRAME", 
        "DEBUG", 
        "INFO", 
        "WARNING", 
        "ERROR", 
        "CRITICAL"
      ],
      "default": "WARNING"
    },
    "target_language": { 
      "type": "string",
      "default": "ja"
    },
    "always_ocr": {
      "type": "boolean",
      "default": true,
    },
    "ocr_method": {
      "type": "string", 
      "enum": [
        "vision_read", 
        "vision_ocr", 
        "document"
      ],
      "default": "vision_read"
    },
    "ocr_interval": {
      "type": "number" ,
      "default": 3
    },
    "ocr_read_operation_check_interval": { 
      "type": "number",
      "default": 0.3

    },
    "enable_datasaver": { 
      "type": "boolean",
      "default": false
    },
    "camera_device_id": {
      "type": "number",
      "default": 0,
      "minimum": 0
    },"
    "debug_mode": { 
      "type": "boolean",
      "default": false
    },
    "font_url": { 
      "type": "string",
      "default": "https://github.com/adobe-fonts/source-han-sans/raw/release/SubsetOTF/JP/SourceHanSansJP-Medium.otf",
    },
    "font_path": { 
      "type": "string",
      "default": "fonts/SourceHanSansJP-Medium.otf"
    },
    "overlay_alpha": { 
      "type": "number",
      "default": 200,
      "minimum": 0,
      "maximum": 255
    },
    "audio_channels": { 
      "type": "number",
      "default": 2,
      "minimum": 0
    }, 
    "audio_format": {
      "type": "string",
      "enum": [
        "S16_LE"
      ]
    },
    "audio_channels": {
      "type": "number",
      "default": 2,
      "minimum": 1
    },
    "audio_buffer_size": {
      "type": "number",
      "default": 1024,
      "minimum": 1
    },
    "audio_sample_rate": {
      "type": "number",
      "default": 48000,
      "minimum": 1
    }
  }
} as const;
export type tconfig = jctt.FromSchema<typeof schema>;

export const getConfig = () => {
  const configPath = path.resolve(process.cwd(), "config.json");

  // Check if the file exists before reading it
  if (fs.existsSync(configPath)) {
    const rawConfig = fs.readFileSync(configPath, "utf-8");
    return JSON.parse(rawConfig);
  } else {
    throw new Error("Config file not found");
  }
};

export const checkConfig = (req: JSON): boolean => {
  const ajv = new Ajv();
  addFormats(ajv);
  const comp: jctt.$Compiler = (schema) => {
    return ajv.compile(schema);
  };
  if(!wrapCompilerAsTypeGuard(comp))
    return false;
  else throw new Error();
  return true;
};

