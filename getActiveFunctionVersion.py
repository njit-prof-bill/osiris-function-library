from setActiveFunctionVersion import function_versions

def getActiveFunctionVersion(function_name: str) -> str:
    return function_versions.get(function_name, "")
