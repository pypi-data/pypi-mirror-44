import os
from setuptools import setup

cwd = os.getcwd()
try:
	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	setup(
		name = 'peachapisec-ci',
		description = 'Peach API Security CI tool',
		long_description = open('README.rst').read(),
		author = 'Peach Tech',
		author_email = 'contact@peach.tech',
		url = 'https://peach.tech',
		version = '1.5.40',

		py_modules = ['peach_ci_runner'],

		# update requirements.txt as well!
		install_requires = [
			'click~=6.7', 
			'peachapisec-api==1.5.40', 
			'requests>=2.18.4',
			],
		entry_points = {
			'console_scripts': ['peachci=peach_ci_runner:run'],
		},

		license = 'Apache License, Version 2.0',
		keywords = 'peach fuzzing security test rest',

		classifiers = [
			'Development Status :: 5 - Production/Stable',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: Apache Software License',
			'Operating System :: OS Independent',
			'Topic :: Security',
			'Topic :: Software Development :: Quality Assurance',
			'Topic :: Software Development :: Testing',
			'Topic :: Utilities',
			'Programming Language :: Python',
			'Programming Language :: Python :: 2',
			'Programming Language :: Python :: 3'
		])

finally:
	os.chdir(cwd)

# end
