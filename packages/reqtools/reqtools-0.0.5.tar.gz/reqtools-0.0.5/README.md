Requirements
============

* Python >= 3.6

Installation
============

```bash
pip install reqtools
```

Usage
=====

Remote API session
------------------

```python
from reqtools import RemoteApiSession

session = RemoteApiSession('http://my-api.com', prefix='api')
response = session.get('/api/method', params={'param': 'value'})
```
