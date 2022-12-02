
REQUIREMENTS = {"MIN_LENGTH": 8,
                "REQUIRE_LOWER": True,
                "REQUIRE_UPPER": True,
                "REQUIRE_NUM": True,
                "REQUIRE_SPECIAL": True}


# Given a returned password strength dictionary, returns whether it passed all tests
def check_strength_of_dict(pass_dict):
    for key in pass_dict:
        if not pass_dict[key]:
            return False
    return True


# Given a password, returns a bool if it passed all or not or returns a dict of all tests if rtn_bool=False
def get_strength_bool(password, rtn_bool=True):
    out = {'Password': password}

    # Check length
    if len(password) > REQUIREMENTS["MIN_LENGTH"]:
        out["MIN_LENGTH"] = True
    else:
        out["MIN_LENGTH"] = False
    
    # Check for lower
    if REQUIREMENTS["REQUIRE_LOWER"]:
        out["REQUIRE_LOWER"] = False
        i = 0
        while i < len(password) and not out["REQUIRE_LOWER"]:
            if password[i].islower():
                out["REQUIRE_LOWER"] = True
            i += 1

    # Check for uppper
    if REQUIREMENTS["REQUIRE_UPPER"]:
        out["REQUIRE_UPPER"] = False
        i = 0
        while i < len(password) and not out["REQUIRE_UPPER"]:
            if password[i].isupper():
                out["REQUIRE_UPPER"] = True
            i += 1
    
    # Check for numbers
    if REQUIREMENTS["REQUIRE_NUM"]:
        out["REQUIRE_NUM"] = False
        i = 0
        while i < len(password) and not out["REQUIRE_NUM"]:
            if password[i].isnumeric():
                out["REQUIRE_NUM"] = True
            i += 1

    # Check for if it contains special char
    if REQUIREMENTS["REQUIRE_SPECIAL"]:
        out["REQUIRE_SPECIAL"] = not password.isalnum()

    if rtn_bool:
        return check_strength_of_dict(out)
    else:
        return out

def get_strength_dict(password):
    return get_strength_bool(password, rtn_bool=False)
