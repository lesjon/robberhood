
def read_key():
    if
    with open('openai.key', "r") as keyfile:
        return keyfile.read()

def get_header():
    key = read_key()
    header = {"Authorization": "Bearer " + key}
    return header