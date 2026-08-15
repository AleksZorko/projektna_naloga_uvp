import os
from bs4 import BeautifulSoup
import pandas as pd

def varno_preberi_stevilko(element, mozni_atributi):
    if not element:
        return None
    if isinstance(mozni_atributi, str):
        mozni_atributi = [mozni_atributi]
    
    for atr in mozni_atributi:
        celica = element.find(['td', 'th'], {'data-stat': atr})
        if celica and celica.text.strip():
            besedilo = celica.text.strip().replace(',', '.')
            try:
                return float(besedilo)
            except ValueError:
                continue
    return None

def izlusci_popolno_statistiko():
    mapa = "html_strani"
    vsi_podatki = []

    print("Začenjam iskanje in izluščanje, vključno z naprednimi meti (polaganja in polrazdalja)...")

    attr_3pa = ['fg3a', 'fg3a_per_g']
    attr_3p  = ['fg3', 'fg3_per_g']
    attr_3pct= ['fg3_pct']
    attr_2pa = ['fg2a', 'fg2a_per_g']
    attr_2p  = ['fg2', 'fg2_per_g']
    attr_2pct= ['fg2_pct']
    attr_fta = ['fta', 'fta_per_g']
    attr_ft  = ['ft', 'ft_per_g']
    attr_ftpct= ['ft_pct']
    attr_pts = ['pts', 'pts_per_g']
    attr_orb = ['orb', 'orb_per_g']

    attr_0_3 = ['pct_fga_00_03', 'fgpa_pct_from_0_to_3']
    attr_10_16 = ['pct_fga_10_16', 'fgpa_pct_from_10_to_16']
    attr_16_3p = ['pct_fga_16_xx', 'fgpa_pct_from_16_to_3p', 'fgpa_pct_from_16_to_xx']

    for ime_datoteke in os.listdir(mapa):
        if ime_datoteke.endswith(".html"):
            leto = int(ime_datoteke.split("_")[2].split(".")[0])
            pot = os.path.join(mapa, ime_datoteke)
            
            with open(pot, 'r', encoding='utf-8') as f:
                vsebina = f.read()
                
            vsebina = vsebina.replace('<!--', '').replace('-->', '')
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

            tabela_osnovna = soup.find('table', id='per_game-team')
            if not tabela_osnovna:
                tabela_osnovna = soup.find('table', id='team-stats-per_game')

            tabela_streljanje = soup.find('table', id='shooting-team')

            liga_podatki = {}
            prvak_podatki = {}
            zmagovalec_cisto = zmagovalec.lower().replace('*', '').strip()

            if tabela_osnovna:
                noge_tabele = tabela_osnovna.find('tfoot')
                if noge_tabele:
                    liga_podatki.update({
                        'Liga_poskusi_3p': varno_preberi_stevilko(noge_tabele, attr_3pa),
                        'Liga_zadetki_3p': varno_preberi_stevilko(noge_tabele, attr_3p),
                        'Liga_odstotek_3p': varno_preberi_stevilko(noge_tabele, attr_3pct),
                        'Liga_poskusi_2p': varno_preberi_stevilko(noge_tabele, attr_2pa),
                        'Liga_zadetki_2p': varno_preberi_stevilko(noge_tabele, attr_2p),
                        'Liga_odstotek_2p': varno_preberi_stevilko(noge_tabele, attr_2pct),
                        'Liga_poskusi_PM': varno_preberi_stevilko(noge_tabele, attr_fta),
                        'Liga_zadetki_PM': varno_preberi_stevilko(noge_tabele, attr_ft),     # <-- DODANO
                        'Liga_odstotek_PM': varno_preberi_stevilko(noge_tabele, attr_ftpct), # <-- DODANO
                        'Liga_tocke': varno_preberi_stevilko(noge_tabele, attr_pts),
                        'Liga_napadalni_skoki': varno_preberi_stevilko(noge_tabele, attr_orb),
                    })
                
                tbody = tabela_osnovna.find('tbody')
                if tbody and zmagovalec != "Neznano":
                    for tr in tbody.find_all('tr'):
                        ekipa_celica = tr.find(['td', 'th'], {'data-stat': ['team', 'team_name', 'team_id']})
                        if ekipa_celica:
                            ekipa_tekst = ekipa_celica.text.lower().replace('*', '').strip()
                            if zmagovalec_cisto in ekipa_tekst or ekipa_tekst in zmagovalec_cisto:
                                prvak_podatki.update({
                                    'Prvak_poskusi_3p': varno_preberi_stevilko(tr, attr_3pa),
                                    'Prvak_odstotek_3p': varno_preberi_stevilko(tr, attr_3pct),
                                    'Prvak_poskusi_2p': varno_preberi_stevilko(tr, attr_2pa),
                                    'Prvak_tocke': varno_preberi_stevilko(tr, attr_pts),
                                    'Prvak_napadalni_skoki': varno_preberi_stevilko(tr, attr_orb),
                                })
                                break

            if tabela_streljanje:
                noge_streljanje = tabela_streljanje.find('tfoot')
                if noge_streljanje:
                    liga_podatki.update({
                        'Liga_delez_0_3': varno_preberi_stevilko(noge_streljanje, attr_0_3),
                        'Liga_delez_10_16': varno_preberi_stevilko(noge_streljanje, attr_10_16),
                        'Liga_delez_16_3p': varno_preberi_stevilko(noge_streljanje, attr_16_3p),
                    })

                tbody_streljanje = tabela_streljanje.find('tbody')
                if tbody_streljanje and zmagovalec != "Neznano":
                    for tr in tbody_streljanje.find_all('tr'):
                        ekipa_celica = tr.find(['td', 'th'], {'data-stat': ['team', 'team_name', 'team_id']})
                        if ekipa_celica:
                            ekipa_tekst = ekipa_celica.text.lower().replace('*', '').strip()
                            if zmagovalec_cisto in ekipa_tekst or ekipa_tekst in zmagovalec_cisto:
                                prvak_podatki.update({
                                    'Prvak_delez_0_3': varno_preberi_stevilko(tr, attr_0_3),
                                    'Prvak_delez_10_16': varno_preberi_stevilko(tr, attr_10_16),
                                    'Prvak_delez_16_3p': varno_preberi_stevilko(tr, attr_16_3p),
                                })
                                break

            if liga_podatki:
                zdruzeni_podatki = {'Leto': leto, 'Zmagovalna_ekipa': zmagovalec}
                zdruzeni_podatki.update(liga_podatki)
                if prvak_podatki:
                    zdruzeni_podatki.update(prvak_podatki)
                vsi_podatki.append(zdruzeni_podatki)

    vsi_podatki = sorted(vsi_podatki, key=lambda x: x['Leto'])
    
    df = pd.DataFrame(vsi_podatki)
    ime_csv = 'nba_popolna_statistika.csv'
    df.to_csv(ime_csv, index=False)
    print(f"\nKončano! Podatki so uspešno shranjeni v '{ime_csv}'.")

if __name__ == "__main__":
    izlusci_popolno_statistiko()
    