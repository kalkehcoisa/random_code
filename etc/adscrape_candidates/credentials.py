''' This file only contains a dictionary with credentials for netwroks in
    format:
    {
        __network_id__: [
            {
                'login': __login__,
                'password': __password,
            },
            ...
        ],
        ...
    }

    Where values surrounded by double underscores ("__") should be replaced
    with real values.
'''

FETCHER_CREDENTIALS = {
    'example-fetcher.com': [
        {
            'login': 'example-login',
            'password': 'example-password',
        }
    ],
    'revcontent.com': [
        {
            'login': 'ALLDAYMEDIA',
            'password': 'wgR9hh6Gs57T',
        }
    ],
    'publishers.criteo.com': [
        {
            'login': 'diplywebsite',
            'password': 'M2diply1234!',
        }
    ],
}
