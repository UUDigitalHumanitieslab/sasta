from sastadev.namepartlexicon import namepartlexicon


def test_namepartlexicon():
    max = 10
    ctr = 0
    for namepart in namepartlexicon:
        if ctr == max:
            break
        else:
            print(namepart, namepartlexicon[namepart])
        ctr += 1
