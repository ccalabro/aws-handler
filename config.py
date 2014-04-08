#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from argparse import ArgumentParser

args = None

scale_values = ['up', 'down']

class Config:
	"""Configuration class."""

	def __init__(self):
		global args
		args = self.parser()

		self.data = {
			'database': {
				'host': '<HOST_HERE>',
				'user': '<USER_HERE>',
				'pass': '<PASS_HERE>',
				'name': '<DB_NAME_HERE>'
			},
			'aws': {
				'key_name': '<KEY_NAME_HERE>',
				'secret_key': '<SECRET_KEY_HERE>'
			}
		}

		self.set()

	def parser(self):
		parser = ArgumentParser(description = "Update and check DNS's A records on Route53. Change EC2 Instances types.")

		subparsers = parser.add_subparsers(help = 'DNS & EC2 Actions')

		check_parser = subparsers.add_parser('check', help = 'DNS Checking.')
		check_parser.set_defaults(which = 'check')
		check_parser.add_argument('domains', help = 'Domains to check. Can be a list. (ex: domain1, domain2, domain3) or "all"')

		modify_parser = subparsers.add_parser('modify', help = 'DNS Modification.')
		modify_parser.set_defaults(which = 'modify')
		modify_parser.add_argument('domains', help = 'Domains to modify. Can be a list. (ex: domain1, domain2, domain3) or "all"')
		modify_parser.add_argument('server', help = 'Destination Server Name.')

		scale_parser = subparsers.add_parser('scale', help = 'Scale up or Scale down a EC2 Instance.')
		scale_parser.set_defaults(which = 'scale')
		scale_parser.add_argument('server', help = 'Server Name to scale.')
		scale_parser.add_argument('type', choices = scale_values, help = 'Scale type (up or down).')

		return parser.parse_args()

	def set(self):
		# task to perform
		setattr(self, 'action', args.which)

		# domains
		if 'domains' in args:
			setattr(self, 'domains', self.prepare_domains_list())

		# server
		if 'server' in args:
			setattr(self, 'server', args.server)

		# scale type
		if 'type' in args:
			setattr(self, 'type', args.type)

	def prepare_domains_list(self):
		return args.domains.split(',')