def get_os_version_accuracy(version_container: dict, key: str = 'accuracy') -> int:
    return int(version_container.get(key, 0))
