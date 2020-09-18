from .stringfunctions import monosyllabic, syllableheadsre

# TODO: Find out what the test results should be


def t_condition(condition, word):
    if condition(word):
        print('OK:{}'.format(word))
    else:
        print('NO:{}'.format(word))


def test_stringfunctions():
    monosyllabicwords = ['baai', 'eeuw', 'mooi', 'aap', 'deed', 'Piet', 'noot', 'duut', 'rijd', 'meid', 'rauw', 'koud', 'buit', 'reuk', 'boer', 'la', 'de', 'hik', 'dop', 'dut',
                         'yell', 'ry', 'Händl', 'Pëtr', 'bït', 'Köln', 'Kür', 'Tÿd']
    disyllabicwords = ['baaien', 'eeuwen', 'mooie', 'aapje', 'deden', 'Pietje', 'noten', 'dut', 'rijden', 'meiden', 'rauwe', 'koude', 'buitje', 'reuken', 'boeren', 'laden', 'dender',
                       'hikken', 'doppen', 'dutten', 'yellen', 'ryen', 'Händler', 'Pëtri', 'bïty', 'Kölner', 'Kürer', 'Tÿding', 'naäap', 'meeëten', 'ciën', 'coöp']

    for word in monosyllabicwords:
        t_condition(monosyllabic, word.lower())
    for word in disyllabicwords:
        t_condition(monosyllabic, word.lower())

    for word in monosyllabicwords + disyllabicwords:
        ms = syllableheadsre.finditer(word)
        print(word, end=' -- ')
        for m in ms:
            print(m.group(0), end=', ')
        print('')
