import sqlalchemy as sa
from sqlalchemy import orm

from core.db import Base


class ScanTarget(Base):
    __tablename__ = 'scan_targets'
    id = sa.Column(sa.BIGINT, primary_key=True)
    target = sa.Column(sa.TEXT, nullable=False, unique=False)

    scan_runs = orm.relationship(
        "RunReport",
        lazy='joined',
        cascade="all, delete",
        passive_deletes=True,

    )

    def __init__(self, target: str):
        self.target = target
