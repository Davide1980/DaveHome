# Scraper Immobiliare - Monselice

Sistema automatico di scraping per la ricerca di immobili su vari portali immobiliari italiani.

## Caratteristiche

- Ricerca su **4 portali principali**:
  - Immobiliare.it
  - Casa.it
  - Idealista.it
  - Subito.it

- Filtraggio automatico in base ai criteri specificati
- Esportazione risultati in formato CSV
- Report dettagliato con statistiche

## Criteri di Ricerca Attuali

- **Località**: Monselice (PD)
- **Prezzo**: €100.000 - €180.000
- **Tipo**: Casa indipendente
- **Superficie**: 120-220 m²
- **Camere**: 3
- **Caratteristiche**: garage, giardino, balcone, studio
- **Stato**: nuovo, ristrutturato, o da ristrutturare

## Installazione

1. **Clona il repository** (se non l'hai già fatto)

2. **Installa Python 3.8+** se non è già installato

3. **Installa le dipendenze**:
```bash
pip install -r requirements.txt
```

## Configurazione

Modifica il file `config.json` per personalizzare i criteri di ricerca:

```json
{
  "search_criteria": {
    "location": "Monselice",
    "province": "Padova",
    "price_min": 100000,
    "price_max": 180000,
    "property_type": "casa indipendente",
    "area_min": 120,
    "area_max": 220,
    "rooms": 3,
    "features": ["garage", "giardino", "balcone", "studio"],
    "condition": ["nuovo", "ristrutturato", "da ristrutturare"]
  }
}
```

## Utilizzo

Esegui lo script principale:

```bash
python main.py
```

Il programma:
1. Legge i criteri da `config.json`
2. Esegue lo scraping su tutti i portali
3. Filtra i risultati in base ai criteri
4. Salva i risultati in formato CSV e Excel
5. Mostra un riepilogo con statistiche e top 5 match

## Output

Lo scraper genera **2 file** per ogni esecuzione:

### 📄 File CSV: `risultati_monselice_YYYYMMDD_HHMMSS.csv`
File semplice con tutti i dati in formato testo.

### 📊 File Excel: `risultati_monselice_YYYYMMDD_HHMMSS.xlsx` (CONSIGLIATO)
File Excel formattato con:
- ✅ **Intestazioni colorate** (blu scuro con testo bianco)
- ✅ **Colori automatici per i prezzi**:
  - 🟢 Verde = Prezzi bassi (primo 33% del range)
  - 🟡 Giallo = Prezzi medi (33-66% del range)
  - 🔴 Rosso = Prezzi alti (ultimo 33% del range)
- ✅ **Link cliccabili** per aprire gli annunci direttamente
- ✅ **Colonne auto-dimensionate** per leggibilità ottimale
- ✅ **Filtri automatici** su tutte le colonne
- ✅ **Intestazione bloccata** (rimane visibile quando scorri)
- ✅ **Formattazione valuta** (€ con separatori delle migliaia)
- ✅ **Bordi e allineamento** per una lettura facile

### Colonne contenute:
- **Fonte**: Portale da cui proviene l'annuncio
- **Titolo**: Titolo dell'annuncio
- **Prezzo (€)**: Prezzo (con colori verde/giallo/rosso)
- **Superficie (m²)**: Metri quadri
- **Camere**: Numero di camere
- **Località**: Zona/Città
- **Caratteristiche**: garage, giardino, balcone, ecc.
- **Link**: URL cliccabile per vedere l'annuncio
- **Descrizione**: Testo completo dell'annuncio

## Struttura del Progetto

```
.
├── config.json              # Configurazione criteri di ricerca
├── main.py                  # Script principale
├── requirements.txt         # Dipendenze Python
├── scrapers/
│   ├── __init__.py
│   ├── base.py             # Classe base per gli scraper
│   ├── immobiliare.py      # Scraper per Immobiliare.it
│   ├── casait.py           # Scraper per Casa.it
│   ├── idealista.py        # Scraper per Idealista.it
│   └── subito.py           # Scraper per Subito.it
└── README.md
```

## Note Importanti

1. **Rate Limiting**: Gli scraper includono delay casuali (1-3 secondi) tra le richieste per essere rispettosi verso i siti web

2. **Aggiornamenti dei Siti**: I siti web possono cambiare la loro struttura HTML. Se uno scraper smette di funzionare, potrebbe essere necessario aggiornare i selettori CSS

3. **Uso Responsabile**: Questo tool è per uso personale. Non fare richieste eccessive che potrebbero sovraccaricare i server

4. **Legalità**: Verifica i termini di servizio dei siti web prima dell'uso. Il web scraping potrebbe violare i ToS di alcuni siti

## Troubleshooting

### Nessun risultato trovato
- Verifica che i criteri non siano troppo restrittivi
- Controlla che la località sia scritta correttamente
- Alcuni siti potrebbero bloccare richieste automatiche

### Errori di connessione
- Controlla la connessione internet
- Alcuni siti potrebbero richiedere più tempo per rispondere
- Riprova dopo qualche minuto

### Errori di parsing
- I siti potrebbero aver cambiato la loro struttura HTML
- Controlla gli aggiornamenti del repository

## Possibili Estensioni

- Aggiungere più portali (Tecnocasa, Wikicasa, etc.)
- Notifiche via email per nuovi annunci
- Interfaccia web con Flask/Django
- Database per tracciare la cronologia degli annunci
- Filtri avanzati (distanza da punti di interesse, ecc.)

## Licenza

Questo progetto è fornito "as-is" per uso personale.
