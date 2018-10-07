#!/usr/local/bin/python3

import os
import sys

from utils import db

import utils.functions
from utils.help import usage
from commands import create, check, update

COMMANDS = {
	'create': create,
	'check': check,
	'update': update
}

def resolve_command(cmd):
	try:
		return COMMANDS[cmd]
	except KeyError:
		return None



def main():

	if len(sys.argv) < 2:
		usage()
		sys.exit(1)
	
	command = sys.argv[1]
	parameters = sys.argv[2:]

	command_handler = resolve_command(command)
	if command_handler is None:
		print(f"\nInvalid command: '{command}'\n")
		usage()
		sys.exit(2)
		
	command_handler(parameters)

main()
