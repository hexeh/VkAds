# VkAds
Collection of wrappers for Ads methods of VKontakte

Example:

```python
# -*- coding: utf-8 -*-

import pprint
from py.vk_class import VKInstance

if __name__ == '__main__':

	pp = pprint.PrettyPrinter( indent = 4 )
	vk = VKInstance({'access_token': 'token'})

	pp.pprint(vk.callMethod('getClients', {'account_id': 1}))
```
