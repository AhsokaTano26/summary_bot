import hashlib

async def encrypt(txt):
    sha256_obj = hashlib.sha256()
    sha256_obj.update(txt.encode())
    sha256_result = sha256_obj.hexdigest()
    return sha256_result