from model.Label import Label, CountryLabel, MenuLabel, ULMenuLabel
import model.Countries

label_setting = [
    MenuLabel('Ver',      'Ver.',    'Versions'),
    ULMenuLabel('Other',    'Other',   'Others'),

    Label('SFV',       'SFV',       'Street Fighter V'),
    Label('SFV-S1',    'SFV-S1',    'Street Fighter V Season 1'),
    Label('SFV-S2',    'SFV-S2',    'Street Fighter V Season 2'),

    Label('SFIV',      'SFIV',      'Street Fighter IV'),
    Label('USFIV',     'USFIV',     'Ultra Street Fighter IV'),
    Label('SSFIVAE12', 'SSFIVAE12', 'Super Street Fighter IV AE 2012'),

    Label('2016',      '16',      '2016'),
    Label('2015',      '15',      '2015'),
    Label('2014',      '14',      '2014'),

    Label('CPT',       'CPT',     'Capcom Pro Tour'),

    Label('NA',        'NA',      'North America'),
    Label('LA',        'LA',      'Latin America'),
    Label('AO',        'AO',      'Asia/Oceania'),
    Label('EU',        'EU',      'Europe'),

    Label('Ranking',   'Ranking', 'Ranking'),
    Label('Premier',   'Premier', 'Premier'),
    Label('Evo',       'Evo',     'Evolution'),
    Label('ON',        'ONLINE',  'ONLINE'),
    Label('RF',        'RF',      'Regional Finals'),
    Label('LCQ',       'LCQ',     'Last Chance Qualifier'),
    Label('CC',        'CC',      'Capcom Cup'),

    Label('GP',       'GP',      'Global Premier'),
    Label('CPT-NA',   'CPT-NA',  'CPT North America'),
    Label('CPT-EU',   'CPT-EU',  'CPT Europe'),
    Label('CPT-A',    'CPT-A',   'CPT Asia'),
    Label('WC',       'WC',      'Wild Card'),

    Label('ESL',      'ESL',     'ESL'),
    Label('RB',       'RedBull', 'RedBull'),
    Label('DRK',      'Darake!', 'Darake!'),
    Label('IISPO',    'Iispo!',  'Iispo!'),
    Label('RAGE',     'RAGE',    'RAGE'),
    Label('Crash',    'Crash',   'Crash'),
    Label('KTL',      'Kakutop', 'Kakutop League'),
    Label('DTV',      'Douyu',   'Douyu TV'),
]

label_links = [
    ('Ver', [
        ('SFV',  ['SFV-S1', 'SFV-S2']),
        ('SFIV', ['USFIV']),
    ]),

    ('CPT', [
        ('2016', [
            'NA', 'LA', 'AO', 'EU', 'Ranking', 'Premier', 'Evo', 'RF', 'LCQ', 'CC'
        ]),
        ('2015', [
            'GP', 'CPT-NA', 'CPT-EU', 'CPT-A', 'WC', 'Evo', 'CC'
        ]),
        ('2014', [
            'GP', 'CPT-NA', 'CPT-EU', 'CPT-A', 'WC', 'Evo', 'ON', 'CC'
        ])
    ]),

    ('Other', [
        ('ESL',    []),
        ('RB',     []),
        ('DRK',    []),
        ('IISPO',  []),
        ('RAGE',   []),
        ('Crash',  []),
        ('KTL',    []),
        ('DTV',    []),
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
        if c2 in label_dictionary:
            raise Exception('duplicated label')
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
