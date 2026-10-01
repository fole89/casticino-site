"""Copertine di annuari e Informazione: prima pagina del PDF -> assets/img/pubblicazioni/<nome>.webp

Crea solo le copertine che mancano (passa --tutte per rifarle tutte) e cancella quelle dei PDF tolti.
Servono PyMuPDF e Pillow, solo per questo script:  pip install pymupdf pillow
Uso: python scripts/copertine.py
"""
import glob, io, os, sys
import pymupdf
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "pubblicazioni")
LARGHEZZA = 800


def main(tutte=False):
    os.makedirs(OUT, exist_ok=True)
    pdf = sorted(glob.glob(os.path.join(ROOT, "docs", "annuari", "*.pdf")) +
                 glob.glob(os.path.join(ROOT, "docs", "informazione", "*.pdf")))
    nomi = set()
    for f in pdf:
        nome = os.path.splitext(os.path.basename(f))[0]
        nomi.add(nome)
        dest = os.path.join(OUT, nome + ".webp")
        if os.path.exists(dest) and not tutte:
            continue
        pagina = pymupdf.open(f)[0]
        z = LARGHEZZA / pagina.rect.width
        pix = pagina.get_pixmap(matrix=pymupdf.Matrix(z, z))
        Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB").save(dest, "WEBP", quality=80, method=6)
        print("copertina", os.path.relpath(dest, ROOT))
    for vecchia in glob.glob(os.path.join(OUT, "*.webp")):
        if os.path.splitext(os.path.basename(vecchia))[0] not in nomi:
            os.remove(vecchia)
            print("tolta", os.path.relpath(vecchia, ROOT))


if __name__ == "__main__":
    main("--tutte" in sys.argv)
