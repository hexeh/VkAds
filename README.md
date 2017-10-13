# VkAds
Collection of wrappers for Ads methods of VKontakte

Example:

```python
# -*- coding: utf-8 -*-

import pprint
from py.vk_class import VKInstance

if __name__ == '__main__':

	pp = pprint.PrettyPrinter( indent = 4 )
	try:
		config_f = open('vk_config.json')
		config = json.load(config_f)
		config_f.close()
	except:
		config = {}
	vk = VKInstance(config)

	pp.pprint(vk.callMethod('getClients', {'account_id': 1}))
```
