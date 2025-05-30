# cli.py

import argparse
import threading

def check_enrollment_flag():
    """Check if --manage flag is set and return result"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--manage', action='store_true',
                        help="Start in enrollment mode")
    args, _ = parser.parse_known_args()
    return args.manage

# For backward compatibility
def start_enrollment_thread(machine):
    """
    If launched with `--manage`, puts FSM into enroll mode immediately.
    """
    def _run():
        if check_enrollment_flag():
            machine.enroll_mode = True

    t = threading.Thread(target=_run, daemon=True)
    t.start()