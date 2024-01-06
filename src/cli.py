import argparse

from .main import extract_cert_infos_from_directory


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=str, help="source directory with .sig files", required=True)

    args = parser.parse_args()
    infos = extract_cert_infos_from_directory(args.source)
    print(infos)  # noqa: WPS421
