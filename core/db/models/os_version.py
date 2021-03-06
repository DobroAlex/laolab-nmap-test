import sqlalchemy as sa
from sqlalchemy import orm

from core.db.models import Base


class OsVersion(Base):
    __tablename__ = 'os_version'
    id = sa.Column(sa.BIGINT, primary_key=True)
    host_id = sa.Column(
        sa.BIGINT,
        sa.ForeignKey(
            'hosts.id',
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )
    name = sa.Column(sa.TEXT, nullable=True)
    accuracy = sa.Column(sa.SMALLINT, nullable=True)

    hosts = orm.relationship("Host", back_populates='os_version', lazy="joined")

    def __init__(
            self,
            host_id: int,
            name: str,
            accuracy: int,
    ):
        self.host_id = host_id
        self.name = name
        self.accuracy = accuracy
