# passway.py

import argparse
import random
import string
import sys
import os # Imported for potential file path operations

def generate_password(length, chars):
    """Generates a single password of the specified length."""
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    """Parses command-line arguments and generates/saves passwords."""
    parser = argparse.ArgumentParser(
        description="Passway: A custom password generator.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # --- REQUIRED ARGUMENTS ---

    parser.add_argument(
        '-c',
        type=int,
        required=True,
        dest='length',
        help='The required length (number of characters) for your passwords.'
    )

    # --- OPTIONAL ARGUMENTS ---

    parser.add_argument(
        '-C',
        type=int,
        default=1,
        dest='count',
        help='Number of passwords to generate (default: 1). Max: 200.'
    )

    # NEW ARGUMENT: -s for saving to a file
    parser.add_argument(
        '-s',
        type=str,
        default=None,
        dest='output_file',
        help='Saves the generated passwords to the specified file (e.g., passwords.txt).'
    )


    # --- CHARACTER SET FLAGS (Must specify at least one) ---

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

    if args.count > 200:
        print("Error: Maximum password count (-C) is 200.")
        sys.exit(1)

    if not (args.n or args.U or args.L or args.S):
        print("Error: You must specify at least one character set (-n, -U, -L, or -S).")
        parser.print_help()
        sys.exit(1)

    if args.length < 1:
        print("Error: Password length (-c) must be at least 1.")
        sys.exit(1)

    # --- BUILD CHARACTER SET ---

    allowed_chars = ''
    if args.n:
        allowed_chars += string.digits
    if args.U:
        allowed_chars += string.ascii_uppercase
    if args.L:
        allowed_chars += string.ascii_lowercase
    if args.S:
        allowed_chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'

    # --- GENERATE PASSWORDS ---

    passwords = []
    for _ in range(args.count):
        passwords.append(generate_password(args.length, allowed_chars))

    # --- OUTPUT RESULTS ---

    if args.output_file:
        # Save to file using 'w' mode (write, which overwrites file contents)
        try:
            with open(args.output_file, 'w') as f:
                for idx, password in enumerate(passwords):
                    f.write(f"[{idx + 1:02d}] {password}\n")

            # Print a confirmation message to the terminal
            print(f"\n✅ Successfully generated {args.count} password(s) and saved to: {args.output_file}")

        except IOError as e:
            # Handle potential file writing errors
            print(f"\n❌ Error saving file to {args.output_file}: {e}")
            sys.exit(1)

    else:
        # Print to terminal (default behavior)
        print(f"\n🔑 Generating {args.count} password(s) with length {args.length}...")
        for idx, password in enumerate(passwords):
            print(f"[{idx + 1:02d}] {password}")
        print("\nGeneration complete.")

if __name__ == "__main__":
    main()
