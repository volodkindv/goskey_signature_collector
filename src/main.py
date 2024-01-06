from pathlib import Path

from cryptography.hazmat.primitives.serialization.pkcs7 import load_der_pkcs7_certificates
from cryptography.x509 import ObjectIdentifier
from pydantic import BaseModel


class CertificateShortInfo(BaseModel):
    subject_name: str
    subject_snils: str


def extract_cert_info_from_sig_file(filename: str) -> CertificateShortInfo:
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

    return CertificateShortInfo(
        subject_name=subject_name,
        subject_snils=subject_snils,
    )


def extract_cert_infos_from_directory(path: str) -> list[CertificateShortInfo]:
    res: list[CertificateShortInfo] = []

    for filename in Path(path).glob("*.sig"):
        res.append(extract_cert_info_from_sig_file(str(filename)))

    return res
