from dataclasses import dataclass, field
from typing import Any, Dict, List, Union

@dataclass
class UserSetting:
    name: str
    value: Any
    description: str
    type: str
    accessibility: str
    group: str
    icon: str

@dataclass
class StaticSettings:
    setting_1: str
    setting_2: int

@dataclass
class PageMappingEntry:
    widget_ref: str
    enabled: bool
    index: int
    icon: str
    selectable: bool
    license_required: bool

@dataclass
class PageMapping:
    defaults: Dict[str, PageMappingEntry] = field(default_factory=dict)
    plugins: Dict[str, PageMappingEntry] = field(default_factory=dict)