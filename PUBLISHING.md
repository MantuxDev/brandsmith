# Publishing Brandsmith · Pubblicare Brandsmith

[English](#english) · [Italiano](#italiano)

---

## English

How to publish the project. Every public text (README, release notes, Figma listing) must say clearly that
Brandsmith **supports designers and does not replace them**: it is for professionals who already do brand and
identity work, and it keeps every decision with them.

### 1. Before publishing

- [x] `LICENSE` author filled in.
- [x] Repository: https://github.com/MantuxDev/brandsmith
- [ ] Rebuild everything from the sources (never edit generated files by hand):
  ```bash
  python3 tools/build_release.py           # dist/brandsmith-skill.zip + docs/index.html
  python3 tools/build_figma_plugin.py      # figma-plugin/
  python3 tools/build_illustrator_script.py
  python3 tools/test_lab_ui.py --sample    # smoke test + docs/sample-report.pdf
  ```
- [ ] `tools/test_lab_ui.py` ends with "all checks passed".
- [ ] Upload `dist/brandsmith-skill.zip` to the Claude app once yourself (Skills settings → Upload skill) and run
      one real request ("check this logo, just the checks"). Note the exact menu path you saw and correct the
      *Install* section of both READMEs if it differs.
- [ ] `test-projects/` and `design-handoff/` are not committed (`git status` shows nothing from them).
- [ ] `CHANGELOG.md` has the version you are about to publish.

### 2. GitHub repository and release

1. Create a public repository named `brandsmith` and push `master` (merge any work branch first).
2. Add a description: *Studio partner for professional brand designers: logo stress test, critique, guidelines.
   Supports designers, doesn't replace them.* Topics: `branding`, `logo`, `brand-identity`, `design`,
   `claude`, `agent-skills`, `figma-plugin`.
3. Create a release tagged with the CHANGELOG version (e.g. `v0.4.0`). Attach `dist/brandsmith-skill.zip`.
   Release notes: copy the CHANGELOG entry and add one line in both languages:
   *Brandsmith supports the designer's work; it does not replace it. · Brandsmith supporta il lavoro del
   designer; non lo sostituisce.*

### 3. Logo Lab on the web (GitHub Pages)

`docs/index.html` is a single page that makes no network requests. In the repository settings → *Pages*, publish
from the `master` branch, folder `/docs`. The Lab will be at `https://mantuxdev.github.io/brandsmith/`.
Link it at the top of both READMEs once it is live.

### 4. Figma Community

Listing texts in English and Italian, cover and icon: `figma-plugin/community/PUBLISHING.md`.
Before submitting, test the plugin inside Figma desktop (see `HANDOFF.md`, item 1): frames, groups, components,
text layers, PDF and PNG downloads. Publishing needs the author's Figma account; Figma reviews it before it goes
live.

### 5. Illustrator

No store needed: `illustrator/LogoLab.jsx` is attached to the GitHub release and linked from the README.

### 6. After publishing

- Ask a few working designers to try it on a real project and open issues (see `TESTING.md`).
- Keep the "supports, doesn't replace" message in every post or announcement. Don't present simulated panel
  results as real testimonials.

---

## Italiano

Come pubblicare il progetto. Ogni testo pubblico (README, note di rilascio, scheda Figma) deve dire chiaramente
che Brandsmith **supporta il lavoro dei designer e non lo sostituisce**: è pensata per professionisti che
lavorano già su brand e identità, e lascia a loro ogni decisione.

### 1. Prima di pubblicare

- [x] Autore inserito in `LICENSE`.
- [x] Repository: https://github.com/MantuxDev/brandsmith
- [ ] Rigenera tutto dai sorgenti (non modificare mai a mano i file generati):
  ```bash
  python3 tools/build_release.py           # dist/brandsmith-skill.zip + docs/index.html
  python3 tools/build_figma_plugin.py      # figma-plugin/
  python3 tools/build_illustrator_script.py
  python3 tools/test_lab_ui.py --sample    # test dell'interfaccia + docs/sample-report.pdf
  ```
- [ ] `tools/test_lab_ui.py` termina con "all checks passed".
- [ ] Carica tu stesso `dist/brandsmith-skill.zip` nell'app Claude (impostazioni delle skill → Upload skill) e
      prova una richiesta reale ("controlla questo logo, solo i controlli"). Annota il percorso esatto dei menu
      che hai visto e correggi la sezione *Installazione* dei due README se è diverso.
- [ ] `test-projects/` e `design-handoff/` non sono nei commit (`git status` non mostra nulla di loro).
- [ ] `CHANGELOG.md` contiene la versione che stai per pubblicare.

### 2. Repository GitHub e release

1. Crea un repository pubblico chiamato `brandsmith` e fai il push di `master` (prima unisci gli eventuali branch
   di lavoro).
2. Aggiungi una descrizione: *Studio partner for professional brand designers: logo stress test, critique,
   guidelines. Supports designers, doesn't replace them.* Topic: `branding`, `logo`, `brand-identity`, `design`,
   `claude`, `agent-skills`, `figma-plugin`.
3. Crea una release con il tag della versione del CHANGELOG (per esempio `v0.4.0`) e allega
   `dist/brandsmith-skill.zip`. Note di rilascio: copia la voce del CHANGELOG e aggiungi una riga in entrambe le
   lingue: *Brandsmith supports the designer's work; it does not replace it. · Brandsmith supporta il lavoro
   del designer; non lo sostituisce.*

### 3. Logo Lab sul web (GitHub Pages)

`docs/index.html` è una pagina unica che non fa richieste di rete. Nelle impostazioni del repository → *Pages*,
pubblica dal branch `master`, cartella `/docs`. Il Lab sarà su `https://mantuxdev.github.io/brandsmith/`.
Quando è online, metti il link in cima a entrambi i README.

### 4. Figma Community

Testi della scheda in inglese e in italiano, copertina e icona: `figma-plugin/community/PUBLISHING.md`.
Prima di inviarlo, prova il plugin dentro Figma desktop (vedi `HANDOFF.md`, punto 1): frame, gruppi, componenti,
livelli di testo, download di PDF e PNG. Per pubblicare serve l'account Figma dell'autore; Figma lo revisiona
prima che sia visibile.

### 5. Illustrator

Non serve uno store: `illustrator/LogoLab.jsx` va allegato alla release GitHub e linkato dal README.

### 6. Dopo la pubblicazione

- Chiedi ad alcuni designer professionisti di provarla su un progetto reale e di aprire issue (vedi `TESTING.md`).
- Mantieni il messaggio "supporta, non sostituisce" in ogni post o annuncio. Non presentare i risultati del panel
  simulato come testimonianze reali.
