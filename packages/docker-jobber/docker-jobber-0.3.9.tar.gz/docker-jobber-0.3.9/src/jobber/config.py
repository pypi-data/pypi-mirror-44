#	Copyright (C) 2019, Mentice AB
#	See accompanying LICENSE file

import os
import shlex
import jsonmerge
import yaml

default_config = {
	'verbose' : False,
	'host' : '',			# Remote host to run command on
	'default-registry' : '',
	'runtime' : 'nvidia',	# Docker runtime
	'inputs' : [],
	'out' : None,
	'cmd' : None,			# CMD override
	'timeout': None,		# In seconds (None means wait indefinitely)
	'result-image': 'always' # Create a latest-result image based on container exit status: 'success', 'always', 'none' -or- 'never'
}

# Merge schema when merging jobber-config.yml files
config_file_schema = {
	'properties': {
		'credentials': {
			'mergeStrategy': 'append'
		}
	}
}
config_file_strat = jsonmerge.Merger(config_file_schema)

# Merge schema when merging named configs
configs_schema = {
	'properties': {
		'credentials': {
			'mergeStrategy': 'append'
		},
		'inputs': {
			'mergeStrategy': 'append'
		},
		'Xdocker': {
			'mergeStrategy': 'append'
		}
	}
}
configs_strat = jsonmerge.Merger(configs_schema)

def merge_config_file(config, path):
	path = os.path.expanduser(path)
	if os.path.isfile(path):
		with open(path, 'r') as inf:
			dict = yaml.safe_load(inf)
			if dict == None: dict = {}
			config = config_file_strat.merge(config, dict)	# Note: using default merge strategy here
	return config

def find_on_path(dir, filename):
	"""Look for filename searching up through all directories on the path 'dir'.
		
	Returns list of full paths where file exists in parent dirs starting with parent, or an empty list
	"""
	paths = []
	for _ in range(20):
		path = os.path.join(dir, filename)
		if os.path.isfile(path):
			paths.append(path)
		dir, _ = os.path.split(dir)
		if dir == '/': break
	return reversed(paths)	# reverse so paths are ordered from root down to dir

def get_config(config_names=['default']):
	config = merge_config_file(default_config, '~/.config/jobber/jobber-config.yml')
	paths = find_on_path(os.getcwd(), 'jobber-config.yml')
	for path in paths:
		config = merge_config_file(config, path)

	def translate(dic):
		for key, val in dic.items():
			if key in ('Xdocker', 'cmd') and type(val) is str:
				dic[key] = shlex.split(val)
			if key in ('cmd', 'timeout') and type(val) is str and val.lower() == 'none':
				dic[key] = None
			if key == 'credentials':
				for val2 in val:	# val should be a list
					for key3, val3 in list(val2.items()):	# val2 should be a dict
						if key3 == 'password-file':
							del val2[key3]
							with open(os.path.expanduser(val3)) as inf:
								val2['password'] = inf.read()	# Read entire contents of file
	translate(config)

	# Merge configurations
	if 'configs' in config:
		configs = config['configs']
		config_names = list(config_names)		# make a copy
		for name in config_names:
			if name in configs:
				val = configs[name]
				if type(val) is list:
					for nm in val:
						if nm not in config_names:
							config_names.append(nm)
				else:
					translate(val)
					config = configs_strat.merge(config, val)
			elif name != 'default':
				print('warning: config not found: {0}'.format(name))
		del config['configs']	# Remove 'configs' since they're used to populate the config dict itself

	# print('config:')
	# for k, v in config.items():
	# 	print(f'  {k:16} {v}')

	return config