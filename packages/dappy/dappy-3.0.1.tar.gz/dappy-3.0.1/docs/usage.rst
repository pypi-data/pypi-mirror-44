=====
Usage
=====

To use dappy in a project::

    from dappy import API, Endpoint

    ItunesAPI = API('itunes.apple.com', [
        Endpoint(
            'search', '/search',
            query_map={ 'search_string': 'term' },  # Map input query params to what the API actually expects
            default_query={ 'entity': 'podcast' }  # Default query params to send with every request
            # we could also pass default_params={} or default_headers={} here
        ),
        Endpoint('lookup', '/lookup')
    ], scheme='https')  # scheme defaults to 'https'

    ItunesAPI.search(query={
        'search_string': 'Hello, World'  # 'search_string" will get mapped to 'term' before we send the request
    })  # 'entity=podcast' gets added to the query without us providing it here

    ItunesAPI.get(query={ 'id': '656270845' })


Return Values
==========

All dappy functions return either a dict representing JSON or a requests request object depending on how an Endpoint was set up. Currently it defaults to parsing JSON and returning a dict. ::

    from dappy import API, Endpoint
    from dappy.formatters import default_formatter, json_formatter

    ItunesAPI = API('itunes.apple.com', [
        Endpoint('search', '/search'),
    ])
    ItunesAPI.search()  # Returns requests request object


    ItunesAPI = API('itunes.apple.com', [
        Endpoint('search', '/search'),
    ], formatter=json_formatter)
    ItunesAPI.search()  # Returns dict parsed from JSON


    ItunesAPI = API('itunes.apple.com', [
        Endpoint('search', '/search', formatter=json_formatter),
        Endpoint('lookup', '/lookup'),
     json=False)
    ItunesAPI.search()  # Returns dict parsed from JSON
    ItunesAPI.lookup()  # Returns requests request object


    ItunesAPI = API('itunes.apple.com', [
        Endpoint('search', '/search', formatter=default_formatter),
        Endpoint('lookup', '/lookup'),
    ], formatter=json_formatter)
    ItunesAPI.search()  # Returns requests request object
    ItunesAPI.lookup()  # Returns dict parsed from JSON


Mocking
=======

Using the requests-mock module, we can mock specific URLs ::

    import requests_mock
    from dappy import API, Endpoint

    ItunesAPI = API('itunes.apple.com', [
        Endpoint('search', '/search'),
    ])
    with requests_mock.Mocker() as mock:
        mock.get('https://itunes.apple.com/search', json={'results': []})
        ItunesAPI.search().json() # returns {'results': []}


GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, PATCH, TRACE
============================================================

Dappy supports all http methods, each http method can accept keyword args 'query', 'params', and 'headers' ::

    from dappy import API, Endpoint

    ItunesAPI = API('itunes.apple.com', [
        Endpoint('search', '/search'),
    ])
    ItunesAPI.search()  # sends a GET request
    ItunesAPI.search.get(query={})  # also sends a GET request
    ItunesAPI.search.head()
    ItunesAPI.search.post(params={}, headers={'Authorization': 'Basic ...'})
    ItunesAPI.search.put()
    ItunesAPI.search.delete()
    ItunesAPI.search.connect()
    ItunesAPI.search.options()
    ItunesAPI.search.patch()
    ItunesAPI.search.trace()
    
    ...