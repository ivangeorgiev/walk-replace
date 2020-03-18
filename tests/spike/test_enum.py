import enum

class SubEnum(enum.Enum):
    PLAINTEXT = 'plaintext'


def test_get_name_value():
    assert "plaintext" == SubEnum.PLAINTEXT.value
    assert "PLAINTEXT" == SubEnum.PLAINTEXT.name
    assert "SubEnum.PLAINTEXT" == str(SubEnum.PLAINTEXT)
