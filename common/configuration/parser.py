import json
from typing import Dict, Any
from pathlib import Path
from .models import UserSetting, StaticSettings, PageMapping, PageMappingEntry

class ConfigurationManager:
    _instance = None

    def __new__(cls, config_path: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: str = None):
        if self._initialized:
            return
        self._initialized = True
        self.config_path = config_path or "config/configuration.json"
        self.user_settings: Dict[str, UserSetting] = {}
        self.static_settings: StaticSettings = None
        self.page_mapping: PageMapping = None
        self._load()

    def _load(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        config = data["configuration"]
        self.user_settings = {
            k: UserSetting(**v) for k, v in config["user"].items()
        }
        self.static_settings = StaticSettings(**config["static"])
        pm = data["page_mapping"]
        self.page_mapping = PageMapping(
            defaults={k: PageMappingEntry(**v) for k, v in pm["defaults"].items()},
            plugins={k: PageMappingEntry(**v) for k, v in pm["plugins"].items()},
        )

    def save_user_settings(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["configuration"]["user"] = {
            k: vars(v) for k, v in self.user_settings.items()
        }
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add_page_mapping(self, section: str, name: str, entry: PageMappingEntry):
        mapping = getattr(self.page_mapping, section)
        mapping[name] = entry
        self._save_page_mapping()

    def remove_page_mapping(self, section: str, name: str):
        mapping = getattr(self.page_mapping, section)
        if name in mapping:
            del mapping[name]
            self._save_page_mapping()

    def _save_page_mapping(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for section in ["defaults", "plugins"]:
            data["page_mapping"][section] = {
                k: vars(v) for k, v in getattr(self.page_mapping, section).items()
            }
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)