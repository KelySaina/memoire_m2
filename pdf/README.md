# Mémoire M2 – version PDF

`memoire.pdf` est généré à partir du texte de `build/content/*.md` (une partie par fichier).

## Régénérer

```sh
cd build
python3 build.py            # écrit ../memoire.pdf
```

Prérequis : Python 3 avec `reportlab` et `Pillow`, polices Liberation Serif et DejaVu (`fonts-liberation`, `fonts-dejavu`).

## Organisation

- `build/content/` – texte du mémoire (pages liminaires, parties I à III, conclusion et annexes)
- `build/code/` – listings repris du dépôt `microservices-project`
- `build/build.py` – mise en page (page de garde, numérotation romaine/arabe, sommaire, listes des figures et tableaux)
- `fig_etude/`, `fig_bokyy/`, `fig_m2/` – figures extraites des PDF sources (`build/flatten.py`)
- `images/` – photo du CV

Les directives de mise en forme (`@chapter`, `@img`, `@code`, `@tabcap`…) sont décrites en tête de `build.py`.
