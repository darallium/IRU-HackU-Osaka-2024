import fs from "fs";
import { promisify } from "util";

const readFile = promisify(fs.readFile);
const writeFile = promisify(fs.writeFile);

export default async function handler(req, res) {
  if (req.method === "PUT") {
    const key = req.body.key;
    const newValue = req.body.value;

    try {
      const data = await readFile(
        "/home/yutodama/testapp/web-ui/public/config.json",
        "utf8",
      );
      const config = JSON.parse(data);
      config[key] = newValue;
      await writeFile(
        "/home/yutodama/testapp/web-ui/public/config.json",
        JSON.stringify(config, null, 2),
        "utf8",
      );
      res.status(200).send("Config updated successfully");
    } catch (err) {
      res.status(500).send("Error reading or writing to config file");
    }
  } else {
    res.status(405).send("Method not allowed");
  }
}
