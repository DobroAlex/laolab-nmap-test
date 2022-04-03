from typing import Optional

import sqlalchemy as sa

import core.context


class PgController:
    def __init__(self, context: core.context.Context):
        self.__context = context
        self.engine: Optional[sa.engine.Engine] = None

    def __enter__(self):
        self.engine = sa.create_engine(
            self.__context.config.db.db_connection_string,
            echo=False,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None
