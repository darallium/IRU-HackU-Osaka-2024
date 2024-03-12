import fs from "fs";
import path from "path";

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
