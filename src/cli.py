import argparse

from .main import extract_cert_infos_from_directory


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=str, help="source directory with .sig files", required=True)
    parser.add_argument("-o", "--output", type=str, help="result filename (JSON)")

    args = parser.parse_args()
    extract(args.source, args.output)


def extract(source: str, output: str | None) -> None:
    infos = extract_cert_infos_from_directory(source)
    dumped = infos.model_dump_json(indent=2)
    if output:
        with open(output, "w", encoding="utf8") as result_file:
            result_file.write(dumped)
    else:
        print(dumped)  # noqa: WPS421
