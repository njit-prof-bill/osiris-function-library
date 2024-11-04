from archiveRestoreApi import archiveRestoreServer

def archiveFunctionVersion(function_name: str, version: str) -> bool:
    functions = archiveRestoreServer.functions
    if function_name not in functions:
        functions[function_name] = {}
    if version not in functions[function_name]:
        return False
    if functions[function_name][version] == 'archived':
        return False
    functions[function_name][version] = 'archived'
    return True

