import hashlib

data = b"This is the data to be hashed"
hash_object = hashlib.sha256()
hash_object.update(data)
hex_digest = hash_object.hexdigest()

print("Hash value:", hex_digest)