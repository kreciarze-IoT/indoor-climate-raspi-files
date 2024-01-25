import base64
from Crypto.Cipher import AES


class AESCipher(object):

    def __init__(self, key: str, iv: str = None):
        self._bs = AES.block_size
        # self.key = hashlib.sha256(key.encode()).digest()
        self._key = bytes.fromhex(key)
        self._iv = bytes.fromhex(iv)

    def encrypt(self, raw, iv=None):
        if iv is None:
            if self._iv is None:
                raise ValueError("Missing iv!")
            iv = self._iv
        raw = self._pad(raw)
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        return base64.b64encode(cipher.encrypt(raw.encode()))

    def decrypt(self, enc, iv=None):
        if iv is None:
            if self._iv is None:
                raise ValueError("Missing iv!")
            iv = self._iv
        enc = base64.b64decode(enc)
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(enc)).decode('utf-8')

    def _pad(self, s):
        return s + (self._bs - len(s) % self._bs) * chr(self._bs - len(s) % self._bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


if __name__ == '__main__':
    print("===== AES test =====")

    key = '8fc2bcffbb4b1ac9b9de03588d390f3d9bf336c2c4422c90c158cc714225f629'

    # iv = Random.new().read(AES.block_size)
    iv = "142add543cac3cf704e3fe4dbdbda1a1"

    cipher = AESCipher(key, iv)

    message = 'Hello World'
    encrypted = cipher.encrypt(message)
    print("encrypted:", encrypted)

    encrypted_b = b'qmq5VKfp62UNtM1GxXPGDg=='
    print("control encrypted == encrypted:", encrypted_b == encrypted)
    decrypted = cipher.decrypt(encrypted_b)
    print("decrypted:", decrypted)

    print("===== AES test end =====")
