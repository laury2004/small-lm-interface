from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response, FileResponse 
from contextlib import asynccontextmanager
from model import lyric_model
import uvicorn
import os

# --- GESTIONE CICLO DI VITA (LIFESPAN) ---
# Questa funzione viene eseguita all'avvio del server.
# È fondamentale perché scarica i dati e "addestra" il modello prima che l'utente possa usarlo.
@asynccontextmanager
async def lifespan(app: FastAPI):
    lyric_model.download_and_train()
    yield

# Inizializzazione di FastAPI con il lifespan definito sopra
app = FastAPI(lifespan=lifespan)

# --- CONFIGURAZIONE FILE STATICI E TEMPLATE ---
# Collega la cartella 'static' (CSS, immagini) all'URL /static
app.mount("/static", StaticFiles(directory="static"), name="static")
# Configura Jinja2 per cercare i file HTML nella cartella 'templates'
templates = Jinja2Templates(directory="templates")

# --- FIX FAVICON ---
# Gestisce la richiesta automatica del browser per l'iconcina della scheda.
# Restituisce '204 No Content' per evitare errori 404 nei log del terminale.
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204) 

# --- ROTTA PRINCIPALE (HOME) ---
# Carica la pagina iniziale (index.html) e passa la lista degli artisti disponibili dal modello.
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "artists": lyric_model.available_artists
    })

# --- LOGICA DI GENERAZIONE AI ---
# Riceve i dati JSON dal frontend (artista, incipit, lunghezza, creatività).
@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    
    # Estrazione dei parametri inviati dall'interfaccia Vue.js
    artist = data.get("artist")
    prompt = data.get("prompt", "")
    length = int(data.get("length", 40))
    creativity = float(data.get("creativity", 0.5)) 
    
    # Chiama la funzione di generazione nel file model.py e restituisce il risultato al frontend
    output = lyric_model.generate(artist, prompt, length, creativity)
    return {"output": output}

# --- AVVIO DEL SERVER ---
# Configura l'indirizzo IP e la porta (5000) su cui l'app sarà raggiungibile.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)