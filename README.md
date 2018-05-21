# VKontakte API (Ads)
Collection of wrappers for Ads methods of VKontakte

## Example:

```python
# -*- coding: utf-8 -*-

import pprint
from api import VK
from agency import AgencyAccount

if __name__ == '__main__':

	pp = pprint.PrettyPrinter( indent = 4 )
	try:
		config_f = open('config/vk.json')
		config = json.load(config_f)
		config_f.close()
	except:
		config = {}
	vk = VK(config, 'ads')
	agency = AgencyAccount(vk)

	pp.pprint(agency.getDictionaries('clients'))
```
Extended example can be found [here](/interface.py)
## Requirements

### App

Create VK App [here](https://vk.com/apps)

 * App Type: **Web**
 * App Redirect URI: **https://vk.com/**
 
### System

 * Python v3.0.6 or higher
