import os
import requests
import time

def shrani_strani(zacetno_leto, koncno_leto):
    mapa = "html_strani"

    if not os.path.exists(mapa):
        os.makedirs(mapa)
        print(f"Ustvaril sem mapo: {mapa}")
    for leto in range(zacetno_leto, koncno_leto + 1):
        url = f"https://www.basketball-reference.com/leagues/NBA_{leto}.html"
        pot_do_datoteke = os.path.join(mapa, f"nba_sezona_{leto}.html")

        if os.path.exists(pot_do_datoteke):
            print(f"Stran za leto {leto} že obstaja. Preskakujem...")
            continue

        print(f"Prenašam podatke za leto {leto}...")
        odgovor = requests.get(url)

        if odgovor.status_code == 200:
            with open(pot_do_datoteke, 'w', encoding= 'utf-8') as f:
                f.write(odgovor.text)
            print(f"Shranjeno: {pot_do_datoteke}")
        else:
            print(f"Napaka pri prenosu leta {leto}. Koda napake: {odgovor.status_code}")
        time.sleep(3)
if __name__ == "__main__":
    print("Začenjam prenos...")
    shrani_strani(2000, 2025)
    print("Konec prenosa!")  