from model.Label import Label, CountryLabel, MenuLabel, ULMenuLabel
import model.Countries

label_setting = [
    MenuLabel('Ver',      'Ver.',    'Versions'),
    ULMenuLabel('Other',    'Other',   'Others'),

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

    Label('ESL',      'ESL',     'ESL'),
    Label('RB',       'RedBull', 'RedBull'),
    Label('DRK',      'Darake!', 'Darake!'),
    Label('IISPO',    'Iispo!',  'Iispo!'),
    Label('RAGE',     'RAGE',    'RAGE'),
    Label('Crash',    'Crash',   'Crash'),
]

label_links = [
    ('Ver', [
        ('SFV',  []),
    ]),

    ('CPT', [
        ('2016', [
            'NA', 'LA', 'AO', 'EU', 'Ranking', 'Premier', 'Evo', 'RF', 'LCQ'
        ])
    ]),

    ('Other', [
        ('ESL',    []),
        ('RB',     []),
        ('DRK',    []),
        ('IISPO',  []),
        ('RAGE',   []),
        ('Crash',  []),
    ])
]

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
        if isinstance(item, tuple):
            return [rec(item[0]), rec(item[1])]
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
