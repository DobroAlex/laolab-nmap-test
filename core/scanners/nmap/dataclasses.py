import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, Optional

import core.scanners.utils


@dataclass
class NmapRunMeta:
    scanner: str
    args: str
    started_at: Union[str, datetime.datetime]
    finished_at: Union[str, datetime.datetime]
    nmap_version: str
    xml_version: str

    def __post_init__(self):
        self.started_at = core.scanners.utils.timestamp_to_date(self.started_at)
        self.finished_at = core.scanners.utils.timestamp_to_date(self.finished_at)


@dataclass
class Port:
    port_num: int
    protocol: Optional[str]
    state: str
    reason: Optional[str]
    service_name: Optional[str]
    service_product: Optional[str]
    version: Optional[str]
    os_type: Optional[str]
    extra_info: Optional[str]


@dataclass
class OsVersion:
    name: Optional[str] = field(default=None)
    accuracy: Optional[int] = field(default=None)


@dataclass
class Host:
    address: Optional[str]
    address_type: Optional[str]
    ports: list['Port'] = field(default_factory=list)
    os_version: 'OsVersion' = field(default_factory=OsVersion)


@dataclass
class NmpRunReport:
    target: str
    report_file: Path
    run_metadata: NmapRunMeta
    host_records: list[Host]
