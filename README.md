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
| `sjablonen/` | De vaste layouts voor feed en story (nog te maken). |

## Lokaal bekijken

De pagina laadt `regels.md` met `fetch`, dus dubbelklikken op `index.html` werkt niet. Open hem via een lokale server:

- IntelliJ: rechtsklik op `index.html`, dan "Open in Browser".
- VS Code: installeer de extensie Live Server, rechtsklik op `index.html`, dan "Open with Live Server".
- Of in een terminal: `python3 -m http.server` en ga naar http://localhost:8000

## Online zetten met GitHub Pages

1. Maak op GitHub een nieuwe publieke repository, bijvoorbeeld `huisstijl`.
2. In deze map:
   ```
   git init
   git add .
   git commit -m "Eerste versie"
   git branch -M main
   git remote add origin https://github.com/<gebruiker>/huisstijl.git
   git push -u origin main
   ```
3. Op GitHub: Settings, Pages, kies bij "Branch" `main` en map `/ (root)`, en bewaar.
4. Na een minuut staat de pagina op `https://<gebruiker>.github.io/huisstijl/`.
   De regels voor AI staan dan op `https://<gebruiker>.github.io/huisstijl/regels.md`.

De startzin op de pagina gebruikt automatisch het juiste adres.

## Een regel aanpassen

1. Wijzig `regels.md`.
2. Verhoog het versienummer in de titel.
3. Commit en push. De pagina en elke AI die de link leest volgen meteen.

## Nog te doen

- `Huize-Briers-logo-volledig-wit.svg` en de PNG-versies toevoegen (zaten niet in de export van de gids).
- Sjablonen voor feed (1080 × 1350) en story (1080 × 1920).
- Een voorbeeld van een post die volledig klopt.
