# ANALIZA PORASTI META ZA 3 TOČKE V NBA

Za projektno nalogo pri predmetu **Uvod v Programiranje** sem analiziral spremembe v količini poskusov meta za 3 točke in kako je to uplivalo na igro. Podatke sem postrgal iz spletne strani [Basketball reference](https://www.basketball-reference.com) analiziral pa sem jih z uporabo jupyter notebooka.

## Pridobivanje in obdelava podatkov

V datoteki prenos_strani.py se nahaja funkcija s katero sem spraskal podatke za posamezna leta od 2020-2025 iz spletne strani, potem pa sem jih uredil z funkcijami v datoteki izlusci_podatke.py, ter te shranil v datoteko nba_popolna_statistika.csv

## Analiza

V datoteki **analiza.ipynb** sem z uporabo knjižnic Pandas in Matplotlib uvozil podatke ter iz njih naredil grafe za boljši vizualni prikaz podatkov:

* **Graf 1:** Sprememba načina igre v NBA (2000–2025): Dvojke vs. Trojke
* **Graf 2:** Poskusi metov za 3 točke: Zmagovalci sezone vs. Povprečje lige
* **Graf 3:** Stabilnost in učinkovitost strelcev (2000–2025): Natančnost po tipu meta
* **Graf 4:** Eksplozija rezultatov v NBA in padec napadalnih skokov
* **Graf 5:** Konec obdobja polrazdalje: Delež metov po oddaljenosti od koša (polaganja vs. polrazdalja)

## Ugotovitve

Na podlagi analiziranih podatkov sem ugotovil, da je porast poskusov za 3 točke močno vplival na zmanjšanje števila klasičnih metov za 2 točki (predvsem metov s polrazdalje, ki so skoraj izginili). Kljub drastično večjemu volumnu poskusov za tri točke, so igralci v povprečju obdržali visoko in stabilno natančnost. Prav tako se je zvišalo povprečje doseženih točk na tekmo, medtem ko je število napadalnih skokov zaradi širjenja igre navzven upadlo.

### Navodila za uporabo

Če bi želeli program preizkusiti tudi sami, sledite naslednjim korakom:

1. Prenesite datoteke `prenos_strani.py`, `izlusci_podatke.py` in `analiza.ipynb` ter jih odprite v urejevalniku (npr. VS Code).
2. V terminalu najprej zaženite **`prenos_strani.py`**, da skripta prenese vse potrebne HTML datoteke.
3. Ko se program zaključi, v terminalu zaženite še **`izlusci_podatke.py`**, da se ustvari datoteka s podatki (`nba_popolna_statistika.csv`).
4. Na koncu odprite zvezek **`analiza.ipynb`** in postopoma zaženite vse celice s kodo za prikaz analiz in grafov.
