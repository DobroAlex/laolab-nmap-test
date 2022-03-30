from typing import Optional

import sqlalchemy as sa
from sqlalchemy import orm

from core.db.models import Base


class Port(Base):
    __tablename__ = 'ports'
    id = sa.Column(sa.BIGINT, primary_key=True)
    host_id = sa.Column(
        sa.BIGINT,
        sa.ForeignKey(
            'hosts.id',
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=False,

    )
    port_num = sa.Column(sa.Integer, nullable=False)
    protocol = sa.Column(sa.TEXT, nullable=True)
    state = sa.Column(sa.TEXT, nullable=False)
    reason = sa.Column(sa.TEXT, nullable=True)
    service_name = sa.Column(sa.TEXT, nullable=True)
    service_product = sa.Column(sa.TEXT, nullable=True)
    version = sa.Column(sa.TEXT, nullable=True)
    os_type = sa.Column(sa.TEXT, nullable=True)
    extra_info = sa.Column(sa.TEXT, nullable=True)

    host = orm.relationship("Host", lazy="joined")

    def __init__(
            self,
            port_num: int,
            protocol: Optional[str],
            state: str,
            reason: Optional[str],
            service_name: Optional[str],
            service_product: Optional[str],
            version: Optional[str],
            os_type: Optional[str],
            extra_info: Optional[str],
    ):
        self.port_num = port_num
        self.protocol = protocol
        self.state = state
        self.reason = reason
        self.service_name = service_name
        self.service_product = service_product
        self.version = version
        self.os_type = os_type
        self.extra_info = extra_info
