import enum

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

UNCONDITIONAL_PERM_LIST = [
    Perms.CREATE_MATCHES,
    Perms.VIEW_RANKINGS,
]
MAIL_CONFIRMED_PERM_LIST = [
    Perms.VIEW_USERS,
    Perms.VIEW_GAMES,
    Perms.VIEW_MATCHES,
]
# try:
#     some_object_iterator = iter(some_object)
# except TypeError as te:
#     print(some_object, 'is not iterable')

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