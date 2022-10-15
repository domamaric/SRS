import argparse

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes


class PasswManager:
    def __init__(self, master_passw):
        self.master_password = master_passw
        self.salt = "tinf srs uui"

    def find_sha_key(self):
        aes_key = scrypt(self.master_password, self.salt, 32, N=2 ** 18, r=8,
                         p=1)
        sha = SHA256.new()
        sha.update(aes_key)
        return sha

    @staticmethod
    def write_sha_key(sha_key):
        with open('shakey.bin', 'wb') as f:
            f.write(sha_key.digest())


def main(argv):
    if argv.init is not None:
        pm = PasswManager(argv.init)
        pm.write_sha_key(pm.find_sha_key())
        print("[PROGRAM] Alat za pohranu lozinki inicijaliziran.")
    elif argv.save is not None:  # [masterPassw, webLok, sifra]
        with open('shakey.bin', 'rb') as f:
            file_key = f.read()

        pm = PasswManager(argv.save[0])
        sha_key = pm.find_sha_key()

        if sha_key.digest() == file_key:  # Glavne su lozinke identične
            new_key = get_random_bytes(32)
            aes = AES.new(sha_key.digest(), AES.MODE_EAX)
            encrypted_key, tag = aes.encrypt_and_digest(new_key)

            with open('passwords.bin', 'a+b') as f:
                new_chiper_key = AES.new(new_key, AES.MODE_EAX)
                x, y = new_chiper_key.encrypt_and_digest(bytes(
                    argv.save[1] + ',' + argv.save[2], 'utf-8', 'ignore'))
                arguments = b'janje'.join(
                	[aes.nonce, encrypted_key, tag, new_chiper_key.nonce, x, y, b'\n']
                	)
                f.write(arguments)
            print("[PROGRAM] Spremljena lozinka za lokaciju {}.".format(
                argv.save[1]))
        else:
            print("[ERROR] Glavne zaporke nisu identične.")
    elif argv.get is not None:  # [masterPassw, weblok]
        with open('shakey.bin', 'rb') as f:
            file_key = f.read()

        pm = PasswManager(argv.get[0])
        sha_key = pm.find_sha_key()

        if sha_key.digest() == file_key:
            with open('passwords.bin', "rb") as f:
                for line in f:
                    lst = line.split(b'janje')
                    aes = AES.new(sha_key.digest(), AES.MODE_EAX, nonce=lst[0])
                    key = aes.decrypt(lst[1])
                    try:
                        aes.verify(lst[2])
                    except ValueError as e:
                        exit(e)

                    aes = AES.new(key, AES.MODE_EAX, nonce=lst[3])
                    pair = aes.decrypt(lst[4])
                    try:
                        aes.verify(lst[5])
                    except ValueError as e:
                        exit(e)

                    pair = pair.decode('utf-8', 'ignore')
                    if pair.split(',')[0] == argv.get[1]:
                        print("[PROGRAM] Lozinka za {} je: {}".format(
                            argv.get[1], pair.split(',')[1]))
        else:
            print("[ERROR] Glavne lozinke nisu identične.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Prototip alata za pohranu zaporki.')
    parser.add_argument('-i', '--init', type=str, metavar="msif",
                        help='Inicijaliziraj upravitelja lozinkama')
    parser.add_argument('-s', '--save', nargs=3, type=str,
                        help='Spremi lozinku za web-lokaciju',
                        metavar=('msif', 'lok', 'sif'))
    parser.add_argument('-g', '--get', nargs=2, type=str,
                        help='Dohvati lozinku za web-lokaciju',
                        metavar=('sif', 'lok'))
    main(parser.parse_args())

