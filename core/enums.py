from enum import Enum


class StrEnum(str, Enum):
    ...


class PlatformVersion(StrEnum):
    WINDOWS = 'Windows'
    LINUX = 'Linux'
    MAC = 'Darwin'
