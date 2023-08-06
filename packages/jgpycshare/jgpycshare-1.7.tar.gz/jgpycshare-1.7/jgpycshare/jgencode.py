from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Hash import SHA256
import base64
from Crypto.Cipher import AES
# from Crypto import Random


class JGRSA:

    def __init__(self,app_private_key_path=None,app_public_key_path=None):
        self.app_private_key = None
        self.app_public_key = None

        if app_private_key_path is not None:
            with open(app_private_key_path) as fp:
                self.app_private_key = RSA.importKey(fp.read())

        if app_public_key_path is not None:
            with open(app_public_key_path) as fp:
                self.app_public_key = RSA.importKey(fp.read())

    def ali_pri_sign(self, unsigned_string):
        unsigned_string = unsigned_string.encode("utf-8")
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        # base64 编码，转换为unicode表示并移除回车
        signature = signer.sign(SHA256.new(unsigned_string))
        signed = base64.encodebytes(signature).decode("utf8").replace("\n", "")
        return signed

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.app_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, base64.decodebytes(signature.encode("utf8"))):
            return True
        return False

    def ali_pub_check_sign(self, data, signature):
        return self._verify(data, signature)

    def pub_encode(self, encodestr):
        encodestr = encodestr.encode("utf-8")
        rsakey = self.app_public_key
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(encodestr))
        print(cipher_text)
        return cipher_text

    def pri_decode(self, decodestr):
        rsakey = self.app_private_key
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        # random_generator = Random.new().read
        text = cipher.decrypt(base64.b64decode(decodestr), None)
        return text.decode('utf8')

    @staticmethod
    def ali_pub_check_signfor_key(data, signature, pubkey):
         # 开始计算签名
        key = RSA.importKey(pubkey)
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(data.encode("utf8"))
        if signer.verify(digest, base64.decodebytes(signature.encode("utf8"))):
            return True
        return False

    @staticmethod
    def ali_pri_sign_key(unsigned_string, prikey):
        prikey = RSA.importKey(prikey)
        unsigned_string = unsigned_string.encode("utf-8")
        signer = PKCS1_v1_5.new(prikey)
        # base64 编码，转换为unicode表示并移除回车
        signature = signer.sign(SHA256.new(unsigned_string))
        signed = base64.encodebytes(signature).decode("utf8").replace("\n", "")
        return signed

    @staticmethod
    def pri_decode_key(decodestr, prikey):
        rsakey = RSA.importKey(prikey)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        # random_generator = Random.new().read
        text = cipher.decrypt(base64.b64decode(decodestr), None)
        return text.decode('utf8')

    @staticmethod
    def pub_encode_key(encodestr, pubkey):
        rsakey = RSA.importKey(pubkey)
        encodestr = encodestr.encode("utf-8")
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(encodestr))
        print(cipher_text)
        return cipher_text


class JGAES:
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
 
    def encrypt(self, text):
        import base64
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 16                    
        count = len(text.encode('utf-8'))    
        print(count)               
        if (count % length != 0):
            add = length - (count % length)
        else:
            add = 0            
        text1 = text + ('\0' * add)    
        self.ciphertext = cryptor.encrypt(text1)        
        cryptedStr = str(base64.b64encode(self.ciphertext),encoding='utf-8')
        return cryptedStr
      
 
 
    def decrypt(self, text):
        import base64, json
        base_text = base64.b64decode(text)
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(base_text)
        ne = plain_text.decode('utf-8').rstrip('\0')
        return ne