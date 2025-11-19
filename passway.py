# passway.py

import argparse
import random
import string
import sys

def generate_password(length, chars):
    """Generates a single password of the specified length."""
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    """Parses command-line arguments and generates passwords."""
    parser = argparse.ArgumentParser(
        description="Passway: A custom password generator.",
        formatter_class=argparse.RawTextHelpFormatter # Keeps formatting for help text
    )

    # --- REQUIRED ARGUMENTS ---

    # -c (characters, length)
    parser.add_argument(
        '-c',
        type=int,
        required=True,
        dest='length',
        help='The required length (number of characters) for your passwords.'
    )

    # --- OPTIONAL ARGUMENTS ---

    # -C (copies, count)
    parser.add_argument(
        '-C',
        type=int,
        default=1,
        dest='count',
        help='Number of passwords to generate (default: 1). Max: 200.'
    )

    # --- CHARACTER SET FLAGS ---

    # This group requires at least one character set to be specified
    char_group = parser.add_argument_group('Character Sets (Must specify at least one)')

    char_group.add_argument(
        '-n',
        action='store_true',
        help='Include numeric digits (0-9).'
    )

    char_group.add_argument(
        '-U',
        action='store_true',
        help='Include uppercase letters (A-Z).'
    )

    char_group.add_argument(
        '-L',
        action='store_true',
        help='Include lowercase letters (a-z).'
    )

    char_group.add_argument(
        '-S',
        action='store_true',
        help='Include special characters (!@#$%^&*...).'
    )

    args = parser.parse_args()

    # --- VALIDATION ---

    # 1. Validate Password Count (-C)
    if args.count > 200:
        print("Error: Maximum password count (-C) is 200.")
        sys.exit(1)

    # 2. Validate Character Set Selection
    if not (args.n or args.U or args.L or args.S):
        print("Error: You must specify at least one character set (-n, -U, -L, or -S).")
        parser.print_help()
        sys.exit(1)

    # 3. Validate Password Length
    if args.length < 1:
        print("Error: Password length (-c) must be at least 1.")
        sys.exit(1)

    # --- BUILD CHARACTER SET ---

    allowed_chars = ''
    if args.n:
        allowed_chars += string.digits # 0123456789
    if args.U:
        allowed_chars += string.ascii_uppercase # ABC...XYZ
    if args.L:
        allowed_chars += string.ascii_lowercase # abc...xyz
    if args.S:
        # A common set of strong special characters
        allowed_chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'

    # --- GENERATE AND PRINT ---

    print(f"\n🔑 Generating {args.count} password(s) with length {args.length}...")

    for i in range(args.count):
        password = generate_password(args.length, allowed_chars)
        print(f"[{i + 1:02d}] {password}")

    print("\nGeneration complete.")

if __name__ == "__main__":
    main()
