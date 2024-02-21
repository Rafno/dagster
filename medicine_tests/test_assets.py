from medicine.assets import read_my


def test_read_my():
    test = read_my()
    assert test == 5
