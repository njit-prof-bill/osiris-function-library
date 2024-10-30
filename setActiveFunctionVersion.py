function_versions = {}

def setActiveFunctionVersion(function_name: str, version: str) -> bool:
    if not function_name or not version:
        return False
    
    function_versions[function_name] = version
    return True