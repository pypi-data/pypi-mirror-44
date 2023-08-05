=====
Usage
=====

To use dappy in a project::

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


Return Values
==========

All dappy functions return either a dict representing JSON or a requests request object depending on how an Endpoint was set up. Currently it defaults to parsing JSON and returning a dict. ::

    ItunesAPI = API('itunes.apple.com', [
        Endpoint('search', '/search'),
    ])
    ItunesAPI.search()  # Returns dict parsed from JSON


    ItunesAPI = API('itunes.apple.com', [
        Endpoint('search', '/search'),
    ], json=False)
    ItunesAPI.search()  # Returns requests request object


    ItunesAPI = API('itunes.apple.com', [
        Endpoint('search', '/search', json=True),
        Endpoint('get', '/lookup'),
    ], json=False)
    ItunesAPI.search()  # Returns dict parsed from JSON
    ItunesAPI.lookup()  # Returns requests request object


    ItunesAPI = API('itunes.apple.com', [
        Endpoint('search', '/search', json=False),
        Endpoint('get', '/lookup'),
    ], json=True)
    ItunesAPI.search()  # Returns requests request object
    ItunesAPI.lookup()  # Returns dict parsed from JSON