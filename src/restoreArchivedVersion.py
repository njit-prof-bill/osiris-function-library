# restoreArchivedVersion.py


functions = {}

def restoreArchivedVersion(function_name: str, version: str) -> bool:
 

    
  
    if function_name not in functions:
        return False
   
    if version not in functions[function_name]:
        return False
    
    if functions[function_name][version] != 'archived':
        return False

    functions[function_name][version] = 'active'
    return True

