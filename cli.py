import threading
import argparse

def start_enrollment_thread(machine):
    """
    If launched with `--manage`, puts FSM into enroll mode immediately.
    """
    def _run():
        parser = argparse.ArgumentParser()
        parser.add_argument('--manage', action='store_true',
                            help="Start in enrollment mode")
        args, _ = parser.parse_known_args()
        if args.manage:
            machine.enroll_mode = True

    t = threading.Thread(target=_run, daemon=True)
    t.start()
