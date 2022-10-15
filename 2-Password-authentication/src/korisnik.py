import json
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes


class Korisnik:
    def __init__(self, kor_ime):
        self.__korisnik = kor_ime
        self.__salt = "tinf srs uui"
        self.sha_kljuc = None
        self.__nadi_sha_kljuc()

    def __nadi_sha_kljuc(self):
        aes_kljuc = scrypt(self.__korisnik, self.__salt, 32, N=2 ** 18, r=8,
                           p=1)
        self.sha_kljuc = SHA256.new()
        self.sha_kljuc.update(aes_kljuc)

    def __spremi(self, lozinka, sadrzaj):
        novi_kljuc = get_random_bytes(32)
        aes_kljuc = AES.new(self.sha_kljuc.digest(), AES.MODE_EAX)
        kript_kljuc, oznaka = aes_kljuc.encrypt_and_digest(novi_kljuc)

        novi_aes_kljuc = AES.new(novi_kljuc, AES.MODE_EAX)
        novi_kript_klj, nova_ozn = novi_aes_kljuc.encrypt_and_digest(
            bytes(lozinka, 'utf-8', 'ignore')
        )

        sadrzaj.append({
            "korisnik": self.__korisnik,
            "promjena": False,
            "aes nonce": b64encode(aes_kljuc.nonce).decode('ascii'),
            "kript kljuc": b64encode(kript_kljuc).decode('ascii'),
            "oznaka": b64encode(oznaka).decode('ascii'),
            "novi aes nonce": b64encode(novi_aes_kljuc.nonce).decode(
                'ascii'),
            "novi kript kljuc": b64encode(novi_kript_klj).decode('ascii'),
            "nova ozn": b64encode(nova_ozn).decode('ascii')
        })

        self.spremi_u_bazu(sadrzaj)

    @staticmethod
    def spremi_u_bazu(sadrzaj):
        with open("baza.json", "w") as f:
            json.dump(sadrzaj, f, indent=4, separators=(',', ': '))

    def spremi_lozinku(self, lozinka):
        postoji = False
        sadrzaj = []
        try:
            with open("baza.json", "r") as f:
                sadrzaj = json.load(f)
        except FileNotFoundError:  # datoteka ne postoji, napravi ju
            with open("baza.json", "w+") as f:
                json.dump([], f)

        for element in sadrzaj:
            if element["korisnik"] == self.__korisnik:
                postoji = True
                exit("User already exists.")
                break

        if not postoji:
            self.__spremi(lozinka, sadrzaj)
            return True
        else:
            return False

    def zamjeni(self, lozinka):
        postoji = False

        try:
            with open("baza.json", "r") as f:
                sadrzaj = json.load(f)
        except FileNotFoundError:
            exit("File doesn't exist.")

        for elem in sadrzaj:
            if self.__korisnik == elem["korisnik"]:
                postoji = True
                break

        if not postoji:
            return False
        else:
            novi_json = [i for i in sadrzaj if
                         not (i["korisnik"] == self.__korisnik)]
            self.__spremi(lozinka, novi_json)
            return True
