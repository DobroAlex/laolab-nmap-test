from typing import Optional

import sqlalchemy.orm

from core.db.controller.pg_controller import PgController


class PgSession:

    def __init__(self, pg_controller: PgController):
        self._controller = pg_controller
        self.session: Optional[sqlalchemy.orm.Session] = None

    def __enter__(self):
        # Ensuring that session is only usable in the context-manager mode
        self.session = sqlalchemy.orm.Session(
            self._controller.engine,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: analyze exec_type.
        #       If it's a DB error don't commit but attempt a rollback.
        #       If rollback fails, notify about it and close session
        try:
            self.commit()
        except Exception as err:
            print(
                f'Cant commit to a closing PG session due to:\n'
                f'[{type(err)}] {err}'
            )
            try:
                self.rollback()
            except Exception as rollback_err:
                print(
                    f'Cant rollback a previously errored closing session due to:\n'
                    f'[{type(rollback_err)}] {rollback_err}'
                )
                raise rollback_err from err
        self.close()

    def flush(self):
        self.session.flush()

    def commit(self):
        self.flush()
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()
        self.session = None
