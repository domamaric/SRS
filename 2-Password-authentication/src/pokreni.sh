#!/bin/bash

printf "U sklopu vježbe potrebno je implementirati dva alata, jedan koji omogućava upravljanje\n"
printf "lozinkama i korisničkim imenima i namijenjen je administratorima te drugi koji služi\n"
printf "za prijavu korisnika."
printf "\n============================== usermgmt.py ==========================================\n"
printf "Pokretanje alata za upravljanje lozinkama i korisničkim imenima.\n"
printf "Pokrećemo alat, te dodajemo korisnika u bazu.\n\n"
printf "$ python3 usermgmt.py add korisnik1\n"

python3 usermgmt.py add korisnik1

printf "\nŽelimo li korisnika s istim imenom dodati u bazu program vraća poruku pogreške.\n\n"
printf "$ python3 usermgmt.py add korisnik1\n"

python3 usermgmt.py add korisnik1

printf "\nŽelimo li korisnika izbrisati iz baze podataka pozovemo program s parametrom del.\n\n"
printf "$ python3 usermgmt.py del korisnik1\n"

python3 usermgmt.py del korisnik1

printf "\nDodajmo korisnika imena korisnik2 u bazu korisnika.\n\n"
printf "$ python3 usermgmt.py add korisnik2\n"

python3 usermgmt.py add korisnik2

printf "\nDodajmo korisnika imena korisnik3 u bazu korisnika.\n\n"
printf "$ python3 usermgmt.py add korisnik3\n"

python3 usermgmt.py add korisnik3

printf "\nŽelimo korisniku2 forsirati promjenu zaporke na sljedećoj prijavi.\n"
printf "To ostvarujemo slanjem argumenta forcepass alatu.\n\n"
printf "$ python3 usermgmt.py forcepass korisnik2\n"

python3 usermgmt.py forcepass korisnik2

printf "\nŽelimo li korisniku korisnik3 promijeniti lozinku alatu pošaljemo argument passwd.\n"
printf "Unosom krive lozinke sustav vraća poruku o pogrešci.\n\n"
printf "$ python3 usermgmt.py passwd korisnik3\n"

python3 usermgmt.py passwd korisnik3

printf "\nPogledamo li sada bazu podataka, vidjet ćemo zastavicu promjena korisnika\n"
printf "korisnik2 postavljenu na true što indicira promjenu lozinke.\n"
printf "Prebacimo se stoga na alat login.py koji služi za demonstraciju logiranja korisnika.\n\n"
printf "================================ login.py =============================================\n"
printf "\nPokušajmo se logirati kao korisnik2, međutim unesemo li pogrešnu lozinku tokom\n"
printf "autentikacije koriskinka sustav vraća poruku pogreške te ne dozvoljava promjenu.\n\n"
printf "$ python3 login.py korisnik2\n"

python3 login.py korisnik2

printf "\nO uspješnoj zamjeni lozinke alat obavještava korisnika.\n\n"
printf "$ python3 login.py korisnik2\n"

python3 login.py korisnik2

printf "\nPogledom na model baze korisnika možemo se uvjeriti u projenu lozinke.\n"
