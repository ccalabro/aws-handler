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