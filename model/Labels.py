from model.Label import Label, CountryLabel
import model.Countries

label_setting = [
    Label('Ver',      'Ver.',    'Versions'),
    Label('SFV',      'SFV',     'Street Fighter V'),
    Label('SFIV',     'SFIV',    'Street Fighter IV'),

    Label('2016',     '16',      '2016'),

    Label('CPT',      'CPT',     'Capcom Pro Tour'),

    Label('NA',       'NA',      'North America'),
    Label('LA',       'LA',      'Latin America'),
    Label('AO',       'AO',      'Asia/Oceania'),
    Label('EU',       'EU',      'Europe'),

    Label('Ranking',  'Ranking', 'Ranking'),
    Label('Premier',  'Premier', 'Premier'),
    Label('Evo',      'Evo',     'Evolution'),
    Label('RF',       'RF',      'Regional Finals'),
    Label('LCQ',      'LCQ',     'Last Chance Qualifier'),
]

label_links = {
    'Ver': {
        'SFV': [
            'SFV'
        ],
        'SFIV': [
            'SFIV'
        ]
    },

    'CPT': {
        '2016': [
            'NA', 'LA', 'AO', 'EU', 'Ranking', 'Premier', 'Evo', 'RF', 'LCQ'
        ],
    },
}

label_dictionary = None
links_dicitionary = None


def labels():
    global label_dictionary, label_setting
    if label_dictionary is not None:
        return label_dictionary

    label_dictionary = {s.key: s for s in label_setting}

    for c2, country in model.Countries.countries.items():
        label_dictionary[c2] = CountryLabel(c2, c2, country)

    return label_dictionary


def links():
    def rec(item):
        if isinstance(item, list):
            return [rec(i) for i in item]
        if isinstance(item, dict):
            return {rec(k): rec(v) for k, v in item.items()}
        return ls[item]

    global label_links, links_dicitionary

    if links_dicitionary is not None:
        return links_dicitionary

    ls = labels()
    links_dicitionary = rec(label_links)
    return links_dicitionary


def labels_from_string(string: str):
    label_dic = labels()
    return [label_dic[s.strip()] for s in string.split(',')]


def labels_from_url(path: str):
    label_dic = labels()
    return [label_dic[p.strip()] for p in path.split('/')]
