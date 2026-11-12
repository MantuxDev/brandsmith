# Brandsmith

[English](README.md) · **Italiano**

**Un partner di studio per brand designer professionisti.** Brandsmith è una skill open source per Claude,
accompagnata da Logo Lab, un test di resistenza per loghi gratuito che funziona nel browser, in Figma e in
Illustrator. Ti toglie le parti ripetitive e verificabili del lavoro sull'identità (test del logo, accessibilità,
esportazioni, token, linee guida, revisioni critiche) e, solo quando glielo chiedi, ti aiuta su strategia,
concept e testi.

> **Supporta il lavoro del designer. Non lo sostituisce.**
> Brandsmith è pensata per chi questo lavoro lo fa già: brand designer, studi di identità, art director.
> Non progetta al posto tuo e non decide al posto tuo. Misura, controlla, documenta e propone;
> le idee, il disegno, il giudizio e il rapporto con il cliente restano tuoi.
> Non è uno strumento per ottenere un brand senza un designer.

## Quattro modi di usarla

| | Cosa ottieni | Cosa ti serve |
|---|---|---|
| **Logo Lab nel browser** | Il test completo del logo, una dimensione minima e i report PDF | Niente: apri `docs/index.html` e trascina il logo. Nessuna installazione, nessun account, nessuna IA, nulla viene caricato online |
| **Logo Lab per Figma** | Lo stesso Lab sul livello selezionato | Figma desktop: *Plugins → Development → Import plugin from manifest* → `figma-plugin/manifest.json` |
| **Logo Lab per Illustrator** | Lo stesso Lab sulla selezione, aperto nel browser | Illustrator: *File → Script → Altro script…* → `illustrator/LogoLab.jsx` |
| **Skill Brandsmith per Claude** | Revisioni critiche, memoria di progetto, strategia, testi, linee guida, più il Lab | Un piano Claude con skill ed esecuzione di codice (vedi *Installazione*) |

## Logo Lab (senza IA, nulla caricato online)

Trascina un SVG o un PNG nella pagina, incollalo da Figma o Illustrator (Ctrl+V) oppure seleziona un livello in
Figma. Tutto gira sul tuo computer e richiede pochi secondi.

- **Prima il verdetto:** un punteggio su 10 e la **dimensione minima** a cui il marchio regge, con il motivo
  spiegato a parole, e un breve elenco "Da controllare" che porta a ogni test che richiede attenzione.
- **Le misure dietro il punteggio:** tratto più sottile, spazio più stretto, fedeltà a 16 e 32 px, parti che si
  fondono o si spezzano, riempimento, simmetria, spazio negativo. I marchi bicolore vengono misurati sia sulla
  sagoma sia sulle forme interne.
- **Più di 20 test in cinque sezioni.** *Dimensione e leggibilità:* scala da 128 a 16 px, pixel reali, sfocatura.
  *Forma:* spazio negativo, peso visivo, area di rispetto, griglia icona app, curvatura e punti di ancoraggio (SVG).
  *Nel contesto:* favicon nelle schede del browser, lockup tipografici, biglietto da visita e badge, fotografia,
  cartellone, pattern, filigrana. *Riproduzione:* monocolore e negativo, materiali, rilievo e incisione, retino,
  ricamo. *File ed esportazione:* controllo del sorgente SVG e kit PNG (16–1024 px, apple-touch-icon, 192, 512).
- **Ogni test segnalato dice cosa succede e come si risolve.** Le sezioni in cui tutto è a posto restano chiuse.
- **Due report PDF**, dal pannello *Esporta report*:
  - *Per me / lo studio* (4 pagine A4): verdetto e metriche, dimensione e leggibilità, forma e contesto,
    riproduzione, e i prossimi passi ricavati dagli avvisi. Vedi `docs/sample-report.pdf`.
  - *Per il cliente* (2 pagine): niente punteggio e niente gergo tecnico. Il marchio, quale versione usare da
    quale dimensione, dove vivrà, cosa evitare, e la nota del tuo studio.
