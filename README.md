# VkAds
Collection of wrappers for Ads methods of VKontakte

## Example:

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
	vk = VKInstance(config, 'ads')

	pp.pprint(vk.callMethod('getClients', {'account_id': 1}))
```
## Requirements

### App

Create VK App [here](https://vk.com/apps)

 * App Type: **Web**
 * App Redirect URI: **https://vk.com/**
 
### System

 * Python v3.0.6 or higher
