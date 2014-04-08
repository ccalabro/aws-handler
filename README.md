# AWS Handler

This project provides actions related to DNS management and EC2 Instances scale.

## Requirements

* Python 2.7+
* boto - AWS SDK for Python (https://github.com/boto/boto)

## Configuration File:

You must specify database's and aws' connection data on config.py file.

`self.data = {
	'database': {
		'host': 'xxxx',
		'user': 'xxxx',
		'pass': 'xxxx',
		'name': 'xxxx'
	},
	'aws': {
		'key_name': 'xxxx',
		'secret_key': 'xxxx'
	}
}`

The DNS zones must be hosted on Route53.

## Instalation

On Ubuntu:

* Python: apt-get install python
* boto: pip install boto

## Documentation

[Python interface to Amazon Web Services](http://docs.pythonboto.org/en/latest/)
[Github boto](https://github.com/boto/boto)

## Examples

* Check a domain DNS 'A' records status (or domains, can be a list):

	`python aws_actions.py check example1,example2`

* Check DNS 'A' records status for all domains:

	`python aws_actions.py check all`

* Modify a domain DNS 'A' records (or domains, can be a list):

	`python aws_actions.py modify example1.com,example2.com`

* Modify DNS 'A' records for all domains:

	`python aws_actions.py modify all`

* Scale up a specific EC2 instance:

	`python aws_actions.py scale up <host1|host2>`

* Scale down a specific EC2 instance:

	`python aws_actions.py scale down <host1|host2>`

## Contributing

Anyone and everyone is welcome to contribute. Please feel free to contribute with new issues, requests, code fixes or new features.
