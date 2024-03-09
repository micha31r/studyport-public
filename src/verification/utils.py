import string, random, uuid


def random_string(seed=None, size=6, chars=string.ascii_letters + string.digits):
    random.seed(seed or str(uuid.uuid4()))
    return ''.join(random.choice(chars) for _ in range(size))
