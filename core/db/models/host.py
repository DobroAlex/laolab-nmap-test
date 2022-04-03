from typing import Optional

import sqlalchemy as sa
from sqlalchemy import orm

from core.db.models import Base


class Host(Base):
    __tablename__ = 'hosts'
    id = sa.Column(sa.BIGINT, primary_key=True)
    run_id = sa.Column(
        sa.BIGINT,
        sa.ForeignKey(
            'run_reports.id',
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=False,
    )
    address = sa.Column(sa.TEXT, nullable=True, unique=False)
    address_type = sa.Column(sa.TEXT, nullable=True, unique=False)

    run_reports = orm.relationship("RunReport", back_populates='hosts', lazy="joined")
    ports = orm.relationship(
        "Port",
        back_populates='hosts',
        lazy="joined",
        cascade="all, delete",
        passive_deletes=True,
    )
    os_version = orm.relationship(
        "OsVersion",
        back_populates='hosts',
        lazy="joined",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __init__(
            self,
            run_id: int,
            address: Optional[str],
            address_type: Optional[str],
    ):
        self.run_id = run_id
        self.address = address
        self.address_type = address_type
