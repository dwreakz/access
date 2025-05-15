import json

class Door:
    def __init__(self, name, relay_pin, button_pin, allowed_tags=None):
        self.name         = name
        self.relay_pin    = relay_pin
        self.button_pin   = button_pin
        self.allowed_tags = allowed_tags or []

class Config:
    def __init__(self, master_tag, doors, enroll_timeout_s, relay_pulse_ms, filepath):
        self.master_tag       = master_tag
        self.doors            = doors
        self.enroll_timeout_s = enroll_timeout_s
        self.relay_pulse_ms   = relay_pulse_ms
        self.filepath         = filepath

def load_config(path):
    with open(path, 'r') as f:
        data = json.load(f)

    master_tag = data['master_tag']
    settings   = data.get('settings', {})
    enroll_to  = settings.get('enroll_timeout_s', 30)
    relay_ms   = settings.get('relay_pulse_ms', 500)

    doors = []
    for d in data['doors']:
        doors.append(Door(
            name         = d['name'],
            relay_pin    = d['relay_pin'],
            button_pin   = d['button_pin'],
            allowed_tags = d.get('allowed_tags', [])
        ))

    return Config(master_tag, doors, enroll_to, relay_ms, path)

def save_config(cfg: Config):
    data = {
        'master_tag': cfg.master_tag,
        'doors': [],
        'settings': {
            'enroll_timeout_s': cfg.enroll_timeout_s,
            'relay_pulse_ms':   cfg.relay_pulse_ms
        }
    }
    for d in cfg.doors:
        data['doors'].append({
            'name':         d.name,
            'relay_pin':    d.relay_pin,
            'button_pin':   d.button_pin,
            'allowed_tags': d.allowed_tags
        })
    with open(cfg.filepath, 'w') as f:
        json.dump(data, f, indent=2)
