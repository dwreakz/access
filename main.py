#!/usr/bin/env python3

import sys
import time
from config       import Config
from rfid_reader  import RFIDReader
from hw_control   import HWControl
import gui
import cli

# Simplified main.py state machine logic
class AccessStateMachine:
    def __init__(self, cfg, reader, hw):
        self.cfg = cfg
        self.reader = reader
        self.hw = hw
        self.enroll_mode = False
        
    def run(self):
        gui.update('IDLE')
        try:
            while True:
                if self.enroll_mode:
                    self._handle_enrollment()
                else:
                    self._handle_normal_mode()
                time.sleep(0.1)
        except KeyboardInterrupt:
            self._cleanup()
            
    def _handle_normal_mode(self):
        tag = self.reader.get_tag()
        if not tag:
            return
            
        if tag == self.cfg.master_tag:
            self.enroll_mode = True
            gui.update('ENROLL')
            print(">> Entered enrollment mode")
        else:
            self._handle_access(tag)
            
    def _handle_enrollment(self):
        # Check for exit condition first
        tag = self.reader.get_tag()
        if tag == self.cfg.master_tag:
            self.enroll_mode = False
            gui.update('IDLE')
            print(">> Exited enrollment mode")
            return
            
        # Check door buttons
        for idx, door in enumerate(self.cfg.doors):
            if not self.hw.is_button_pressed(idx):
                continue
                
            gui.update('SELECT_DOOR', door.name)
            print(f">> Programming door: {door.name}")
            new_tag = self._wait_for_tag()
            
            if new_tag:
                self._toggle_tag_for_door(new_tag, door)
                gui.update('ENROLL')
            else:
                print("   → Enrollment timed out")
            time.sleep(0.5)
            break
    
    def _toggle_tag_for_door(self, tag, door):
        if tag in door.allowed_tags:
            door.allowed_tags.remove(tag)
            print(f"   Removed {tag} from {door.name}")
        else:
            door.allowed_tags.append(tag)
            print(f"   Added {tag} to {door.name}")
        self.cfg.save()
    
    def _cleanup(self):
        print("Stopping, cleaning up GPIO…")
        self.hw.cleanup()
        gui.stop()
        sys.exit(0)

    def _handle_access(self, tag):
        allowed = [(i, d.name) for i, d in enumerate(self.cfg.doors)
                   if tag in d.allowed_tags]

        if allowed:
            door_names = ", ".join(name for _, name in allowed)
            gui.update('GRANTED', door_names)
            print(f"GRANTED on: {door_names}")
            for idx, _ in allowed:
                self.hw.unlock(idx, self.cfg.relay_pulse_ms)
            time.sleep(5)
            gui.update('IDLE')
        else:
            gui.update('DENIED')
            print(f"DENIED for tag {tag}")
            time.sleep(5)
            gui.update('IDLE')

        time.sleep(0.5)

    def _wait_for_tag(self):
        start = time.time()
        while time.time() - start < self.cfg.enroll_timeout_s:
            t = self.reader.get_tag()
            if t and t != self.cfg.master_tag:
                return t
            time.sleep(0.1)
        return None


def main():
    # Load and initialize everything
    cfg     = Config.load('config.json')
    reader  = RFIDReader()
    hw      = HWControl(cfg)
    machine = AccessStateMachine(cfg, reader, hw)

    # Optional CLI “--manage” enroll toggle
    cli.start_enrollment_thread(machine)

    # Start the GUI & run the FSM
    gui.start()
    machine.run()

if __name__ == '__main__':
    main()