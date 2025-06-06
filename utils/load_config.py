import os
import json
import re
from dotenv import load_dotenv
load_dotenv(override=True)

def load_report_config(config_path):
    """
    Loads a JSON report config file and replaces ${ENV_VAR} placeholders with actual .env values.
    Casts numeric strings in options to integers.
    """
    if not config_path or not os.path.exists(config_path):
        raise FileNotFoundError(f"[ERROR] REPORT_CONFIG_PATH not found: {config_path}")

    with open(config_path, "r") as f:
        config_text = f.read()

    # Substitute ${ENV_VAR} with corresponding environment values
    config_text = re.sub(r"\$\{(\w+)\}", lambda m: os.getenv(m.group(1), ""), config_text)
    config = json.loads(config_text)

    # Auto-cast numeric strings in options
    for section in config:
        section["options"] = {
            k: int(v) if isinstance(v, str) and v.isdigit() else v
            for k, v in section.get("options", {}).items()
        }

    return config