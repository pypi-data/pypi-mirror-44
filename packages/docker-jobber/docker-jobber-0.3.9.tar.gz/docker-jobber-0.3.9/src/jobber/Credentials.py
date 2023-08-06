class Credentials(object):
	"""	Keep track of registry and host credentials
	"""
	def __init__(self, jobber):
		self.jobber = jobber
		config = jobber.config.copy()
		self.registries = {}
		self.hosts = {}
		if 'credentials' in config:
			for cred in config['credentials']:	# 'credentials' should be a dict
				cred['__cred__'] = None
				if 'registry' in cred:
					cred['__logged_in__'] = False
					self.registries[cred['registry']] = cred
				elif 'host' in cred:
					self.hosts[cred['host']] = cred

	def create_creds(self):
		""" Create credentials on host
		"""
		pass

	def remove_creds(self):
		""" Logout of all registries and remove all credentials from host file system
		"""
		pass
		
	async def login(self, registry):
		""" Log into a registry if necessary
			Returns 0 on success, 1 on failure
		"""
		# print(f'login {registry} in registries: {registry in self.registries}')
		if registry in self.registries:
			reg = self.registries[registry]
			if not reg['__logged_in__'] and 'user' in reg and 'password' in reg:
				url = reg.get('registry', '')
				user = reg.get('user', '')
				password = reg.get('password', '')

				async def code():
					if url and user and password:
						if self.jobber.verbose:
							print('docker login {registry}'.format(registry=registry))
						await self.jobber._exec([['docker', 'login', '-u', user, '--password', password, url]], verbose=False, echo=False)
						reg['__logged_in__'] = True
					return 0
				if await self.jobber._try(code, 'Unable to login to {0}'.format(url)):
					return 1
		return 0
				


