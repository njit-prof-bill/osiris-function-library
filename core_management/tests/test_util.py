from unittest.mock import MagicMock
from core_management.server import util

# addFunctionToLibrary tests
def test_fail_add_function():
    util.addFunctionToLibrary = MagicMock(return_value=(False, "Function already exists."))
    success, _ = util.addFunctionToLibrary("function_name", "code", "Python", "1.0")
    assert success == False

def test_success_add_function():
    util.addFunctionToLibrary = MagicMock(return_value=(True, "Function added successfully."))
    success, _ = util.addFunctionToLibrary("function_name", "code", "Python", "1.0")
    assert success == True

# archiveFunction tests
def test_fail_archive_function():
    util.archiveFunction = MagicMock(return_value=(False, "Function not in function library."))
    success, _ = util.archiveFunction("function_name")
    assert success == False

def test_success_archive_function():
    util.archiveFunction = MagicMock(return_value=(True, "Function archived."))
    success, _ = util.archiveFunction("function_name")
    assert success == True

# listFunctionsInLibrary tests
def test_list_functions_empty_library():
    util.listFunctionsInLibrary = MagicMock(return_value=(False, "No functions available in the library."))
    success, _ = util.listFunctionsInLibrary()
    assert success == False

def test_list_functions_with_entries():
    util.listFunctionsInLibrary = MagicMock(return_value=(True, "Name: func1, Version: 1.0, Runtime: Python"))
    success, _ = util.listFunctionsInLibrary()
    assert success == True

# getFunctionDetails tests
def test_get_function_details_not_found():
    util.getFunctionDetails = MagicMock(return_value=(False, "Function not found."))
    success, _ = util.getFunctionDetails("non_existent_function")
    assert success == False

def test_get_function_details_success():
    util.getFunctionDetails = MagicMock(return_value=(True, "Name: func1, Version: 1.0, Runtime: Python, Code: def func1(): pass"))
    success, _ = util.getFunctionDetails("func1")
    assert success == True
