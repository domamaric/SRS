# Upute za korištenje alata za upravljanje korisnicima i prijavu

Ovaj skup alata omogućuje upravljanje korisničkim računima i prijavu u sustav iz naredbenog retka. Implementira mehanizme za sigurno pohranjivanje zaporki koristeći modernu kriptografiju, specifično `cryptography` biblioteku u Pythonu. Zaporke se ne pohranjuju u čistom obliku, već se iz njih derivira **Fernet** ključ pomoću `Scrypt` funkcije za derivaciju ključeva sa slučajnim, jedinstvenim `salt`-om za svakog korisnika. To povećava razinu sigurnosti i zaštitu od različitih napada.

**NAPOMENA**: Sve se datoteke nalaze u radnome kazalu!

## I. Alat za upravljanje korisnicima (usermgmt.py)

Ovaj alat namijenjen je administratorima i omogućuje im upravljanje korisničkim računima.

### 1. Dodavanje novog korisnika

```bash
python usermgmt.py add <korisnicko_ime>
```

**Opis koraka**: Nakon pokretanja naredbe, alat će zatražiti unos zaporke dva puta (za potvrdu). Za svakog novog korisnika, generira se kriptografski siguran, jedinstveni `salt` koji se koristi zajedno s unesenom zaporkom za derivaciju sigurnog Fernet ključa pomoću Scrypt algoritma. Umjesto pohrane same zaporke, sustav pohranjuje enkriptirani "dokaz ključa" (`key_proof`) dobiven pomoću ovog ključa. Ovo štiti od napada rječnikom i "rainbow table" napada jer je svaki unos jedinstven. Podaci se pohranjuju u `database.json`.

### 2. Promjena zaporke postojećeg korisnika

```bash
python usermgmt.py passwd <korisnicko_ime>
```

**Opis koraka**: Alat će zatražiti unos nove zaporke dva puta. Prilikom promjene zaporke, generira se novi, jedinstveni `salt` za novu zaporku i ažurira se odgovarajući "dokaz ključa" u `database.json`. Ovo osigurava da svaka promjena zaporke ima svoju vlastitu kriptografsku zaštitu.

### 3. Forsiranje promjene zaporke korisniku

```bash
python usermgmt.py forcepass <korisnicko_ime>
```

**Opis koraka**: Ova naredba postavlja zastavicu (`force_password_change`) za navedenog korisnika u bazi podataka. Kada se korisnik sljedeći put pokuša prijaviti putem `login.py` alata, bit će prisiljen odmah promijeniti svoju zaporku.

### 4. Brisanje postojećeg korisnika

```bash
python usermgmt.py del <korisnicko_ime>
```

**Opis koraka**: Ova naredba trajno uklanja korisnički račun i sve njegove podatke iz `database.json` datoteke.

## II. Alat za prijavu korisnika (login.py)

Ovaj alat omogućuje korisnicima prijavu u sustav.
### 1. Prijava u sustav

```bash
python login.py <korisnicko_ime>
```

**Opis koraka**: Nakon pokretanja naredbe, alat će zatražiti unos zaporke. Zaporka se unosi prikriveno (nije vidljiva). Sustav zatim koristi unesenu zaporku i pohranjeni, jedinstveni `salt` korisnika kako bi derivirao Fernet ključ. Pomoću tog ključa pokušava dekriptirati pohranjeni "dokaz ključa". Ako je dekripcija uspješna, prijava je uspješna, jer to dokazuje da je unesena zaporka ispravna. U suprotnom, prijava ne uspijeva. Nakon uspješne prijave, ispisuje se poruka o uspjehu.

### 2. Promjena zaporke nakon uspješne prijave (ako je administrator prisilio)

**Opis koraka**: Ako je administrator prethodno postavio zastavicu za forsiranje promjene zaporke, nakon uspješne prijave, korisnik će biti odmah zatražen da unese i potvrdi novu zaporku. Po uspješnoj promjeni, zastavica za forsiranje promjene zaporke se automatski uklanja.

<br>
Više informacija o formatu upisa argumenata za pojedine alate može se vidjeti sljedećim naredbama u naredbenom retku:

```bash
python usermgmt.py
python login.py
```

## Sigurnosne značajke

1. Nema pohrane čiste zaporke: Zaporke se nikada ne pohranjuju u čistom tekstualnom obliku. Umjesto toga, koriste se za derivaciju kriptografskih ključeva.
2. Jaka derivacija ključa: Koristi se Scrypt algoritam s visokim troškovima procesora i memorije (n=2^18, r=8, p=1) za sigurnu derivaciju Fernet ključa iz zaporke. Ovo značajno otežava "brute-force" napade.
3. Jedinstveni salt po korisniku: Svaki korisnik ima svoj jedinstveni, slučajno generirani salt, što sprječava korištenje "rainbow table" napada i osigurava da iste zaporke različitih korisnika rezultiraju potpuno različitim pohranjenim podacima.
4. Integritet podataka: Korištenje Fernet enkripcije (koja se temelji na AES-u u CBC načinu s HMAC autentifikacijom) osigurava integritet i autentičnost podataka, štiteći od manipulacije.
5. Prikriveni unos zaporke: Alati koriste getpass modul kako bi unos zaporke bio prikriven u naredbenom retku.

## Zahtjevi

Za rad programa potrebno je imati instaliranu Python biblioteku `cryptography`. Instalacija je navedena u opisu prethodne lab. vježbe.
