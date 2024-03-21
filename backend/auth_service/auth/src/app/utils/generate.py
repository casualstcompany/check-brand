import random
import string


def random_name(length):
    letters = string.ascii_lowercase
    rand_string = "".join(random.choice(letters) for i in range(length))
    return rand_string
