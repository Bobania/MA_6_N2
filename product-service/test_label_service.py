from app.api.models import LabelIn, LabelOut


def labels():
    return LabelIn(
        name='Dead Dynasty',
        phone='+7999999999',
        count_artists=5,
        county='Russia',
    )


def test_create_label(labels):
    assert labels.name == 'Dead Dynasty'
    assert labels.phone == '+7999999999'
    assert labels.count_artists == 5
    assert labels.county == 'Russia'


def test_update_label(labels):
    labels_upd = LabelOut(
        id=1,
        name='Dead Dynasty',
        phone='+7999999999',
        count_artists=5,
        county='Russia'
    )
    assert labels_upd.id == 1
    assert labels_upd.name == 'Dead Dynasty'
    assert labels_upd.phone == '+7999999999'
    assert labels_upd.count_artists == 5
    assert labels_upd.county == 'Russia'


# количество артистов является целым числом и больше или равно нулю
def test_label_count_artists_integer(labels):
    assert isinstance(labels.count_artists, int)
    assert labels.count_artists >= 0


# номер телефона начинается с символа "+" и остальные символы являются цифрами.
def test_label_phone_valid_format(labels):
    assert labels.phone.startswith('+')
    assert all(char.isdigit() for char in labels.phone[1:])
