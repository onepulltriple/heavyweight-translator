import sys
import getpass
import os

#_____________________________________________________________________________________________________________________________#
###########################################################################
# GET SHARED FUNCTIONALITY
# Get the absolute, user-specific file path of the directory which hosts the shared functionality files
username = getpass.getuser()
absolute_path_to_shared_functionality = "C:/Users/" + username + "/Documents/__Coding Projects/01__Translation Projects/00__translation-shared-functionality"
sys.path.append(absolute_path_to_shared_functionality)

# If the directory does not exist, raise an error message
if not os.path.exists(absolute_path_to_shared_functionality):
    raise FileNotFoundError(f"Path does not exist: {absolute_path_to_shared_functionality}")
    
# Optionally list the contents of that directory as confirmation that it was found
list_of_contents = os.listdir(absolute_path_to_shared_functionality)
print("Contents of shared functionality directory:")
for item in list_of_contents : print(f"{item}")
print()

# Add the directory to the python path, if it's not already there
if absolute_path_to_shared_functionality not in sys.path:
    sys.path.append(absolute_path_to_shared_functionality)

# Optionally list the contents of the python path
list_of_contents = sys.path
print("Contents of python environment path:")
for item in list_of_contents : print(f"{item}")
print()

# Import functions from the shared functionality directory
from dict_operations import * # type: ignore
from text_operations import * # type: ignore
from file_operations import * # type: ignore
import test_constants # type: ignore

# Check that the directory is being loaded despite "not resolved" warnings
debug = test_constants.TEST01
debug = test_constants.TEST02

#_____________________________________________________________________________________________________________________________#
###########################################################################
# Import local variables
# import constants
# import input_parameters as IP


