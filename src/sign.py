from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def encrypt_and_sign(data, private_key):

    public_key = private_key.public_key()

    encrypted_data = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA224()),
            algorithm=hashes.SHA224(),
            label=None
        )
    )

    signature = private_key.sign(
        encrypted_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA224()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA224()
    )

    return encrypted_data, signature

def verify(data, signature, key):
    return key.public_key().verify(
        signature,
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA224()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA224()
    )


def decrypt_and_verify(encrypted_data, signature, private_key):

    private_key.public_key().verify(
        signature,
        encrypted_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA224()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA224()
    )

    data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA224()),
            algorithm=hashes.SHA224(),
            label=None
        )
    )

    return data

def key_gen():

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    return private_key


def test_encrypt_decrypt():
    private_key = key_gen()
    data = b"my secret data"

    encrypted_data, signature = encrypt_and_sign(data, private_key)

    decrypted_data = decrypt_and_verify(encrypted_data, signature, private_key)

    print(data)
    print(decrypted_data)

if __name__ == "__main__":
    test_encrypt_decrypt()

