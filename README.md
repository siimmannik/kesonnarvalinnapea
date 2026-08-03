# Kes on Narva linnapea?

Sait, mis vastab ühele Eesti kiiremini aeguvale küsimusele.

Robot käib igal hommikul [narva.ee](https://www.narva.ee/kontakt) lehel vaatamas,
kes on parajasti Narva linnapea, ja uuendab `data.json` faili. Sait kuvab tulemuse
koos päevaloenduri ja eelmiste hooaegadega.

Inspiratsioon: kassilviailvesonvallaline.

## Kuidas see töötab

- `index.html` — sait ise (GitHub Pages)
- `data.json` — praegune linnapea ja ametiaegade ajalugu
- `kontroll.py` — skript, mis parsib narva.ee lehelt linnapea nime
- `.github/workflows/kontroll.yml` — käivitab kontrolli igal hommikul kell 8

Kui linnapea on vahetunud, lisatakse uus hooaeg automaatselt.
