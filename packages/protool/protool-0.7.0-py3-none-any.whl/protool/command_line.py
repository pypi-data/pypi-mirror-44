#!/usr/bin/env python3

import argparse
import json
import os
import sys

import protool


def _handle_diff(args):
    """Handle the diff sub command."""

    if len(args.profiles) != 2:
        print("Expected 2 profiles for diff command")
        sys.exit(1)

    try:
        print(protool.diff(args.profiles[0], args.profiles[1], ignore_keys=args.ignore, tool_override=args.tool))
    except Exception as ex:
        print(f"Could not diff: {ex}", file=sys.stderr)


def _handle_git_diff(args):
    """Handle the gitdiff sub command."""

    try:
        print(protool.diff(args.git_args[1], args.git_args[4], ignore_keys=args.ignore, tool_override=args.tool))
    except Exception as ex:
        print(f"Could not diff: {ex}", file=sys.stderr)


def _handle_read(args):
    """Handle the read sub command."""

    try:
        value = protool.value_for_key(args.profile, args.key)
    except Exception as ex:
        print(f"Could not read file: {ex}", file=sys.stderr)

    regular_types = [str, int, float]
    found_supported_type = False

    for regular_type in regular_types:
        if isinstance(value, regular_type):
            found_supported_type = True
            print(value)
            break

    if not found_supported_type:
        try:
            result = json.dumps(value)
        except:
            print("Unable to serialize values. Please use the XML format instead.", file=sys.stderr)
            sys.exit(1)

        print(result)


def _handle_decode(args):
    """Handle the decode sub command."""
    try:
        print(protool.decode(args.profile))
    except Exception as ex:
        print(f"Could not decode: {ex}", file=sys.stderr)


def _handle_arguments():
    """Handle command line arguments and call the correct method."""

    print(sys.argv)

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    diff_parser = subparsers.add_parser('diff', help="Perform a diff between two profiles")
    diff_parser.add_argument("-i", "--ignore", dest="ignore", action="store", nargs='+', default=None, help='A list of keys to ignore. e.g. --ignore TimeToLive UUID')
    diff_parser.add_argument("-t", "--tool", dest="tool", action="store", default=None, help='Specify a diff command to use. It should take two file paths as the final two arguments. Defaults to opendiff')
    diff_parser.add_argument("-p", "--profiles", dest="profiles", action="store", nargs=2, required=True, help='The two profiles to diff')
    diff_parser.set_defaults(subcommand="diff")

    diff_parser = subparsers.add_parser('gitdiff', help="Perform a diff between two profiles with the git diff parameters")
    diff_parser.add_argument("-i", "--ignore", dest="ignore", action="store", nargs='+', default=None, help='A list of keys to ignore. e.g. --ignore TimeToLive UUID')
    diff_parser.add_argument("-t", "--tool", dest="tool", action="store", default=None, help='Specify a diff command to use. It should take two file paths as the final two arguments. Defaults to opendiff')
    diff_parser.add_argument("-g", "--git-args", dest="git_args", action="store", nargs=7, required=True, help='The arguments from git')
    diff_parser.set_defaults(subcommand="gitdiff")

    read_parser = subparsers.add_parser('read', help="Read the value from a profile using the key specified command")
    read_parser.add_argument("-p", "--profile", dest="profile", action="store", required=True, help='The profile to read the value from')
    read_parser.add_argument("-k", "--key", dest="key", action="store", required=True, help='The key to read the value for')
    read_parser.set_defaults(subcommand="read")

    decode_parser = subparsers.add_parser('decode', help="Decode a provisioning profile and display in a readable format")
    decode_parser.add_argument("-p", "--profile", dest="profile", action="store", required=True, help='The profile to read the value from')
    decode_parser.set_defaults(subcommand="decode")

    args = parser.parse_args()

    try:
        _ = args.subcommand
    except:
        parser.print_help()
        sys.exit(1)

    if args.subcommand == "diff":
        _handle_diff(args)
    elif args.subcommand == "gitdiff":
        _handle_git_diff(args)
    elif args.subcommand == "read":
        _handle_read(args)
    elif args.subcommand == "decode":
        _handle_decode(args)

def run():
    _handle_arguments()

if __name__ == "__main__":
    _handle_arguments()
