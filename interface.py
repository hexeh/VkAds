# -*- coding: utf-8 -*-

import datetime
import json
import pprint
import argparse
from api import VK
from agency import AgencyAccount

YESTERDAY = datetime.date.today() - datetime.timedelta(1)
TODAY = datetime.date.today()

if __name__ == '__main__':
	pp = pprint.PrettyPrinter( indent = 4 )
	parser = argparse.ArgumentParser( description = 'Interface for VKontakte API')
	parser.add_argument("task", help = "complete task")
	parser.add_argument("-v", "--verbose", action = "store_true", help = "print execution info")
	parser.add_argument("-cl", "--clients_list", nargs = '*', help = "produce clients list", default = [])
	parser.add_argument("-dr", "--date_range", nargs = '*', help = "produce date range", default = [str(YESTERDAY)])
	args = parser.parse_args()

	if len(args.date_range) != 1 and len(args.date_range) > 2:
		print('Date range can contain only one or two dates')
		sys.exit()

	log = []

	try:
		config_f = open('config/vk.json')
		config = json.load(config_f)
		config_f.close()
	except:
		config = {}
	vk = VK(config, 'ads')
	agency = AgencyAccount(vk)

	current_task = args.task

	if current_task == 'clients':
		pp.pprint(agency.getDictionaries('clients'))
	if current_task == 'campaigns':
		pp.pprint(agency.getDictionaries('campaigns', all = False, params = {'client_id': 123}))
	if current_task == 'stats':
		pp.pprint(agency.getStats('campaign', 'day', '2018-05-01', '2018-05-10', all = False, idsList = [123]))
