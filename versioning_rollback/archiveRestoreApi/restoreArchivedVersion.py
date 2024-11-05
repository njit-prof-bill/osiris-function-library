from . import archiveRestoreServer

def restoreArchivedVersion(function_name: str, version: str) -> bool:
    functions = archiveRestoreServer.functions
    if function_name not in functions:
        return False
    if version not in functions[function_name]:
        return False
    if functions[function_name][version] != 'archived':
        return False
    functions[function_name][version] = 'active'
    return True

