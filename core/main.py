import core.db.models
from core import cli
from core.db.controller.pg_controller import PgController
from core.db.session.pg_session import PgSession
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

        # for scanner in scanners:
        #    scanner.run()
        #    if not scanner.is_return_code_ok:
        #        raise RuntimeError(
        #            f'{scanner.name} terminated improperly:\n'
        #            f'STDOUT: {scanner.process.stdout}\n\n\n'
        #            f'STDERR: {scanner.process.stderr}\n\n\n'
        #            f'EXIT CODE: {scanner.process.process.returncode}'
        #        )

        for scanner in scanners:
            scanner.parse_output()

        with PgController(self.context) as pg_controller:
            with PgSession(pg_controller) as pg_session:
                for scanner in scanners:
                    for item in scanner.to_db_repr:
                        pg_session.session.add(item)
                        pg_session.commit()
                    # pg_session.session.add_all(scanner.to_db_repr)
