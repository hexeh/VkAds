# -*- coding: utf-8 -*-

import json
import requests
import os

class VKInstance:
	
	def __init__(self, config):

		self.config = config
		dict_file = open(os.path.dirname(__file__) + '/methods_dict.json')
		self.definition = json.load(dict_file)
		self.methods = [a['name'] for a in self.definition['methods']]
		dict_file.close()
		self.req_base = 'https://api.vk.com/method/' + self.definition['prefix']
		self.doc_base = 'https://vk.com/dev/ads/' + self.definition['prefix']

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
		composed_query = {
			'v': self.definition['api_version'],
			'access_token': self.config['access_token']
		}
		composed_query = {**composed_query, **{k: (json.dumps(v) if type(v) == 'dict' else v ) for k,v in params.items()}}
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
