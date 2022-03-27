from core import cli
from core.scanners.nmap.nmap_scanner import NmapScanner
from core.context import Context


class MainRunner:

    def __init__(self):
        self.context = Context(cli.ArgsParser().parse_args())

    def run(self):
        scanners = [
            scanner(self.context) for scanner in [
                NmapScanner,
            ]
        ]

        for scanner in scanners:
            scanner.run()
            if not scanner.is_return_code_ok:
                raise RuntimeError(
                    f'{scanner.name} terminated improperly:\n'
                    f'STDOUT: {scanner.process.stdout}\n\n\n'
                    f'STDERR: {scanner.process.stderr}\n\n\n'
                    f'EXIT CODE: {scanner.process.process.returncode}'
                )

        for scanner in scanners:
            scanner.parse_output()
