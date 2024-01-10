import os
from base64 import b64decode
from datetime import datetime

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from src.main import SignatureShortInfo, SignaturesList


class SignaturesListFactory(ModelFactory[SignaturesList]):
    pass


class SignatureShortInfoFactory(ModelFactory[SignatureShortInfo]):
    pass


from src.cli import extract
from src.main import extract_cert_info_from_sig_file, extract_cert_infos_from_directory, write_signatures_to_file


def bytes_from_base64_file(filename: str) -> bytes:
    with open(filename, "r", encoding="utf8") as f:
        return b64decode(f.read())


def bytes_from_binary_file(filename: str) -> bytes:
    with open(filename, "rb") as f:
        return f.read()


@pytest.mark.parametrize(
    "filename,sign_date",
    [
        ("tests/fixtures/NEP/IMG_20231227_085120.jpg.sig", datetime(2023, 12, 29, 18, 13, 55)),
        ("tests/fixtures/KEP/Результат_оказания_услуги_11_29_41.pdf.sig", datetime(2023, 12, 29, 18, 7, 56)),
    ],
)
def test_main_extract(filename: str, sign_date: datetime):
    res = extract_cert_info_from_sig_file(filename)
    assert res.subject_name == "Володькин Данила Викторович"
    assert res.subject_snils == "12522310804"
    assert res.sign_date == sign_date


def test_extract_list_of_signatures():
    """
    на входе каталог с файлами подписей. На выходе ожидаем массив данных по подписям.
    """
    path = "tests/fixtures/mass"
    res = extract_cert_infos_from_directory(path).root
    assert len(res) == 2
    assert res[0].subject_name == "Володькин Данила Викторович"


def test_cli_extract():
    source = "tests/fixtures/mass"
    output = "build/result.ods"
    extract(source, output)


def test_write_excel():
    """TODO не перезаписывать существующий файл, бросать исключение"""
    out_filename = "build/out.ods"
    if os.path.exists(out_filename):
        os.remove(out_filename)
    signatures = SignaturesList(
        root=SignatureShortInfoFactory.batch(10),
    )
    write_signatures_to_file(signatures, out_filename)
    assert os.path.exists(out_filename)
