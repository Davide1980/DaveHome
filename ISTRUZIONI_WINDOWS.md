# Guida per Windows - Scraper Immobiliare Monselice

## Requisiti (da installare PRIMA di iniziare)

### 1. Python
- Scarica da: https://www.python.org/downloads/
- **IMPORTANTE**: Durante l'installazione spunta "Add Python to PATH"
- Verifica l'installazione aprendo il Prompt dei comandi e digitando: `python --version`

### 2. Git
- Scarica da: https://git-scm.com/download/win
- Installa con le opzioni predefinite
- Verifica l'installazione aprendo il Prompt dei comandi e digitando: `git --version`

### 3. Google Chrome
- Se non ce l'hai: https://www.google.com/chrome/
- ✅ Hai già Chrome installato!

---

## Installazione del Progetto

### Passo 1: Apri il Prompt dei comandi
- Premi `Win + R`
- Digita `cmd` e premi Invio

### Passo 2: Vai nella cartella dove vuoi salvare il progetto
```cmd
cd Desktop
```
(o qualsiasi altra cartella preferisci)

### Passo 3: Clona il repository
```cmd
git clone https://github.com/Davide1980/DaveHome.git
cd DaveHome
git checkout claude/scrape-casa-listings-011CULa8JJsA8mfPVDnZQXb9
```

### Passo 4: PRIMA ESECUZIONE - Setup automatico
Fai doppio click su: **`setup_and_run.bat`**

Questo script:
- Crea un ambiente virtuale Python
- Installa tutte le dipendenze necessarie
- Avvia lo scraper

⏱️ La prima volta potrebbe richiedere 2-3 minuti per scaricare tutto.

---

## Uso Quotidiano

### Per eseguire lo scraper dopo il primo setup:
Fai doppio click su: **`run.bat`**

Questo avvierà lo scraper che:
1. Cerca case a Monselice su 4 portali principali
2. Filtra in base ai tuoi criteri (vedi config.json)
3. Salva i risultati in un file CSV con timestamp

---

## Personalizzare la Ricerca

Apri il file **`config.json`** con Notepad e modifica i criteri:

```json
{
  "search_criteria": {
    "location": "Monselice",
    "price_min": 100000,
    "price_max": 180000,
    "area_min": 120,
    "area_max": 220,
    "rooms": 3
  }
}
```

Salva il file e riesegui `run.bat`.

---

## File Generati

I risultati vengono salvati in:
- **`risultati_monselice_YYYYMMDD_HHMMSS.csv`**

Puoi aprirlo con Excel o LibreOffice Calc.

---

## Risoluzione Problemi

### "Python non è riconosciuto come comando interno..."
- Reinstalla Python e assicurati di spuntare "Add Python to PATH"
- Riavvia il computer dopo l'installazione

### "Git non è riconosciuto come comando interno..."
- Installa Git da: https://git-scm.com/download/win
- Riavvia il Prompt dei comandi

### "ChromeDriver error..."
- Assicurati che Chrome sia aggiornato all'ultima versione
- Il driver viene scaricato automaticamente alla prima esecuzione

### Lo scraper non trova risultati
- Verifica i criteri in config.json (potrebbero essere troppo restrittivi)
- I siti web potrebbero aver cambiato la struttura HTML
- Alcuni siti potrebbero bloccare le richieste automatiche

### Lo scraper è molto lento
- È normale! Usa delay casuali (2-5 secondi) per sembrare umano
- Cerca su 4 siti diversi, può richiedere alcuni minuti

---

## Note Importanti

⚠️ **Uso Responsabile**: Questo tool è per uso personale. Non eseguirlo troppo frequentemente (max 2-3 volte al giorno) per non sovraccaricare i server.

📝 **Legalità**: Verifica i termini di servizio dei siti web prima dell'uso. Il web scraping potrebbe violare i ToS di alcuni siti.

🔄 **Aggiornamenti**: I siti web possono cambiare la loro struttura. Se uno scraper smette di funzionare, potrebbe essere necessario aggiornare il codice.

---

## Supporto

Per problemi o domande, apri un issue su GitHub.
