#!/bin/bash
printf "Prikaz pomocnog izbornika programa...\n\n"
python password_manager.py --help

printf "\nInicijalizacija alata masterPassword glavnom lozinkom\n"
python password_manager.py --init masterPassword

printf "\nSpremanje lozinke neprobojnaSifra za adresu fer.unizg.hr\n\n"
python password_manager.py --put masterPassword fer.unizg.hr neprobojnaSifra

printf "\nDohvat lozinke za adresu fer.unizg.hr\n\n"
python password_manager.py --get masterPassword fer.unizg.hr

printf "\nSpremanje lozinke jakoteskaSifra za adresu chatgpt.com\n\n"
python password_manager.py --put masterPassword chatgpt.com jakoteskaSifra

printf "\nDohvat lozinke za adresu chatgpt.com\n\n"
python password_manager.py --get masterPassword chatgpt.com

printf "\nDohvat lozinke za adresu chatgpt.com pogresnom glavnom lozinkom\n\n"
python password_manager.py --get masterPasssssword chatgpt.com