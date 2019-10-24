import hashlib

SHORTNAME_LENGTH = 10

class ShortnameGenerator:
    def generate_shortname(self, url, try_number = 0):
        sha = hashlib.sha256()
        sha.update(str(try_number).encode())
        sha.update(url.encode())

        return sha.hexdigest()[:SHORTNAME_LENGTH]
