# -*- coding: utf-8 -*-

import json
import requests
import datetime
import os

class VKInstance:
	
	def __init__(self, config, type):

		self.config = config
		self.available_scopes = [
			'notify',
			'friends',
			'photos',
			'audio',
			'video',
			'pages',
			'status',
			'notes',
			'messages',
			'wall',
			'ads',
			'offline',
			'docs',
			'groups',
			'notifications',
			'stats',
			'email',
			'market',
			'manage'
		]
		dict_file = open(os.path.dirname(__file__) + '/dict.json')
		self.definition = json.load(dict_file)
		self.definition = [a for a in self.definition if a['prefix'] == type]
		if len(self.definition) != 0:
			self.definition = self.definition[0]
		else:
			msg = 'Unknown API endpoint: {0!r}'.format(type)
			raise Exception(msg)
		self.grants = ['offline']
		if self.definition['prefix'] in self.available_scopes:
			self.grants.insert(0, self.definition['prefix'])
		self.methods = [a['name'] for a in self.definition['methods']]
		dict_file.close()
		self.req_base = 'https://api.vk.com/method/' + self.definition['prefix']
		self.doc_base = 'https://vk.com/dev/ads/' + self.definition['prefix']
		self.getAccess()

	def getAccess(self):

		processAuth = False
		if 'expires_at' in self.config.keys() and 'access_token' in self.config.keys():
			if str(self.config['expires_at']) != 'Never':
				if datetime.datetime.strptime(self.config['expires_at'], '%Y-%m-%d %H:%M:%S.%f') <= datetime.datetime.now():
					processAuth = True
			if 'scopes' in self.config.keys():
				grants_check = 0
				for g in self.grants:
					grants_check += sum([1 if g == i else 0 for i in self.config['scopes']])
				if grants_check != len(self.grants):
					processAuth = True
			else:
				processAuth = True
		else:
			processAuth = True

		if processAuth:
			if 'client_id' not in self.config.keys() and 'client_secret' not in self.config.keys():
				grants_error = 'Please provide client_id and client_secret'
				raise Exception(grants_error)
			code_url = 'https://oauth.vk.com/authorize?client_id={0!s}&redirect_uri=https://vk.com/&display=page&scope={1!s}&response_type=code&v={2!s}'.format(
				self.config['client_id'],
				','.join(self.grants),
				self.definition['api_version']
				)
			print('Open following URL in Your Browser: \n\n' + code_url + '\n')
			code = input('Please paste Code Here (Appears in URL): ')
			if len(code) == 0:
				code_error = 'Code can\'t be empty!'
				raise Exception(code_error)
			access_url = 'https://oauth.vk.com/access_token?client_id={0!s}&client_secret={1}&redirect_uri=https://vk.com/&code={2!s}'.format(
				self.config['client_id'],
				self.config['client_secret'],
				code
				)
			access_q = requests.get(access_url)
			if access_q.status_code == 200:
				access_r = json.loads(access_q.text)
				if 'access_token' in list(access_r.keys()):
					token_data = access_r
				else:
					error = 'Error Request with message: {0!s}.\nError description: {1}'.format(access_r['error'], access_r['error_description'])
					raise Exception(error)
				expiration = datetime.datetime.now() + datetime.timedelta(0, token_data['expires_in']) if token_data['expires_in'] > 0 else 'Never'
				self.config.update({
					'access_token': token_data['access_token'], 
					'expires_at': str(expiration),
					'token_user': token_data['user_id'],
					'scopes': ','.join(self.grants)
				})
				print('\nAccess Details:\nToken: {0!s}\nExpires At: {1!s}\nGranted for User: {2!s}\nScopes: {3!s}'.format(
					self.config['access_token'],
					self.config['expires_at'],
					self.config['token_user'],
					','.join(self.grants)
					)
				)
				with open('vk_config.json', 'w') as cfg:
					json.dump(self.config, cfg)
				print('\nConfigruation stored in current folder as "vk_config.json"\n')
			else:
				msg = 'Server Responded with Status Code: {0!s}. Response Text: {1}'.format(access_q.status_code, access_q.text)
				raise Exception(msg)

	def callMethod(self, method, params = {}):
		if method not in self.methods:
			raise NameError('Method Is Not Supported! Refer to docs: https://vk.com/dev/ads')
		currentConfig = [a for a in self.definition['methods'] if a['name'] == method][0]
		requiredParams = [a['name'] for a in currentConfig['params'] if a['required']]
		if set(requiredParams) != set(list(params.keys())):
			msg = 'List of parameters is not correct. Please refer to docs: {0!s}'.format(self.doc_base + '.' + method)
			raise Exception(msg)
		for ep in currentConfig['params']:
			if type(params[ep['name']]).__name__ != ep['type']:
				msg = 'Parameter {0} should be of type {1!r}, but {2!r} given'.format(ep['name'], ep['type'], type(params[ep['name']]).__name__)
				raise Exception(msg)
			if type(params[ep['name']]).__name__ == 'list' and ep['limit'] > 0:
				if len(params[ep['name']]) > ep['limit']:
					msg = 'Too much objects for method {0}. Please refer to docs: {1!s}'.format(method, self.doc_base + '.' + method)
					raise Exception(msg)
			if type(params[ep['name']]).__name__ == 'str' and 'limited_by' in ep.keys():
				if params[ep['name']] not in ep['limited_by']:
					msg = 'Unknown value for {0}. Please refer to docs: {1!s}'.format(ep['name'], self.doc_base + '.' + method)
					raise Exception(msg)
		composed_query = {
			'v': self.definition['api_version'],
			'access_token': self.config['access_token']
		}
		composed_query = {**composed_query, **{k: (json.dumps(v) if type(v) in ['dict', 'list'] else v ) for k,v in params.items()}}
		method_req = requests.post(
			self.req_base + '.' + method,
			data = composed_query
			)
		if method_req.status_code == 200:
			data = json.loads(method_req.text)
			if 'response' in list(data.keys()):
				result = data['response']
				return(result)
			else:
				error = 'Error Request with code: {0!s}. Error message: {1}'.format(data['error']['error_code'], data['error']['error_msg'])
				raise Exception(error)
		else:
			msg = 'Server Responded with Status Code: {0!s}. Response Text: {1}'.format(method_req.status_code, method_req.text)
			raise Exception(msg)
