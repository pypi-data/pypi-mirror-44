#!/usr/bin/env python

import setuptools

setuptools.setup(
	name='ebdalia',
	version='0.0.4',
	scripts=['ebdalia'],
	author="Jonathas Hortense",
	author_email="jonathas.hortense@daliaresearch.com",
	description="Elastic Beanstalk ssh cli using the internal IP address",
	# long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/DaliaResearch/ebdalia",
	packages=setuptools.find_packages(),
	install_requires=[
		'awsebcli',
		'boto3'
	],
)
