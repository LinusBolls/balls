import enum

from src.errors import MissingPermissionError

class Perms(enum.Enum):
    """Enum of permissions accesible by both dot and bracket notation.

    A list of members is reducable to a single int w/o loss of information
    """
    MANAGE_USERS = 1
    MANAGE_GAMES = 2
    MANAGE_MATCHES = 4
    MANAGE_RANKINGS = 8

    CREATE_USERS = 16
    CREATE_GAMES = 32
    CREATE_MATCHES = 64

    VIEW_USERS = 128
    VIEW_GAMES = 256
    VIEW_MATCHES = 512
    VIEW_RANKINGS = 1024

NO_ACCOUNT_REQUIRED_PERMS_LIST = [
    Perms.VIEW_USERS,
    Perms.VIEW_GAMES,
    Perms.VIEW_MATCHES,
    Perms.VIEW_RANKINGS,
]
ACCOUNT_REQUIRED_PERMS_LIST = [
    Perms.CREATE_MATCHES,
]
MAIL_CONFIRM_REQUIRED_PERMS_LIST = [ 
    Perms.CREATE_GAMES,
]
def has_permissions(user, permissions_list):

    """
    checks if all permissions in permissions_list are included in either
    user.perms_list or NO_ACCOUNT_REQUIRED_PERMS_LIST.

    example:

    if not has_permissions(User.from_token(db, request.cookies.get("token"))[0], [ Perms.VIEW_USERS ]):
        raise MissingPermissionError

    Perms.VIEW_USERS is included in NO_ACCOUNT_REQUIRED_PERMS_LIST,
    so no cookie is required for that action.
    """

    account_required = not set(permissions_list).issubset(NO_ACCOUNT_REQUIRED_PERMS_LIST)

    if not account_required:
        return True

    if user is None:
        return False

    return set(permissions_list).issubset(user.perms_list + NO_ACCOUNT_REQUIRED_PERMS_LIST)

def assert_has_permissions(user, permissions_list):

    is_authorized = has_permissions(user, permissions_list)

    if not is_authorized:
        raise MissingPermissionError

def encode_perms(perms_list, perms_enum = Perms):
    perms_int = 0

    try:
        iter(perms_list)
    except TypeError:
        return 0

    for permission in perms_list:

        if permission not in perms_enum.__members__ and permission not in perms_enum:
            continue

        if isinstance(permission, str):
            permission = perms_enum[permission]

        perms_int += permission.value

    return perms_int

def decode_perms(perms_int, perms_enum = Perms):

    if not isinstance(perms_int, int) or perms_int == 0:
        return []

    sum = 0
    perms_list = []

    nums = list(perms_enum)
    nums.reverse()

    for i in nums:
        if i.value + sum <= perms_int:
            perms_list.append(Perms._value2member_map_[i.value])
            sum += i.value

    return perms_list