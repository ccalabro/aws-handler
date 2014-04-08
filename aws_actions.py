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
		domains_list = db.get_all(db.cursor, 'domains')
		if domains_list == []:
			sys.exit('No domains records on database.')
		for d in domains_list:
			config.domains.append(d['name'])

	if config.action == 'check':
		for domain_name in config.domains:
			domain = db.get(db.cursor, 'domains', 'name', domain_name)
			if not domain:
				print "[ERROR] The domain doesn't exist"
				sys.exit(0)

			current_dns = amazon.get_current_dns(domain['aws_zone_id'], domain_name)

			# Get server by IP address
			server = db.get(db.cursor, 'servers', 'ip', current_dns[domain_name]['destination'])

			print domain_name + ' -> ' + server['name'] + ' (' + current_dns[domain_name]['destination'] + ')'

	if config.action == 'modify':
		# Get destination server info
		server_info = db.get(db.cursor, 'servers', 'name', config.server)

		if not server_info:
			print "[ERROR] The server doesn't exist"
			sys.exit(0)

		for domain_name in config.domains:
			# Get domain info
			domain = db.get(db.cursor, 'domains', 'name', domain_name)

			if not domain:
				print "[ERROR] The domain doesn't exist"
				sys.exit(0)

			modification = amazon.modify_dns(domain, server_info['ip'])
			if not modification:
				print '[ERROR] ' + domain['name'] + ' is already in ' + server_info['name']
				continue

			if modification['ChangeResourceRecordSetsResponse']['ChangeInfo']['Status'] != 'PENDING':
				print '[ERROR] ' + domain['name'] + '.'
				continue

			changes = {
				'server_id': server_info['id']
			}
			db.update_by_id(db.cursor, 'domains', changes, domain['id'])

			print '[OK] ' + domain_name

	if config.action == 'scale':
		# Fetch servers to change
		server = db.get(db.cursor, 'servers', 'name', config.server)

		changed = amazon.change_ec2(server, config.type)

		if changed:
			print '[OK] ' + server['name'] + ' was changed succesfully.'
		else:
			print "[ERROR] " + server['name'] + " wasn't changed succesfully."