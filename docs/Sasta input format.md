# SASTA Input Format (SIF)

Dit document beschrijft het SASTA Input Formaat (SIF). In dit formaat kunnen transcripten aangeleverd worden voor analyse in SASTA.

## 1 - Het bestand
Het transcript dient te worden aangeleverd als een Microsoft Word  `.docx`-bestand. Een `.txt`-bestand met `utf-8`-encoding wordt ook geaccepteerd. De naam van het bestand wordt gebruikt als titel van het transcript binnen SASTA. Zo zal het bestand `sample 12.docx` het transcript `sample 12` opleveren.

## 2 - Sprekers
Het transcript kan uitingen van meerdere sprekers bevatten. Ken elke spreker een unieke drieletterige code toe; bijvoorbeeld CHI (child), INV (interviewer) of PMA (patient met afasie).


## 3 - Metadata
### 3.1 - Uitingen selecteren
SASTA werkt optimaal wanneer het volledige transcript wordt aangeleverd. Dus ook uitingen van sprekers die niet geanalyseerd hoeven te worden, kunnen de resultaten verbeteren. Het is nodig om in dit volledige transcript de uitingen te markeren waarin je geinterresseerd bent. Je kunt dit mechanisme gebruiken om de analyse te baseren op een vast aantal uitingen, bijvoorbeeld 50.

Er zijn twee manieren om een zin te markeren voor analyse:

1. De spreker van de uiting

2. De uiting nummeren (zie 3)

Om alle uitingen van spreker PMA te analyseren, voeg je de volgende regel in:

```

##TARGET SPEAKER PMA

```

Om alleen de genummerde uitingen te analyseren:

```

##TARGET UTTIDS

```

Wanneer uitingen van een spreker worden gemarkeerd, **én** er zijn gemarkeerde uitingen aanwezig, worden alleen de genummerde uitingen van de spreker geanalyseerd.

### 3.2 samplenaam
Het is mogelijk de titel van een transcript te overschrijven aan de hand van het metadata-veld `samplenaam`:
```##META text samplenaam = ASTA-13```
Als dit veld aanwezig is wordt de bestandsnaam genegeerd.

### 3.3 Overige metadata
Alle metadata volgens het [PAQU-formaat](https://paqu.let.rug.nl:8068/info.html#credits) zijn geldige invoer. deze worden echter door niet door SASTA verwerkt.

## 4 - Uitingen

Elke uiting begint op een nieuwe regel. Ze kunnen doorlopen op de volgende regel, maar mogen niet onderbroken worden met een regeleinde. Uitingen hebben een vaste vorm:

```
SPK:<tab of spatie(s)>Inhoud van de uiting.

```

Optioneel zijn ze ook genummerd:

```

INV: Waar ben je vandaag geweest?

1 | PMA: In de dierentuin.

```



### 4.2 Annoteren
Uitingen kunnen geannoteerd worden volgens de [CHAT handleiding][chat-manual].

[chat-manual]: https://talkbank.org/manuals/CHAT.pdf
Voor lijsten met veel gebruikte annotaties, zie TODO: ASTA, STAP, TARSP-specifieke annotaties.

### 4.3 Anonimiseren
De transcripten kunnen gevoelige informatie over participanten bevatten. SASTA staat toe dat anonimisatiecodes gebruikt worden. In de bewerkingstappen die SASTA uitvoert worden deze omgezet in grammaticaal gelijke. De anonimisaties volgen een vast patroon:

```
<optioneel: prefix>CODE<optioneel: affix><optioneel: nummer 1-4>
```

Dezelfde combinatie van CODE + nummering zal steeds hetzelfde woord vervangen worden. Zo blijft een transcript ook voor de menselijke gebruiker duidelijk volgbaar.
Voorbeelden:

```
Ik heet NAAM1. -> Ik heet Jan.
Ik heet VOORNAAM1. -> Ik heet Jan.
Ik heet NAAMKIND. -> Ik heet Maria.
```
Merk op dat NAAM1 en VOORNAAM1 dezelfde vervanging toegewezen krijgen. Dit komt omdat de combinatie code (`NAAM`) en nummering (`1`) gelijk is.
SASTA houdt intern bij waar vervangingen gepleegd zijn. Deze zijn terug te vinden in de CHAT-bestanden op de `%xano` tier. Voorbeeld:

```
*PMA:	uh buiten Breda
%xano:	10|PLAATS1|Breda
```
Op de tiende positie in de zin stond `PLAATS1`, en dit is vervangen door `Breda`.


### 4.4 Beschikbare anonimisatiecodes
- Categorie: plaatsnaam
    - codes: `PLAATS`, `PLAATSNAAM`
    - vervangingen: `Utrecht, Breda, Leiden, Maastricht, Arnhem`
    - voorbeeld: `Ik woon in PLAATS2 -> Ik woon in Leiden`
- Categorie: voornaam
    - codes: `NAAM`, `BROER`,`ZUS`, `KIND`
    - vervangingen: `Maria, Jan, Anna, Esther, Pieter, Sam`
    - voorbeeld: `Dat zei BROER1 -> Dat zei Jan`
    - voorbeeld: `Dat zei mijn TWEELINGZUS1 ->  Dat zei Jan`
- Categorie: achternaam
    - codes: `ACHTERNAAM`
    - vervangingen: `Jansen, Hendriks, Dekker, Dijkstra, Veenstra`
    - voorbeeld: `Dat zei NAAM ACHTERNAAM -> Dat zei Maria Jansen`

