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
			}
		}

	def parser(self):
		parser = ArgumentParser(description = "Update and check DNS's A records on Route53. Change EC2 Instances types.")

		subparsers = parser.add_subparsers(help = 'DNS & EC2 Actions')

		return parser.parse_args()