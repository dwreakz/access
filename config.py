# config.py - simplified version
import json
from dataclasses import dataclass, asdict, field
from typing import List

@dataclass
class Door:
    name: str
    relay_pin: int
    button_pin: int
    allowed_tags: List[str] = field(default_factory=list)

@dataclass
class Config:
    master_tag: str
    doors: List[Door]
    enroll_timeout_s: int = 30
    relay_pulse_ms: int = 500
    filepath: str = "config.json"
    
    @classmethod
    def load(cls, path):
        with open(path, 'r') as f:
            data = json.load(f)
        
        doors = [Door(**d) for d in data['doors']]
        settings = data.get('settings', {})
        
        return cls(
            master_tag=data['master_tag'],
            doors=doors,
            enroll_timeout_s=settings.get('enroll_timeout_s', 30),
            relay_pulse_ms=settings.get('relay_pulse_ms', 500),
            filepath=path
        )
    
    def save(self):
        data = {
            'master_tag': self.master_tag,
            'doors': [asdict(d) for d in self.doors],
            'settings': {
                'enroll_timeout_s': self.enroll_timeout_s,
                'relay_pulse_ms': self.relay_pulse_ms
            }
        }
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)