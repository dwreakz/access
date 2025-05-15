#!/usr/bin/env python3

import sys
import time
from config       import load_config, save_config
from rfid_reader  import RFIDReader
from hw_control   import HWControl
import gui
import cli

class AccessStateMachine:
    def __init__(self, cfg, reader, hw):
        self.cfg         = cfg
        self.reader      = reader
        self.hw          = hw
        self.enroll_mode = False

    def run(self):
        gui.update('IDLE')
        try:
            while True:
                if not self.enroll_mode:
                    tag = self.reader.get_tag()
                    if tag:
                        if tag == self.cfg.master_tag:
                            self.enroll_mode = True
                            gui.update('ENROLL')
                            print(">> Entered enrollment mode")
                        else:
                            self._handle_access(tag)
                    time.sleep(0.1)

                else:
                    # ENROLL: watch each door’s button
                    for idx, door in enumerate(self.cfg.doors):
                        if self.hw.is_button_pressed(idx):
                            gui.update('SELECT_DOOR', door.name)
                            print(f">> Programming door: {door.name}")
                            new_tag = self._wait_for_tag()
                            if new_tag:
                                if new_tag in door.allowed_tags:
                                    door.allowed_tags.remove(new_tag)
                                    print(f"   Removed {new_tag} from {door.name}")
                                else:
                                    door.allowed_tags.append(new_tag)
                                    print(f"   Added {new_tag} to {door.name}")
                                save_config(self.cfg)
                                gui.update('ENROLL')
                            else:
                                print("   → Enrollment timed out")
                            time.sleep(0.5)

                    # Exit ENROLL on master tag
                    tag2 = self.reader.get_tag()
                    if tag2 == self.cfg.master_tag:
                        self.enroll_mode = False
                        gui.update('IDLE')
                        print(">> Exited enrollment mode")
                    time.sleep(0.1)

        except KeyboardInterrupt:
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
    cfg     = load_config('config.json')
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
