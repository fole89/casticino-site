"""Elenco dei capigita per la pagina Capigita.html, ricavato dall'export Droptour dei capigita attivi.

Il file Excel (es. capogita-attivi-2027.xlsx) contiene dati personali: resta solo in locale (*.xlsx è in .gitignore).
Da qui si prendono solo nome, anno «Capogita dal» e categorie, e si scrivono in data/capigita.json, che va su git.
Solo libreria standard (un .xlsx è uno zip di file XML).
Uso: python scripts/capigita.py capogita-attivi-2027.xlsx   poi   python scripts/redesign/pages.py Capigita.html Cerca.html"""
import json, os, re, sys, zipfile
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

# categorie Droptour -> chiave del filtro nella pagina (l'ordine è quello dei pulsanti, in pages.RUOLI_CAPIGITA)
CATEGORIE = {
    "Capogita CAS estivo": "estivo",
    "Capogita CAS invernale": "invernale",
    "Capogita CAS arrampicata": "arrampicata",
    "Capogita CAS escursionismo": "escursionismo",
    "Capogita seniori": "seniori",
    "Aiuto capogita": "aiuto",
    "Soccorso Alpino Svizzero": "soccorso",
}
ESCLUDI = {"Comitato CAS Ticino"}            # righe che non sono persone
NOMI = {"Bossi Elisa": "Elisa Bossi"}        # nomi scritti cognome-nome nell'export


def righe(path):
    """Righe del primo foglio come dizionari {intestazione: valore}."""
    z = zipfile.ZipFile(path)
    stringhe = []
    if "xl/sharedStrings.xml" in z.namelist():
        stringhe = ["".join(t.text or "" for t in si.iter(NS + "t"))
                    for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(NS + "si")]
    tabella = []
    for r in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(NS + "row"):
        riga = {}
        for c in r.iter(NS + "c"):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            v = c.find(NS + "v")
            if c.get("t") == "inlineStr":
                riga[col] = "".join(t.text or "" for t in c.iter(NS + "t"))
            elif v is not None:
                riga[col] = stringhe[int(v.text)] if c.get("t") == "s" else v.text
        tabella.append(riga)
    intestazioni = tabella[0]
    return [{intestazioni[k]: v.strip() for k, v in r.items() if k in intestazioni} for r in tabella[1:]]


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    persone, ignote = [], set()
    for r in righe(sys.argv[1]):
        nome = NOMI.get(r.get("Nome", ""), r.get("Nome", ""))
        if not nome or nome in ESCLUDI:
            continue
        ruoli = []
        for cat in (c.strip() for c in r.get("Categorie", "").split(",")):
            if cat in CATEGORIE and CATEGORIE[cat] not in ruoli:
                ruoli.append(CATEGORIE[cat])
            elif cat and cat not in CATEGORIE:
                ignote.add(cat)
        dal = r.get("Capogita dal", "")
        persone.append({"nome": nome, "dal": int(float(dal)) if dal else None, "ruoli": ruoli})
    if not persone:
        raise SystemExit("nessun capogita trovato: il file è quello giusto?")
    if ignote:
        print("categorie sconosciute, ignorate (aggiungile a CATEGORIE):", ", ".join(sorted(ignote)))
    # ordine alfabetico per cognome (l'ultima parola del nome)
    persone.sort(key=lambda p: (p["nome"].split()[-1].lower(), p["nome"].lower()))
    with open(os.path.join(ROOT, "data", "capigita.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"capigita": persone}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"scritto data/capigita.json: {len(persone)} capigita")


if __name__ == "__main__":
    main()
