# -*- coding: utf-8 -*-
import time
import json

class AgencyAccount:

	def __init__(self, api, account_id = 0):

		self.api = api
		if account_id != 0:
			self.account_id = int(account_id)
		else:
			available_accounts = self.api.callMethod('getAccounts')
			self.account_id = int(available_accounts[0]['account_id'])

	def getDictionaries(self, type, params = {}, all = True):

		if type not in ['clients', 'ads','campaigns']:
			msg = 'There is no dictionary for such kind of objects'
			raise Exception(msg)

		else:
			if type == 'clients':
				result = self.api.callMethod('getClients', {'account_id': self.account_id, **params})
			else:
				if all:
					allClients = [i['id'] for i in self.getDictionaries('clients')]
					result = []
					for i in allClients:
						time.sleep(.5)
						vk_client = ClientAccount(self.api, self.account_id, i)
						result += vk_client.getDictionary(type, params)
				else:
					if 'client_id' in params.keys():
						time.sleep(.5)
						vk_client = ClientAccount(self.api, self.account_id, params['client_id'])
						del params['client_id']
						result = vk_client.getDictionary(type, params)
					else:
						msg = 'Client ID should be defined for non-massive task'
						raise Exception(msg)
		return(result)

	def getStats(self, type, period, date_start, date_end, all = True, idsList = []):

		if type not in ['ad', 'campaign', 'client', 'office']:
			msg = 'Can\'t get stats for such kind of objects'
			raise Exception(msg)
		else:
			if type == 'office':
				result = self.api.callMethod('getStatistics', {
					'account_id': self.account_id,
					'client_id': self.account_id,
					'ids_type': type,
					'ids': ','.join(i),
					'period': period,
					'date_from': date_start,
					'date_to': date_end
				})
				result = [{**i, 'id': result['id'], 'type': result['type']} for i in result['stats']]
			if type == 'client':
				if all:
					allClients = [i['id'] for i in self.getDictionaries('clients')]
					result = []
					for i in allClients:
						client_stats = self.api.callMethod('getStatistics', {
							'account_id': self.account_id,
							'ids_type': type,
							'ids': i,
							'period': period,
							'date_from': date_start,
							'date_to': date_end
						})
						result += [{**j, 'id': result['id'], 'type': result['type']} for j in client_stats['stats']]
				else:
					result = []
					for i in idsList:
						client_stats = self.api.callMethod('getStatistics', {
							'account_id': self.account_id,
							'ids_type': type,
							'ids': i,
							'period': period,
							'date_from': date_start,
							'date_to': date_end
						})
						result += [{**j, 'id': result['id'], 'type': result['type']} for j in client_stats['stats']]
			if type in ['ad', 'campaign']:
				if all:
					allClients = [i['id'] for i in self.getDictionaries('clients')]
					result = []
					for i in allClients:
						time.sleep(.5)
						vk_client = ClientAccount(self.api, self.account_id, i)
						result += vk_client.getStats(type, period, date_start, date_end)
				else:
					result = []
					for i in idsList:
						time.sleep(0.5)
						vk_client = ClientAccount(self.api, self.account_id, i)
						result += vk_client.getStats(type, period, date_start, date_end)

			return(result)

class ClientAccount:

	def __init__(self, api, account_id, client_id):

		self.api = api
		self.account_id = int(account_id)
		self.client_id = client_id

	def getDictionary(self, type, params = {}):

		if type not in ['ads','campaigns']:
			msg = 'There is no dictionary for such kind of objects'
			raise Exception(msg)
		else:
			method = {
				'ads': 'getAds',
				'campaigns': 'getCampaigns'
			}.get(type, '0')
			dict = self.api.callMethod(method, {'account_id': self.account_id, 'client_id': self.client_id, **params})
			dict = [{**k, 'client_id': self.client_id} for k in dict]

		return(dict)

	def getStats(self, type, period, date_start, date_end, all = True, idsList = []):

		if type not in ['ad', 'campaign', 'client']:
			msg = 'Can\'t get stats for such kind of objects'
			raise Exception(msg)
		else:
			if all:
				idsList = [i['id'] for i in self.getDictionary(type + 's')]
			if len(idsList) > 2000:
				chunksList = []
				for i in range(0, len(idsList), 1500):
					chunksList.append(idsList[i:i+1500])
				idsList = chunksList
			else:
				idsList = [idsList]

			result = []
			for i in idsList:	
				stats_part = self.api.callMethod('getStatistics', {
					'account_id': self.account_id,
					'ids_type': type,
					'ids': ','.join(str(i)),
					'period': period,
					'date_from': date_start,
					'date_to': date_end
				})
				stats_part = [{**s, **{'client_id': self.client_id}, 'id': stats_part['id'], 'type': stats_part['type']} for s in stats_part['stats']]
				result += stats_part
			return(result)
