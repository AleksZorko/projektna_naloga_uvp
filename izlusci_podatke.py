import os
from bs4 import BeautifulSoup
import pandas as pd

def varno_preberi_stevilko(vrstica, atributi):
    if not vrstica: return None
    celica = vrstica.find(['td', 'th'], {'data-stat': atributi})
    if celica and celica.text.strip():
        try:
            return float(celica.text.strip())
        except ValueError:
            return None
    return None

def izlusci_popolno_statistiko():
    mapa = "html_strani"
    vsi_podatki = []

    print("Začenjam iskanje in izluščanje...")

    for ime_datoteke in os.listdir(mapa):
        if ime_datoteke.endswith(".html"):
            leto = int(ime_datoteke.split("_")[2].split(".")[0])
            pot = os.path.join(mapa, ime_datoteke)
            
            with open(pot, 'r', encoding='utf-8') as f:
                vsebina = f.read()
                
            vsebina = vsebina.replace('', '')
            soup = BeautifulSoup(vsebina, 'html.parser')
            
            zmagovalec = "Neznano"
            meta_div = soup.find('div', id='meta')
            if meta_div:
                for p in meta_div.find_all('p'):
                    if 'Champion' in p.text:
                        a_tag = p.find('a')
                        if a_tag:
                            zmagovalec = a_tag.text.replace('*', '').strip()
                            break

            tabela = soup.find('table', id='per_game-team')
            
            if tabela:
                noge_tabele = tabela.find('tfoot')
                liga_podatki = {}
                
                if noge_tabele:
                    liga_podatki = {
                        'Liga_poskusi_3p': varno_preberi_stevilko(noge_tabele, ['fg3a_per_g', 'fg3a']),
                        'Liga_zadetki_3p': varno_preberi_stevilko(noge_tabele, ['fg3_per_g', 'fg3']),
                        'Liga_odstotek_3p': varno_preberi_stevilko(noge_tabele, ['fg3_pct']),
                        'Liga_poskusi_2p': varno_preberi_stevilko(noge_tabele, ['fg2a_per_g', 'fg2a']),
                        'Liga_zadetki_2p': varno_preberi_stevilko(noge_tabele, ['fg2_per_g', 'fg2']),
                        'Liga_odstotek_2p': varno_preberi_stevilko(noge_tabele, ['fg2_pct']),
                        'Liga_poskusi_PM': varno_preberi_stevilko(noge_tabele, ['fta_per_g', 'fta']),
                        'Liga_zadetki_PM': varno_preberi_stevilko(noge_tabele, ['ft_per_g', 'ft']),
                        'Liga_odstotek_PM': varno_preberi_stevilko(noge_tabele, ['ft_pct']),
                    }

                prvak_podatki = {}
                tbody = tabela.find('tbody')
                
                if tbody and zmagovalec != "Neznano":
                    for tr in tbody.find_all('tr'):
                        ekipa_celica = tr.find(['td', 'th'], {'data-stat': ['team', 'team_name', 'team_id']})
                        if ekipa_celica and zmagovalec.lower() in ekipa_celica.text.lower():
                            prvak_podatki = {
                                'Prvak_poskusi_3p': varno_preberi_stevilko(tr, ['fg3a_per_g', 'fg3a']),
                                'Prvak_zadetki_3p': varno_preberi_stevilko(tr, ['fg3_per_g', 'fg3']),
                                'Prvak_odstotek_3p': varno_preberi_stevilko(tr, ['fg3_pct']),
                                'Prvak_poskusi_2p': varno_preberi_stevilko(tr, ['fg2a_per_g', 'fg2a']),
                                'Prvak_zadetki_2p': varno_preberi_stevilko(tr, ['fg2_per_g', 'fg2']),
                                'Prvak_odstotek_2p': varno_preberi_stevilko(tr, ['fg2_pct']),
                                'Prvak_poskusi_PM': varno_preberi_stevilko(tr, ['fta_per_g', 'fta']),
                                'Prvak_zadetki_PM': varno_preberi_stevilko(tr, ['ft_per_g', 'ft']),
                                'Prvak_odstotek_PM': varno_preberi_stevilko(tr, ['ft_pct']),
                            }
                            break

                if liga_podatki:
                    zdruzeni_podatki = {'Leto': leto, 'Zmagovalna_ekipa': zmagovalec}
                    zdruzeni_podatki.update(liga_podatki)
                    if prvak_podatki:
                        zdruzeni_podatki.update(prvak_podatki)
                    vsi_podatki.append(zdruzeni_podatki)
            else:
                print(f"Opozorilo: V letu {leto} nisem našel glavne tabele!")

    vsi_podatki = sorted(vsi_podatki, key=lambda x: x['Leto'])
    
    if not vsi_podatki:
        print("\nNAPAKA: Program še vedno ni našel nobenih podatkov!")
        return

    df = pd.DataFrame(vsi_podatki)
    ime_csv = 'nba_popolna_statistika.csv'
    df.to_csv(ime_csv, index=False)
    
    print(f"\nKončano! Podatki so uspešno shranjeni v '{ime_csv}'.")

if __name__ == "__main__":
    izlusci_popolno_statistiko()
    