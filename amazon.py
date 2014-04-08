#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time

from boto.ec2.connection import EC2Connection
from boto.route53.connection import Route53Connection
from boto.route53.record import ResourceRecordSets

class Amazon():
	""" Class to interact with AWS """

	def __init__(self, aws_access_key_id, aws_secret_access_key):
		"""
        Init method to create a new connection to EC2.
        """
		self.route53_conn = Route53Connection(aws_access_key_id, aws_secret_access_key)
		self.ec2_conn = EC2Connection(aws_access_key_id, aws_secret_access_key)

	def get_current_dns(self, zone_id, domain):
		"""
        Obtain domain status from Route53.

		:type zone_id: string
		:param zone_id: AWS DNS Zone identification.

		:type domain: string
		:param domain: Domain to fetch information.

		:rtype: dict
		:return: Domain DNS information.
        """
		rrs = self.route53_conn.get_all_rrsets(zone_id)
		current_dns = {}
		for record in rrs:
			record_name = record.name[:-1]
			if record_name == domain and record.type == 'A':
				current_dns[record_name] = {
					'destination': record.resource_records[0],
					'type': record.type
				}

		return current_dns

	def modify_dns(self, domain, dest_ip):
		"""
        Modify DNS A record.

		:type domain: dict
		:param domain: Domain to change including their information.

		:type dest_ip: string
		:param dest_ip: Destination IP address.

		:rtype: dict
		:return: ResourceRecordSets object.
        """
		domain_name = domain['name']

		rrs = ResourceRecordSets(self.route53_conn, domain['aws_zone_id'])
		current_dns = self.get_current_dns(domain['aws_zone_id'], domain_name)

		if current_dns[domain_name]['destination'] == dest_ip:
			return False

		#change domain
		change = rrs.add_change("DELETE", domain_name, "A", 300)
		change.add_value(current_dns[domain_name]['destination'])
		change = rrs.add_change("CREATE", domain_name, "A", 300)
		change.add_value(dest_ip)

		return rrs.commit()

	def change_ec2(self, server, scale_type):
		"""
		Wrapper Change EC2 Instance Type function.

		:type connection: EC2Connection Object
		:param connection: object connection to EC2 platform.

		:type ec2_server: dict
		:param ec2_servers: dict containing EC2 instance data.

		:type scale_type: string
		:param scale_type: scale type (up, down).

		:rtype: dict
		:return: ResourceRecordSets object.
		"""
		scale_type = 'instance_type_' + scale_type

		rs = self.ec2_conn.get_all_instances()
		for reservation in rs:
			for instance in reservation.instances:
				if instance.get_console_output().instance_id == server['instance_id']:
					server['instance'] = instance

		if 'instance' in server:
			if self.change_instance_type(server['instance'], server[scale_type]):
				server['instance'].use_ip(server['ip'])

				return True
			else:
				return False
		else:
			return False

	def change_instance_type(self, instance, type):
		"""
		Change EC2 Instance Type.

		:type instance: Instance Object
		:param instance: object EC2 instance to change.

		:type type: string
		:param type: instance type.

		:rtype: boolean
		:return: Change performed (True) or not performed (False).
		"""
		if instance.instance_type == type:
			print "ERROR, instance is already %s." % type
			return False
		else:
			print "Stopping instance"
			instance.stop()
			while instance.update() != 'stopped':
				time.sleep(4)
			print "Modifying instance to %s" % type
			instance.modify_attribute('instanceType', type)
			print "Starting instance"
			instance.start()
			while instance.update() != 'running':
				time.sleep(4)
			print "Instance OK"
			return True