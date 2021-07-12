from sastadev.astaforms import AstaFormData, ExcelForm, make_astaform, tabel, scores


def test_astaform():
    astadata = AstaFormData({'boek': 2, 'huis': 3}, {'lopen': 2})
    theform = ExcelForm(tabel, scores)
    theworkbook = make_astaform(theform, astadata, 'astaformulier.xlsx')

    theworkbook.close()
