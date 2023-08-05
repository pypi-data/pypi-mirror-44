# dappy

package to allow defining an API declaratively


## Example

All the API calls below (".get()", ".search()") return a dict parsed with json.loads()
```python
from dappy import API, Endpoint

ItunesAPI = API('itunes.apple.com', [
    Endpoint(
        'search', '/search',
        query_map={ 'search_string': 'term' },  # Map input query params to what the API actually expects
        defaults={ 'entity': 'podcast' }  # Default query params to send with every request
    ),
    Endpoint('get', '/lookup')
], scheme='https')  # scheme defaults to 'https'

ItunesAPI.search(query={
    'search_string': 'Hello, World'  # 'search_string" will get mapped to 'term' before we send the request
})  # 'entity=podcast' gets added to the query without us providing it here

ItunesAPI.get(query={ 'id': '656270845' })
```
See https://dappy.readthedocs.io/en/latest/usage.html for more usage info.


* Free software: MIT license
* Documentation: https://dappy.readthedocs.io.
