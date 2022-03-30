import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from core.db.models import Base


class RunReport(Base):
    __tablename__ = 'run_reports'
    id = sa.Column(sa.BIGINT, primary_key=True)
    scan_target_id = sa.Column(
        sa.BIGINT,
        sa.ForeignKey(
            'scan_targets.id',
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=False,
    )
    scanner = sa.Column(sa.TEXT, nullable=False)
    args = sa.Column(sa.TEXT, nullable=False)
    started_at = sa.Column(sa.TIME, nullable=False)
    finished_at = sa.Column(sa.TIME, nullable=False)
    nmap_version = sa.Column(sa.TEXT, nullable=False)
    xml_version = sa.Column(sa.TEXT, nullable=False)

    target = orm.relationship("ScanTarget", lazy="joined")
    hosts = orm.relationship(
        "Host",
        lazy="joined",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __init__(
            self,
            scan_target_id: int,
            scanner: str,
            args: str,
            started_at: datetime.datetime,
            finished_at: datetime.datetime,
            nmap_version: str,
            xml_version: str,
    ):
        self.scan_target_id = scan_target_id
        self.scanner = scanner
        self.args = args
        self.started_at, self.finished_at = started_at, finished_at
        self.nmap_version, self.xml_version = nmap_version, xml_version
