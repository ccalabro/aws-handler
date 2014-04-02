#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from argparse import ArgumentParser

args = None

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
		check_parser.add_argument('domains', help='Domains to check. Can be a list. (ex: domain1, domain2, domain3) or "all"')

		return parser.parse_args()

	def set(self):
		# task to perform
		setattr(self, 'action', args.which)

		# domains
		if 'domains' in args:
			setattr(self, 'domains', self.prepare_domains_list())

	def prepare_domains_list(self):
		return args.domains.split(',')