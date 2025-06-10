# Upute za korištenje alata za pohranu lozinki

Ovaj alat za pohranu lozinki koristi modernu simetričnu kriptografiju. Radi iz naredbenog retka,
a podatke sprema na disk u zaštićenom obliku. Zasniva se na AES-GCM enkripciji sa ključem dobivenim iz
glavne zaporke pomoću Scrypt funkcije za derivaciju ključeva sa slučajnim salt-om.

**NAPOMENA**: Sve se datoteke nalaze u radnome kazalu!

## I. korak: Inicijalizacija alata i postavljanje glavne zaporke

```bash
python password_manager.py --init <glavna_zaporka>
```

**Opis koraka**: Ovaj korak generira kriptografski siguran slučajni salt koji se sprema u datoteku `salt.bin`
i stvara praznu bazu podataka `passwords.json` u radnome kazalu. Salt se koristi zajedno s glavnom zaporkom
za derivaciju ključa pomoću Scrypt algoritma, što pruža zaštitu od napada rječnikom i "rainbow table" napada.

## II. korak: Spremanje zaporki za zadanu web lokaciju

```bash
python password_manager.py --put <glavna_zaporka> <web_lokacija> <sifra>
```

**Opis koraka**: Ovaj korak zapisuje zaporku za određenu web lokaciju (glavna zaporka mora biti jednaka
onoj prethodno definiranoj). Enkripcija se provodi AES-GCM zaštitom (Galois/Counter Mode) koja pruža i
povjerljivost i autentičnost.
Za svaki se par adresa-zaporka generira jedinstveni nonce (broj koji se koristi samo jednom). Adresa i 
zaporka zajedno se kriptiraju kako bi se osigurala maksimalna zaštita. Podaci se pohranjuju u JSON formatu
 u datoteku `passwords.json`. Ako već postoji zaporka za zadanu adresu, stara se zaporka zamjenjuje novom.

## III. korak: Dohvat zaporke za zadanu web lokaciju

```bash
python password_manager.py --get <glavna_zaporka> <web_lokacija>
```

**Opis koraka**: Ovaj korak vraća zaporku za zadanu adresu (glavna zaporka mora biti jednaka početno definiranoj). 
Provodi se dekripcija podataka koristeći spremljeni nonce i AES-GCM algoritam. Autentifikacijski mehanizam GCM
osigurava integritet podataka i štiti od napada zamjene ili manipulacije podacima.

---

Više informacija o formatu upisa argumenata može se vidjeti sljedećom naredbom u naredbenom retku:

```bash
python password_manager.py -h
```

### Sigurnosne značajke

1. **Povjerljivost zaporki**: Sve zaporke su zaštićene AES-GCM enkripcijom s ključem izvedenim iz glavne zaporke.
2. **Povjerljivost adresa**: Adrese su također kriptirane zajedno sa zaporkama.
3. **Integritet podataka**: AES-GCM pruža autentificiranu enkripciju koja štiti od manipulacije podacima.
4. **Zaštita od napada zamjene**: Svaki par adresa-zaporka enkriptiran je zasebno s jedinstvenim nonce-om.
5. **Sigurna derivacija ključa**: Koristi Scrypt algoritam sa slučajnim salt-om za derivaciju ključa iz glavne zaporke.

### Zahtjevi

Za rad programa potrebno je imati instaliranu Python biblioteku `cryptography`:

```bash
pip install cryptography
```
