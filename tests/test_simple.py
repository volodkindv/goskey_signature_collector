from base64 import b64decode

import pytest

from src.main import extract_cert_info_from_sig_file, extract_cert_infos_from_directory


def bytes_from_base64_file(filename: str) -> bytes:
    with open(filename, "r", encoding="utf8") as f:
        return b64decode(f.read())


def bytes_from_binary_file(filename: str) -> bytes:
    with open(filename, "rb") as f:
        return f.read()


@pytest.mark.parametrize(
    "filename",
    [
        ("tests/fixtures/NEP/IMG_20231227_085120.jpg.sig"),
        ("tests/fixtures/KEP/Результат_оказания_услуги_11_29_41.pdf.sig"),
    ],
)
def test_main_extract(filename: str):
    res = extract_cert_info_from_sig_file(filename)
    assert res.subject_name == "Володькин Данила Викторович"
    assert res.subject_snils == "12522310804"


def test_extract_list_of_signatures():
    """
    на входе каталог с файлами подписей. На выходе ожидаем массив данных по подписям.
    """
    path = "tests/fixtures/mass"
    res = extract_cert_infos_from_directory(path).root
    assert len(res) == 2
    assert res[0].subject_name == "Володькин Данила Викторович"
