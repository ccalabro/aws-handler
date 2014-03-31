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

	""" SELECT functions. """

	def get_all(self, cursor, table):
		"""
        Fetch all rows from any table.

		:type cursor: cursor
        :param cursor: Pointer to DB Connection.

        :type table: string
        :param table: SQL Table name.

        :rtype: list
		:return: data.
        """
		tempList = []

		query = 'SELECT * FROM ' + table + ' ORDER BY id DESC;'
		cursor.execute(query)

		for domain in cursor.fetchall():
			tempList.append(domain)
		return tempList

	def get(self, cursor, table, field, value):
		"""
        Fetch information from any table by any field.

		:type cursor: cursor
		:param cursor: Pointer to DB Connection.

		:type table: string
		:param table: SQL Table Name.

		:type field: string
		:param field: SQL Field Table Name.

		:type value: string
		:param value: Value to search.

		:rtype: dict
		:return: Domain Information.
        """
		query = 'SELECT * FROM ' + table + ' WHERE ' + field + ' = "' + str(value) + '";'
		cursor.execute(query)

		return cursor.fetchone()
