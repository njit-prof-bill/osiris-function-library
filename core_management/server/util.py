from server.data_store import function_library

def addFunctionToLibrary(function_name: str, code: str, runtime: str, version: str = "1.0") -> bool:
    # Check if function already exists
    if function_name in function_library:
        return False, f"Function {function_name} version {version} already exists."

    # If it doesn't exist, create the database entry
    function_library[function_name] = {
        'name': function_name,
        'code': code,
        'runtime_env': runtime,
        'version': version,
        'versions': {version: code}
        }
    return True, f"Function {function_name} version {version} added successfully."

def updateFunctionInLibrary(function_name: str, code: str, version: str) -> bool:
    '''Description:
        The updateFunctionInLibrary API updates the code and version of an existing function in the library.
        It requires the function name, new code, and a new version number.
        Input:
        function_name: The name of the function to update (string)
        code: The updated source code for the function (string)
        version: The new version of the function (string)
        Output:
        True if the function is successfully updated, False otherwise
    '''
    #check if function already exists
    if function_name in function_library:
        #perform update
        function_library[function_name].update({
            'code': code,
            'version': version
            })
        return True, f"Function {function_name} version {version} updated successfully."
    return False, f"Function {function_name} version {version} update failed."
    #function does not exist in library, cannot update

def removeFunctionFromLibrary(function_name: str) -> bool:
    '''Description:
        The removeFunctionFromLibrary API removes a function from the library based on its name.
        The function returns True if the function is successfully removes, False otherwise.
        
        Input: 
        function_name: The name of the function to be removed (string)
        Output:
        True if the function if successfully removed, False otherwise
        '''
    #Check if function is in library
    if function_name in function_library:
        #delete entry using del
        del function_library[function_name]
        return True, f"Function {function_name} deleted successfully."
    return False, f"Function {function_name} delete failed."

def listFunctionsInLibrary():
    """Returns a tuple with success status and a message containing all functions in the library."""
    if function_library:
        function_list = "\n".join([
            f"Name: {func['name']}, Version: {func['version']}, Runtime: {func['runtime_env']}"
            for func in function_library.values()
        ])
        return True, function_list
    else:
        return False, "No functions available in the library."

def getFunctionDetails(function_name: str):
    """Returns a tuple with success status and a message containing details of a specific function."""
    func = function_library.get(function_name)
    if func:
        details = f"Name: {func['name']}, Version: {func['version']}, Runtime: {func['runtime_env']}\nCode: {func['code']}"
        return True, details
    else:
        return False, f"Function {function_name} not found."

# API 6
def rollbackFunctionVersion(function_name: str, target_version: str) -> bool:
    if function_name in function_library:
        # Check if the target version exists in the versions dictionary
        if target_version in function_library[function_name]['versions']:
            # Rollback to the specified version
            function_library[function_name]['code'] = function_library[function_name]['versions'][target_version]
            function_library[function_name]['version'] = target_version
            return True, f"Function {function_name} rolled back to version {target_version}."
        else:
            return False, f"Version {target_version} not found for function {function_name}."
    return False, f"Function {function_name} not found in the library."

# API 7 - Allow for searching functions in the library based on runtime environment
def searchFunctionByRuntime(runtime: str) -> list:
    matching_functions = []
    for function_name, function_data in function_library.items():
        # Check if the runtime environment matches the specified runtime needed
        if function_data.get("runtime_env") == runtime:
            # Append the function name and version to the functions list that match
            matching_functions.append({
                "function_name": function_name,
                "version": function_data.get("version")
            })
    return matching_functions

def publishFunction(function_name: str) -> bool:
    if function_name in function_library:
        function_library[function_name]['published'] = True
        return True, f"Function {function_name} published successfully." 
    return False, f"Failed to publish function {function_name}."

def unpublishFunction(function_name: str) -> bool:
    if function_name in function_library:
        function_library[function_name]['published'] = False
        return True, f"Function {function_name} unpublished successfully." 
    return False, f"Failed to unpublish function {function_name}."

def archiveFunction(function_name: str) -> bool:
    '''Description:
        The archiveFunction API archives a function, which removes it from active usage but retains its information and code in the library for future reference.
        Archived functions can be restored later if needed.

        Input:
        function_name: The name of the function to archive. (string)
        
        Output:
        True if the function is successfully archived, False otherwise.
    '''
    try:
        if function_name in function_library:
            function_library[function_name]["archive_status"] = True 
            return True, f"Function {function_name} archived."
        else:
            return False, f"Function {function_name} not in function library."
    except:
        return False, f"Unexpected error archiving function {function_name}."
