# cli.py - simplified version
import argparse

def check_enrollment_flag():
    """Check if --manage flag is set and return result"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--manage', action='store_true',
                        help="Start in enrollment mode")
    args, _ = parser.parse_known_args()
    return args.manage