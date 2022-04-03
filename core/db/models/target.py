import sqlalchemy as sa
from sqlalchemy import orm

from core.db.models import Base


class ScanTarget(Base):
    __tablename__ = 'scan_target'
    id = sa.Column(sa.BIGINT, primary_key=True)
    target = sa.Column(sa.TEXT, nullable=False, unique=False)

    run_reports = orm.relationship(
        "RunReport",
        back_populates='scan_target',
        lazy='joined',
        cascade="all, delete",
        passive_deletes=True,

    )

    def __init__(self, target: str):
        self.target = target
