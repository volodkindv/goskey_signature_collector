import argparse

from .main import extract_cert_infos_from_directory, write_signatures_to_file


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=str, help="source directory with .sig files", required=True)
    parser.add_argument("-o", "--output", type=str, help="result filename (ODS format)")

    args = parser.parse_args()
    extract(args.source, args.output)


def extract(source: str, output: str | None) -> None:
    infos = extract_cert_infos_from_directory(source)
    if output:
        write_signatures_to_file(infos, output)
    else:
        dumped = infos.model_dump_json(indent=2)
        print(dumped)  # noqa: WPS421
