import rsa


def string_to_key(key: str, acl: str):
    a_list = key.split(", ")
    map_int = list(map(int, a_list))

    if acl == "private":
        a = map_int[0]
        b = map_int[1]
        c = map_int[2]
        d = map_int[3]
        e = map_int[4]

        return rsa.PrivateKey(a, b, c, d, e)
    else:
        a = map_int[0]
        b = map_int[1]

        return rsa.PublicKey(a, b)
