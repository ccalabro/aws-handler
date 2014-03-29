#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import MySQLdb

class DataBase():
	""" Class to interact with relational database """

	def __init__(self, host, user, dbPass, name, port = 3306):
		"""
        Init method to create a new connection to MySQL Database.
        """
		connection = MySQLdb.connect(host=host, user=user, passwd=dbPass, db=name, charset="utf8", init_command="set names utf8", port=port)
		self.cursor = connection.cursor(MySQLdb.cursors.DictCursor)