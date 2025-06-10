#!/bin/bash

# Clean up previous database.json if it exists, for a clean run
if [ -f database.json ]; then
    rm database.json
    printf "Stvaram bazu 'database.json' u demostracijske svrhe.\n\n"
fi

printf "U sklopu vježbe potrebno je implementirati dva alata: jedan za upravljanje\n"
printf "korisničkim računima (usermgmt.py) i drugi za prijavu korisnika (login.py).\n"
printf "Oba alata koriste modernu kriptografiju za sigurno pohranjivanje zaporki.\n"

printf "\n============================== usermgmt.py ==========================================\n"
printf "Pokretanje alata za upravljanje korisničkim računima.\n"
printf "Dodajemo korisnika 'korisnik1' u bazu. Bit ćete zatraženi da unesete zaporku.\n\n"
printf "$ python3 usermgmt.py add korisnik1\n"

python3 usermgmt.py add korisnik1

printf "\n-------------------------------------------------------------------------------------\n"
printf "Pokušajmo dodati korisnika s istim imenom ('korisnik1'). Program bi trebao vratiti poruku pogreške.\n\n"
printf "$ python3 usermgmt.py add korisnik1\n"

python3 usermgmt.py add korisnik1

printf "\n-------------------------------------------------------------------------------------\n"
printf "Brišemo korisnika 'korisnik1' iz baze podataka pomoću parametra 'del'.\n\n"
printf "$ python3 usermgmt.py del korisnik1\n"

python3 usermgmt.py del korisnik1

printf "\n-------------------------------------------------------------------------------------\n"
printf "Dodajmo korisnika 'korisnik2' u bazu.\n\n"
printf "$ python3 usermgmt.py add korisnik2\n"

python3 usermgmt.py add korisnik2

printf "\n-------------------------------------------------------------------------------------\n"
printf "Dodajmo korisnika 'korisnik3' u bazu.\n\n"
printf "$ python3 usermgmt.py add korisnik3\n"

python3 usermgmt.py add korisnik3

printf "\n-------------------------------------------------------------------------------------\n"
printf "Želimo korisniku 'korisnik2' forsirati promjenu zaporke na sljedećoj prijavi.\n"
printf "To ostvarujemo slanjem argumenta 'forcepass' alatu 'usermgmt.py'.\n\n"
printf "$ python3 usermgmt.py forcepass korisnik2\n"

python3 usermgmt.py forcepass korisnik2

printf "\n-------------------------------------------------------------------------------------\n"
printf "Želimo korisniku 'korisnik3' promijeniti zaporku. Alatu šaljemo argument 'passwd'.\n"
printf "Prvo ćemo namjerno unijeti krivu lozinku kako bi se demonstrirala poruka o pogrešci.\n\n"
printf "$ python3 usermgmt.py passwd korisnik3\n"

python3 usermgmt.py passwd korisnik3

printf "\n-------------------------------------------------------------------------------------\n"
printf "Sada ćemo ispravno promijeniti lozinku za 'korisnik3'.\n\n"
printf "$ python3 usermgmt.py passwd korisnik3\n"

python3 usermgmt.py passwd korisnik3

printf "\n-------------------------------------------------------------------------------------\n"
printf "Sada se prebacimo na alat 'login.py' koji služi za demonstraciju prijave korisnika.\n"
printf "================================ login.py =============================================\n"

printf "\nPokušajmo se logirati kao 'korisnik2'. Prvo ćemo unijeti pogrešnu zaporku.\n\n"
printf "$ python3 login.py korisnik2\n"

python3 login.py korisnik2

printf "\n-------------------------------------------------------------------------------------\n"
printf "Sada se prijavimo kao 'korisnik2' s ispravnom zaporkom. Budući da smo forsirali promjenu\n"
printf "zaporke za 'korisnik2', sustav će nas zatražiti da odmah unesemo novu zaporku.\n\n"
printf "$ python3 login.py korisnik2\n"

python3 login.py korisnik2

printf "\n-------------------------------------------------------------------------------------\n"
printf "Ponovno se prijavimo kao 'korisnik2' s novom zaporkom. Sada ne bi smjelo biti zahtjeva za promjenom zaporke.\n\n"
printf "$ python3 login.py korisnik2\n"

python3 login.py korisnik2

printf "\n-------------------------------------------------------------------------------------\n"
printf "Pokušajmo se prijaviti kao 'korisnik3' s nedavno promijenjenom zaporkom.\n\n"
printf "$ python3 login.py korisnik3\n"

python3 login.py korisnik3

printf "\nDemonstracija završena.\n"

if [ -f database.json ]; then
    rm database.json
    printf "Brišem bazu 'database.json' u demostracijske svrhe.\n"
fi
