from model.Label import Label

label_setting = [
    Label('2016',     '16',      '2016', 'CadetBlue'),

    Label('CPT',      'CPT',     'Capcom Pro Tour', 'RoyalBlue'),

    Label('NA',       'NA',      'North America', 'Indigo'),
    Label('LA',       'LA',      'Latin America', 'Indigo'),
    Label('AO',       'AO',      'Asia/Oceania',  'Indigo'),
    Label('EU',       'EU',      'Europe',        'Indigo'),

    Label('Ranking',  'Ranking', 'Ranking',       '#191970'),
    Label('Premier',  'Premier', 'Premier',       '#191970'),
    Label('Evo',      'Evo',     'Evolution',      '#191970'),
    Label('RF', 'RF', 'Regional Finals', '#191970'),
    Label('LCQ',      'LCQ',     'Last Chance Qualifier', '#191970'),
]

label_dictionary = None


def labels():
    global label_dictionary, label_setting
    if label_dictionary is not None:
        return label_dictionary

    label_dictionary = {s.key: s for s in label_setting}
    return label_dictionary


def labels_from_string(string: str):
    label_dic = labels()
    return [label_dic[s.strip()] for s in string.split(',')]
