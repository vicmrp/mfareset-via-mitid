from pprint import pprint

from core.utils.graph import list_user_authentication_methods
from core.utils.auth_methods import prepare_auth_methods

def run(*args):

    upn = args[0] if args else "testtes@dtu.dk"
    print(f"Looking up authentication methods for: {upn}")

    methods = list_user_authentication_methods(upn)

    mfa_methods = prepare_auth_methods(methods)

    



    print("Returned methods:")
    pprint(mfa_methods)