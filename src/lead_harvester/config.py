from __future__ import annotations

import os
import yaml
from dataclasses import dataclass, field

@dataclass(slots=True)
class Settings:
    database_path: str = "leads_v2.sqlite3"
    google_places_api_key: str = field(default_factory=lambda: os.getenv("GOOGLE_PLACES_API_KEY", ""))
    job_config_path: str = ""
    job_config: dict = field(default_factory=dict)
    
    def load_job_config(self):
        if self.job_config_path and os.path.exists(self.job_config_path):
            with open(self.job_config_path, "r", encoding="utf-8") as f:
                self.job_config = yaml.safe_load(f)
