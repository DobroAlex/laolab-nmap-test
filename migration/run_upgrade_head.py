import logging
import os

import alembic.config

logger = logging.getLogger()


def run_migrations() -> None:
    os.chdir(os.path.dirname(os.getcwd()))
    logger.info('Running DB migrations')
    alembic_args = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=alembic_args)


if __name__ == '__main__':
    run_migrations()
