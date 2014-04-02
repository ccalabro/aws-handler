#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Cristian Calabro"
__credits__ = ["Cristian Calabro"]
__version__ = "0.1"
__maintainer__ = "Cristian Calabro"
__email__ = "cristian.calabro@gmail.com"
__status__ = "Development"

import os
import sys

from database import DataBase
from config import Config
from amazon import Amazon

if __name__ == '__main__':
	config = Config()

	dbData = config.data['database']
	awsData = config.data['aws']

	# Connect to MySQL DB
	db = DataBase(dbData['host'], dbData['user'], dbData['pass'], dbData['name'])

	# Connect to AWS
	amazon = Amazon(awsData['key_name'], awsData['secret_key'])

	if hasattr(config, 'domains') and config.domains == ['all']:
		config.domains = []
		domainsList = db.get_all(db.cursor, 'domains')
		if domainsList == []:
			sys.exit('No domains records on database.')
		for d in domainsList:
			config.domains.append(d['name'])

	if config.action == 'check':
		for domain_name in config.domains:
			domain = db.get(db.cursor, 'domains', 'name', domain_name)
			current_dns = amazon.get_current_dns(domain['aws_zone_id'], domain_name)

			# Get server by IP address
			server = db.get(db.cursor, 'servers', 'ip', current_dns[domain_name]['destination'])

			print domain_name + ' -> ' + server['name'] + ' (' + current_dns[domain_name]['destination'] + ')'