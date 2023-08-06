'''
setup.py - a setup script
Author: Xinyu Wang
'''

from setuptools import setup, find_packages

import os
import sys
# import BGP_Forecast_Modules

try:
	setup(
		name='UConnMLHI_UKBiobankProject',
		version='0.0.2',
		author='Xinyu Wang',
		author_email='xinyuwang1209@gmail.com',
		description = ("UConnMLHI_UKBiobankProject."),
		url='https://github.com/xinyuwang1209/UConnMLHI_UKBiobankProject.git',
		platforms = 'any',
		classifiers=[
			'Environment :: Console',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: MIT License',
			'Operating System :: OS Independent',
			'Programming Language :: Python',
			'Programming Language :: Python :: 3'
		],
		keywords=['Xinyu, xinyu, pypi, package, rpki'],
		packages=find_packages(include=['UConnMLHI_UKBiobankProject', 'UConnMLHI_UKBiobankProject.*']),
		# install_requires=[
		# 	'numpy',
		# 	'pandas',
		# 	'pathos',
		# ],

		)
finally:
	pass
