#!/usr/bin/env python3
"""Kontrollib narva.ee lehelt, kes on parajasti Narva linnapea, ja uuendab data.json."""

import json
import re
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

URL = "https://www.narva.ee/kontakt"
FAIL = "data.json"
EESTI = timezone(timedelta(hours=3))  # suveaeg; talvel +2, aga hommik on ikka hommik


def leia_linnapea(html: str):
    """Leiab lehelt nime, mis vahetult eelneb sõnale 'Linnapea' (mitte 'Abilinnapea')."""
    tekst = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    tekst = re.sub(r"<[^>]+>", "\n", tekst)
    read = [r.strip() for r in tekst.split("\n") if r.strip()]
    sona = r"[A-ZÕÄÖÜŠŽ][a-zõäöüšž]+(?:-[A-ZÕÄÖÜŠŽa-zõäöüšž][a-zõäöüšž]*)*"
    nimemuster = re.compile(rf"^{sona}(?:\s{sona})+$")
    for i, rida in enumerate(read):
        if rida == "Linnapea" and i > 0 and nimemuster.match(read[i - 1]):
            return read[i - 1]
    return None


def main():
    with open(FAIL, encoding="utf-8") as f:
        andmed = json.load(f)

    nyyd = datetime.now(EESTI)
    andmed["viimati_kontrollitud"] = nyyd.isoformat(timespec="seconds")

    try:
        paring = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (kesonnarvalinnapea-bot)"})
        with urllib.request.urlopen(paring, timeout=30) as vastus:
            html = vastus.read().decode("utf-8", errors="replace")
        nimi = leia_linnapea(html)
    except Exception as viga:
        print(f"Kontroll ebaõnnestus: {viga}", file=sys.stderr)
        nimi = None

    if nimi is None:
        andmed["kontrolli_status"] = "viga"
    else:
        andmed["kontrolli_status"] = "ok"
        if nimi != andmed["praegune"]["nimi"]:
            print(f"UUS LINNAPEA: {andmed['praegune']['nimi']} -> {nimi}")
            tana = nyyd.date().isoformat()
            if andmed["ajalugu"] and andmed["ajalugu"][0]["kuni"] is None:
                andmed["ajalugu"][0]["kuni"] = tana
            andmed["ajalugu"].insert(0, {"nimi": nimi, "alates": tana, "kuni": None})
            andmed["praegune"] = {"nimi": nimi, "alates": tana, "allikas": URL}
        else:
            print(f"Endiselt {nimi}. Rahulik hommik Narvas.")

    with open(FAIL, "w", encoding="utf-8") as f:
        json.dump(andmed, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
