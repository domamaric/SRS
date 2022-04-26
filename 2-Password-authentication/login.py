import json
from base64 import b64decode
from getpass import getpass
from sys import argv

from Crypto.Cipher import AES

from korisnik import Korisnik


def main(korisnicko_ime):
    with open("baza.json", "r") as f:
        sadrzaj = json.load(f)

    lozinka = getpass()

    postoji = False
    for element in sadrzaj:
        if element["korisnik"] == korisnicko_ime:
            korisnik = Korisnik(korisnicko_ime)
            aes = AES.new(korisnik.sha_kljuc.digest(), AES.MODE_EAX,
                          nonce=b64decode(element["aes nonce"]))
            kljuc = aes.decrypt(b64decode(element["kript kljuc"]))
            try:
                aes.verify(b64decode(element["oznaka"]))
            except ValueError as e:
                print(e)
                exit("Data may have been compromised.")

            aes_novi = AES.new(kljuc, AES.MODE_EAX,
                               nonce=b64decode(element["novi aes nonce"]))
            x = aes_novi.decrypt(b64decode(element["novi kript kljuc"]))
            try:
                aes_novi.verify(b64decode(element["nova ozn"]))
            except ValueError as e:
                print(e)
                print("Username or password incorrect.")
            loz = x.decode('ascii', 'ignore')

            if element["promjena"]:  # slucaj promjene lozinke
                if loz != lozinka:  # stara lozinka nije jednaka prethodnoj
                    exit("Username or password incorrect")
                else:
                    nova_lozinka = getpass("New password: ")
                    nova_ponovljena = getpass("Repeat new password: ")
                    if nova_lozinka == nova_ponovljena:
                        korisnik.zamjeni(lozinka)
                        print("Login successful.")
                    else:
                        print("Username or password incorrect.")
            else:  # slucaj logiranja korisnika
                if loz == lozinka:
                    print("Login successful.")
                else:
                    print("Username or password incorrect.")
            postoji = True
            break

    if not postoji:
        print("Username or password incorrect.")


if __name__ == "__main__":
    main(argv[1])
