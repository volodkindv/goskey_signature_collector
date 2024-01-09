import re
import shlex
import subprocess  # noqa: S404
from datetime import datetime
from pathlib import Path

from cryptography.hazmat.primitives.serialization.pkcs7 import load_der_pkcs7_certificates
from cryptography.x509 import ObjectIdentifier
from pydantic import BaseModel, RootModel


class SignatureShortInfo(BaseModel):
    subject_name: str
    subject_snils: str
    sign_date: datetime


class SignaturesList(RootModel):
    root: list[SignatureShortInfo]


def extract_cert_info_from_sig_file(filename: str) -> SignatureShortInfo:
    with open(filename, "rb") as sig_file:
        sig_data = sig_file.read()
    certificates = load_der_pkcs7_certificates(sig_data)

    if not certificates:
        raise ValueError("Signature should have one certificate")
    if len(certificates) > 1:
        raise ValueError("Signature should have exactly one certificate")

    cert = certificates[0]
    subject_name = cert.subject.get_attributes_for_oid(ObjectIdentifier("2.5.4.3"))[0].value
    subject_snils = cert.subject.get_attributes_for_oid(ObjectIdentifier("1.2.643.100.3"))[0].value

    sign_date = extract_sign_date(filename)

    return SignatureShortInfo(
        subject_name=subject_name,
        subject_snils=subject_snils,
        sign_date=sign_date,
    )


def extract_sign_date(filename: str) -> datetime:
    """Для извлечения даты подписания нет удобных инструментов"""

    cmd = shlex.split(f"openssl asn1parse -inform DER -in {filename}")

    with subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding="utf8") as task:  # noqa: S603
        command_output = task.stdout.read()  # type:ignore[union-attr]

    pattern = re.compile("signingTime.*UTCTIME\s+:(\d+)")  # noqa:W605
    found = re.findall(pattern, command_output.replace("\n", " "))
    return datetime.strptime(found[0], "%y%m%d%H%M%S")


def extract_cert_infos_from_directory(path: str) -> SignaturesList:
    res: list[SignatureShortInfo] = []

    for filename in Path(path).glob("*.sig"):
        res.append(extract_cert_info_from_sig_file(str(filename)))

    return SignaturesList(root=res)