- Italiano e inglese, tema chiaro e scuro, funziona anche da telefono.

Il punteggio è una misura, non una questione di gusto. Il tratto più sottile e lo spazio più stretto vengono
misurati (entro ±0,5 px su marchi sintetici) e convertiti nella dimensione più piccola a cui entrambi restano
almeno di 1 px. È stato calibrato su qualche centinaio di marchi reali
(`skills/brandsmith/references/logo-lab-calibration.md`). Segnala i rischi di riproduzione.
**Non giudica l'idea, e un punteggio alto non fa di un logo un buon logo.** Quel giudizio spetta a te.

## La skill: tre modalità

| Modalità | Quando | Cosa fa |
|---|---|---|
| **Valuta** | Lavoro tuo, di un collega, di un cliente, di un concorrente | Revisione critica su criteri espliciti (logo, sistema di identità, testi, coerenza, strategia): problemi principali in ordine di priorità, correzioni concrete, cosa tenere. Ogni punto rimanda a qualcosa che puoi verificare. Versione per il cliente su richiesta |
| **Continua** | Riprendere un lavoro in corso | Legge i tuoi file, le linee guida, il sito o la presentazione, ricostruisce la memoria di progetto, elenca cosa manca e riparte dalla fase giusta |
| **Crea** | Quando vuoi qualcuno con cui confrontarti | Brief → ricerca → strategia → naming → direzioni → logo → identità → testi → applicazioni → linee guida → consegna, fermandosi a ogni passaggio per la tua decisione |

**Modalità solo controlli:** scrivi "controlla soltanto, non generare" e non proporrà mai concept, nomi o testi.
I concept che abbozza sono punti di partenza da ridisegnare, e lo dice.

Ogni progetto ha una cartella `.brand/` (`status.md`, `brand.md`, `identity.json`, `decisions.md`,
`feedback.md`): il lavoro riprende da una sessione all'altra e si può passare a un collega. Le tue decisioni
vengono registrate e rispettate.

## Strumenti inclusi

Script Python 3 senza dipendenze. Girano in locale e non usano IA.

| Script | Cosa fa |
|---|---|
| `logo_lab.py` | Crea la pagina Logo Lab per un logo, un nome di brand e un colore |
| `lab_metrics.py` | Legge punteggio e dimensione minima del Lab da riga di comando (Firefox headless) |
| `svg_audit.py` | Controllo tecnico dei master SVG: testo non vettorializzato, immagini incorporate, effetti, colori, tratti, angoli quasi retti, dettagli persi a 16/32 px, centratura, forature dipinte invece che ritagliate, residui dell'editor |
| `preview_sheet.py` | Foglio di prova statico e **test dello scaffale** accanto ai marchi dei concorrenti |
| `color_tools.py` | HEX/RGB/HSL/OKLCH/CMYK (approssimato), matrice di contrasto WCAG, simulazione del daltonismo, scale OKLCH, campioni |
| `tokens.py` | Design token da `identity.json`: JSON W3C DTCG, variabili CSS, SCSS, Tailwind |
| `export_variants.py` | Kit SVG da un master: a colori, monocolore, negativo, set favicon |
| `brand_init.py` | Crea la memoria `.brand/` e le cartelle del progetto |

## Installazione

