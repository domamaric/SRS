import json
from getpass import getpass
from sys import argv

from korisnik import Korisnik


def dodavanje_korisnika(korisnicko_ime):
    lozinka = getpass()
    ponovljena_lozinka = getpass("Repeat Password: ")

    if lozinka != ponovljena_lozinka:
        exit("User add failed. Password mismatch.")

    korisnik = Korisnik(korisnicko_ime)
    if korisnik.spremi_lozinku(lozinka):
        print("User add successfuly added.")
    else:
        print("Password add failed.")


def zamjena_lozinke(korisnicko_ime):
    lozinka = getpass()
    ponovljena = getpass("Repeat Password: ")

    if lozinka != ponovljena:
        exit("Password change failed. Password mismatch.")

    korisnik = Korisnik(korisnicko_ime)
    if korisnik.zamjeni(lozinka):
        print("Password change successful.")
    else:
        print("Password change failed.")


def forsiraj_promjenu(korisnicko_ime):
    with open("baza.json", "r") as f:
        sadrzaj = json.load(f)

    for element in sadrzaj:
        if element["korisnik"] == korisnicko_ime:
            element["promjena"] = True
            break

    korisnik = Korisnik(korisnicko_ime)
    korisnik.spremi_u_bazu(sadrzaj)
    print("User will be requested to change password on next login.")


def izbrisi_korisnika(korisnicko_ime):
    with open("baza.json", "r") as f:
        sadrzaj = json.load(f)

    novi_json = [i for i in sadrzaj if
                 not (i["korisnik"] == korisnicko_ime)]

    korisnik = Korisnik(korisnicko_ime)
    korisnik.spremi_u_bazu(novi_json)
    print("User successfully removed.")


if __name__ == "__main__":  # Format ulaza: funkcija varijabla
    if argv[1].lower() == "add":
        dodavanje_korisnika(argv[2])
    elif argv[1].lower() == "passwd":
        zamjena_lozinke(argv[2])
    elif argv[1].lower() == "forcepass":
        forsiraj_promjenu(argv[2])
    elif argv[1].lower() == "del":
        izbrisi_korisnika(argv[2])
    else:
        print("Invalid program argument.")
