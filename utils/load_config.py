import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

def load_report_config(config_path):
    """
    Loads report config from a JSON file and substitutes ${ENV_VAR} values.
    """
    if not config_path or not os.path.exists(config_path):
        raise FileNotFoundError(f"[ERROR] REPORT_CONFIG_PATH not found: {config_path}")
    
    with open(config_path, "r") as f:
        config_text = f.read()

    # Replace placeholders like ${VAR} with values from .env
    config_text = re.sub(
        r"\$\{(\w+)\}",
        lambda m: os.getenv(m.group(1), ""),
        config_text
    )

    config = json.loads(config_text)

    # Auto-cast numeric strings to int where possible
    for section in config:
        options = section.get("options", {})
        for key, value in options.items():
            if isinstance(value, str) and value.isdigit():
                options[key] = int(value)

    return config
