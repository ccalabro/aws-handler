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
import data

from database import DataBase

if __name__ == '__main__':
	dbData = data.data['database']

	# Connect to MySQL DB
	db = DataBase(dbData['host'], dbData['user'], dbData['pass'], dbData['name'])
