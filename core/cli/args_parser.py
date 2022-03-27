import argparse
from pathlib import Path

from core.cli.program_args import ProgramArgs


class ArgsParser:
    def __init__(self):
        self.__parser = self.__get_parser

    @property
    def __get_parser(self) -> 'argparse.ArgumentParser':
        parser_ = argparse.ArgumentParser()
        parser_.add_argument(
            '-t',
            '--target',
            dest='target',
            help='Either single domain as am FQDN or an IP address '
                 'that is a target for Nmap scanning',
            required=True,
            type=str,
        )
        parser_.add_argument(
            '-o',
            '--output-file',
            dest='output_file',
            help='A path (preferably, a full one) where Nmap output is stored',
            required=True,
            type=Path,
        )
        return parser_

    def parse_args(self):
        parsed_args = self.__parser.parse_args()
        return ProgramArgs(
            scan_target=parsed_args.target,
            output_file=parsed_args.output_file,
        )
