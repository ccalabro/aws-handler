#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from boto.ec2.connection import EC2Connection
from boto.route53.connection import Route53Connection
from boto.route53.record import ResourceRecordSets

class Amazon():
	""" Class to interact with AWS """

	def __init__(self, aws_access_key_id, aws_secret_access_key):
		"""
        Init method to create a new connection to EC2.
        """
		self.route53conn = Route53Connection(aws_access_key_id, aws_secret_access_key)
		self.ec2Conn = EC2Connection(aws_access_key_id, aws_secret_access_key)

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
		rrs = self.route53conn.get_all_rrsets(zone_id)
		current_dns = {}
		for record in rrs:
			record_name = record.name[:-1]
			if record_name == domain and record.type == 'A':
				current_dns[record_name] = {
					'destination': record.resource_records[0],
					'type': record.type
				}

		return current_dns
