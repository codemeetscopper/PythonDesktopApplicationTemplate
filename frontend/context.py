from dataclasses import dataclass
from typing import Optional

@dataclass
class AppContext:
    name: str = "Python Desktop App Template"
    version: str = "v0.1"
    config_path: str = "config/configuration.json"
    logger: Optional[object] = None
    settings: Optional[object] = None
    backend_worker: Optional[object] = None

# Create a single instance to share across your app
ApplicationContext = AppContext()
