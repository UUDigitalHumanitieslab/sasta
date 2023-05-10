# Anonimisatie
De transcripten kunnen gevoelige informatie over participanten bevatten. SASTA staat toe dat anonimisatiecodes gebruikt worden. In de bewerkingstappen die SASTA uitvoert worden deze omgezet in grammaticaal gelijke. De anonimisaties volgen een vast patroon:
```
<optioneel: prefix>CODE<optioneel: affix><optioneel: nummer 1-4>
```
Dezelfde combinatie van CODE + nummering zal steeds hetzelfde woord vervangen worden. Zo blijft een transcript ook voor de menselijke gebruiker duidelijk volgbaar. Voorbeelden:

```
Ik heet NAAM1. -> Ik heet Jan.
Ik heet VOORNAAM1. -> Ik heet Jan.
Ik heet NAAMKIND. -> Ik heet Maria.
```
Merk op dat NAAM1 en VOORNAAM1 dezelfde vervanging toegewezen krijgen. Dit komt omdat de combinatie code (NAAM) en nummering (1) gelijk is. SASTA houdt intern bij waar vervangingen uitgevoerd zijn. Deze zijn terug te vinden in de CHAT-bestanden op de %xano tier. Voorbeeld:
```
*PMA:	uh buiten Breda
%xano:	10|PLAATS1|Breda
```
Op de tiende positie in de zin stond PLAATS1, en dit is vervangen door Breda.

## Beschikbare anonimisatiecodes
- categorie: plaatsnaam
    - codes: `PLAATS`, `PLAATSNAAM`
    - vervangingen: `Utrecht`, `Breda`, `Leiden`, `Maastricht`, `Arnhem`
    - voorbeeld: `Ik woon in PLAATS2` -> `Ik woon in Leiden`
- categorie: voornaam
    - codes: `NAAM`, `BROER`, `ZUS`, `KIND`
    - vervangingen: `Maria`, `Jan`, `Anna`, `Esther`, `Pieter`, `Sam`
    - voorbeeld: `Dat zei BROER1` -> `Dat zei Jan`
    - voorbeeld: `Dat zei mijn TWEELINGZUS1` ->  `Dat zei Jan`
- categorie: achternaam
    - codes: `ACHTERNAAM`
    - vervangingen: `Jansen`, `Hendriks`, `Dekker`, `Dijkstra`, `Veenstra`
    - voorbeeld: `Dat zei NAAM ACHTERNAAM` -> `Dat zei Maria Jansen`
