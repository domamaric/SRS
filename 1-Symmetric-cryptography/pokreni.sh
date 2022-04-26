#!/bin/bash

printf "Prikaz pomocnog izbornika programa...\n\n"
python3 passwords.py --help

printf "Inicijalizacija alata masterPassword glavnom lozinkom\n"
python3 passwords.py --init masterPassword

printf "\nSpremanje lozinke asdfghjkl za adresu www.google.com\n\n"
python3 passwords.py --save masterPassword www.google.com asdfghjkl

printf "\nDohvat lozinke za adresu www.google.com\n\n"
python3 passwords.py --get masterPassword www.google.com

printf "\nSpremanje lozinke qwertzuio za adresu www.firefox.com\n\n"
python3 passwords.py --save masterPassword www.firefox.com qwertzuio

printf "\nDohvat lozinke za adresu www.firefox.com\n\n"
python3 passwords.py --get masterPassword www.firefox.com
