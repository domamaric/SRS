#!/bin/bash
printf "Prikaz pomocnog izbornika programa...\n\n"
python password_manager.py --help

printf "\nInicijalizacija alata masterPassword glavnom lozinkom\n"
python password_manager.py --init masterPassword

printf "\nSpremanje lozinke asdfghjkl za adresu www.google.com\n\n"
python password_manager.py --put masterPassword www.google.com asdfghjkl

printf "\nDohvat lozinke za adresu www.google.com\n\n"
python password_manager.py --get masterPassword www.google.com

printf "\nSpremanje lozinke qwertzuio za adresu www.firefox.com\n\n"
python password_manager.py --put masterPassword www.firefox.com qwertzuio

printf "\nDohvat lozinke za adresu www.firefox.com\n\n"
python password_manager.py --get masterPassword www.firefox.com