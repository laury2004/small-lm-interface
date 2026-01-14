# 🎵 LyricGen AI - Professional Lyric Studio

**LyricGen AI** è un'applicazione web basata su intelligenza artificiale per la generazione di testi musicali in stile italiano. Utilizza un modello di linguaggio basato su n-grammi (Bigram Model V2) con smoothing di Laplace per creare testi coerenti partendo da un artista specifico e un prompt testuale.

## ✨ Caratteristiche Principali

- **Generazione Intelligente**: Scegli tra diversi artisti del dataset e regola i parametri di generazione.
- **Effetto Typewriter**: Visualizzazione dinamica del testo generato per simulare il processo creativo dell'AI.
- **Dark Mode Totale**: Interfaccia ottimizzata per il comfort visivo, con un design "Total Dark" persistente.
- **Accessibilità**: 
  - Sintesi vocale (TTS) integrata per ascoltare i versi generati.
  - Funzione di copia rapida negli appunti.
  - Download del testo in formato `.txt`.
- **UI Moderna**: Sviluppata con Vuetify 3 e Vue.js 3, seguendo i principi del Material Design.

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.x)
- **Frontend**: Vue.js 3, Vuetify 3
- **Modello**: Bigram Language Model con Laplace Smoothing
- **Server**: Uvicorn

## 🚀 Installazione e Utilizzo

### 1. Prerequisiti
Assicurati di avere Python installato sul tuo sistema.

### 2. Installazione delle dipendenze
Apri il terminale nella cartella del progetto e installa le librerie necessarie:
```bash
pip install -r requirements.txt

Poi per far avviare il tutto scrivere nel terminale :

python app.py

se lo si vuole ricaricare (se si ferma) :
CTRL + "C"