**App Claude (senza terminale).** Scarica `brandsmith-skill.zip` da *Releases*. In Claude apri le impostazioni
delle skill (*Settings → Capabilities*, oppure *Customize → Skills* nelle versioni più recenti; i nomi dei menu
cambiano con la lingua dell'app), scegli **Upload skill** e seleziona lo ZIP. Attiva la skill e verifica che l'esecuzione di codice sia abilitata. Le skill
personalizzate richiedono un piano che le supporti: controlla il centro assistenza di Anthropic per la
disponibilità attuale.

**Claude Code.**
```bash
npx skills add <github-user>/brandsmith
```
oppure copia `skills/brandsmith/` in `~/.claude/skills/`.

**Uno studio intero.** Metti la skill nel repository condiviso del progetto, in `.claude/skills/brandsmith/`.
Sui piani Team ed Enterprise una skill caricata da una persona resta privata finché non viene condivisa con
l'organizzazione.

## Uso

Parlale come faresti con un collega. Risponde nella tua lingua.

- "Controlla questo logo prima della presentazione di domani. Solo i controlli." *(in Figma: tasto destro → Copy as SVG, poi incolla)*
- "Revisione del secondo giro. È per una torrefazione specialty; la favicon conta molto."
- "Ecco il sito attuale del cliente e il vecchio PDF delle linee guida: ricostruisci il brand e dimmi cosa manca."
- "Riprendi il progetto Lumen da dove eravamo rimasti."
- "Controlla l'accessibilità della palette e prepara i token per gli sviluppatori."

## Domande frequenti

**Sostituirà i designer?** No. È fatta per i designer e lascia a te ogni decisione: lei misura e documenta, tu
progetti e decidi. Usala come un assistente scrupoloso o un secondo paio d'occhi, non come sostituto del lavoro
professionale.

**Quale piano Claude mi serve?** Logo Lab e gli script non richiedono niente: nessun account, nessuna IA. La skill
gira dentro Claude (le app Claude sui piani con skill personalizzate, oppure Claude Code). Brandsmith è gratuita;
l'uso di Claude viene conteggiato dal tuo piano come sempre.

**Il lavoro per il cliente è sotto NDA.** Logo Lab e tutti gli script girano sul tuo computer e non inviano nulla.
Quello che incolli in una conversazione con Claude viene trattato da Anthropic secondo i termini del tuo piano:
verificali, usa un piano business se i tuoi contratti lo richiedono e rendi anonimi i brief. La skill te lo
ricorda quando parli di riservatezza.

**Le revisioni sono generiche?** Ha istruzioni per non esserlo: ogni osservazione deve indicare un elemento, una
dimensione o un valore che puoi verificare. Se non è abbastanza specifica, apri una issue con l'esempio: è la
segnalazione più utile che ci sia.

**Chi la mantiene?** Vedi `CHANGELOG.md` e `ROADMAP.md`. Issue e pull request sono benvenute, soprattutto da
designer che lavorano sul campo.

## Cosa non fa

- Sostituire il lavoro del designer, il suo gusto o la sua responsabilità verso il cliente.
- Sostituire ricerche di anteriorità del marchio, consulenza legale, verifiche sulle licenze dei font, prove di
  stampa o ricerca con gli utenti. Ti dice quando servono.
- Copiare o imitare da vicino loghi esistenti o il lavoro di altri studi.
- Produrre file di stampa definitivi (PDF CMYK/Pantone). Quelli escono dal tuo programma vettoriale.

## Struttura del repository

```
skills/brandsmith/
├── SKILL.md            punto di ingresso: ruolo, modalità, instradamento, convenzioni di lavoro
├── references/         un file per modalità e per modulo, caricato solo quando serve
├── templates/          modelli della memoria .brand/ + logo-lab.html (sorgente di Logo Lab)
└── scripts/            strumenti Python, senza dipendenze
docs/                   pagina Logo Lab (generata), report di esempio, marchio
figma-plugin/           Logo Lab per Figma (generato) + kit per Figma Community
illustrator/            Logo Lab per Illustrator (generato)
tools/                  script di build, calibrazione, test dell'interfaccia
evals/                  prompt di prova per misurare e migliorare la skill
examples/               un progetto fittizio a metà strada, per provare la modalità Continua
PUBLISHING.md           come pubblicare il progetto
TESTING.md              come provare la skill su progetti reali
```

## Licenza

MIT. Vedi `LICENSE`.
