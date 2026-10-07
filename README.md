# Huize Briers: huisstijl en regels voor sociale media

Eén bron voor iedereen die een post maakt, en voor elke AI die daarbij helpt.

## Wat staat waar

| Pad | Wat |
|---|---|
| `regels.md` | De regels die de AI leest. Dit is de bron: pas alleen dit bestand aan. |
| `index.html` | De pagina voor medewerkers. Laadt `regels.md` automatisch in. |
| `huisstijlgids.html` | De volledige huisstijlgids uit Claude Design, voor mensen. |
| `huisstijl.md` | Dezelfde gids als tekst, voor AI. Pas je de gids aan, werk dan ook dit bestand bij. |
| `logo/` | De officiële logobestanden uit de huisstijlgids. |
| `voorbeelden/` | Echte posts, goed en fout, met uitleg. |
| `logo/png/` | Dezelfde logo's als PNG met transparante achtergrond. |
| `downloads/` | Kleuren (CSS en JSON) en `Huize-Briers-huisstijl.zip` met alles. Maak de zip opnieuw met `python3 tools/maak-zip.py` na elke wijziging aan logo's, kleuren of regels. |
| `sjablonen/` | De vaste layouts voor feed en story (nog te maken). |

## Lokaal bekijken

De pagina laadt `regels.md` met `fetch`, dus dubbelklikken op `index.html` werkt niet. Open hem via een lokale server:

- IntelliJ: rechtsklik op `index.html`, dan "Open in Browser".
- VS Code: installeer de extensie Live Server, rechtsklik op `index.html`, dan "Open with Live Server".
- Of in een terminal: `python3 -m http.server` en ga naar http://localhost:8000

## Online

De site staat op https://huize-briers.github.io/huisstijl/ en wordt bijgewerkt bij elke push naar `main` (GitHub Pages, branch `main`, map `/`).

- Pagina voor medewerkers: https://huize-briers.github.io/huisstijl/
- Regels voor AI: https://huize-briers.github.io/huisstijl/regels.md

De startzin op de pagina gebruikt automatisch het juiste adres.

## Een regel aanpassen

1. Wijzig `regels.md`.
2. Verhoog het versienummer in de titel.
3. Commit en push. De pagina en elke AI die de link leest volgen meteen.

## Nog te doen

- Een voorbeeld van een post die volledig klopt: maak er een met een echte foto, en voeg hem toe aan `voorbeelden/` en `index.html`.
