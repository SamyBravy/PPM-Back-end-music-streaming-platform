# Progetto Backend: Music Streaming Service

**Studente:** Samuele  
**Tipo di Progetto:** Full-Stack Web Application (con predisposizione REST API)  
**Framework Utilizzato:** Django 5.x + Django REST Framework  

---

## Descrizione del Progetto

Questo progetto consiste nello sviluppo di un'applicazione web per un servizio di streaming musicale, strutturata su un'architettura **MVT Monolitica ibrida**, con la predisposizione di **REST API**. L'applicazione consente la gestione di un catalogo musicale (generi, canzoni) e la creazione di playlist personali da parte degli utenti.

Il progetto include un sistema di autenticazione, la differenziazione dei ruoli (Listener e Curator) e form personalizzati resi con Bootstrap 5, nel pieno rispetto dei requisiti del disciplinare.

---

## Funzionalità per Ruolo

Il sistema prevede un modello utente personalizzato (`CustomUser`) con ruoli predefiniti che regolano l'accesso e la gestione dei contenuti.

### Ruolo: **Listener** (Utente standard)
- Navigazione libera e consultazione del catalogo canzoni e dei generi musicali.
- Creazione e visualizzazione delle proprie playlist.
- Accesso e navigazione alle rotte protette da `LoginRequiredMixin`.
- Consumo in sola lettura delle API.

### Ruolo: **Curator** (Membro dello Staff)
- Tutte le funzionalità del Listener.
- Inserimento, modifica e cancellazione (CRUD) dei brani musicali dal catalogo (via Viste Class-Based protette e via REST API).
- Gestione tramite il pannello di amministrazione (`/admin`).
- Le operazioni distruttive o di scrittura sono protette backend dal `PermissionRequiredMixin`.

---

## Istruzioni di Installazione e Avvio (Sviluppo Locale)

Requisiti: Python 3.10+

1. **Clonare la Repository**
   ```bash
   git clone <url-repository>
   cd <cartella-progetto>
   ```

2. **Creare e attivare il Virtual Environment**
   - Su Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - Su macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Installare le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Applicare le Migrazioni**
   ```bash
   python manage.py migrate
   ```

5. **Avviare il Server di Sviluppo**
   ```bash
   python manage.py runserver
   ```
   L'applicazione sarà accessibile all'indirizzo [http://127.0.0.0:8000](http://127.0.0.1:8000).

> **Nota:** Il file `db.sqlite3` è già presente e popolato, puoi accedere con gli account demo sottostanti senza eseguire ulteriori comandi.

---

## Account Demo Pre-Popolati

Il database SQLite distribuito è già pre-popolato con canzoni, generi e account utente di prova:

| Username | Password | Ruolo | Note |
|---|---|---|---|
| `admin_demo` | `admin12345` | Superuser | Accesso completo e admin. |
| `curator_demo` | `curator12345` | Curator (Staff) | Permessi di aggiunta/modifica/cancellazione canzoni. |
| `listener_demo`| `listener12345`| Listener | Utente standard in sola lettura (catalogo) e scrittura sulle proprie playlist. |

---

## Endpoint API (Django REST Framework)

Il sistema espone il catalogo musicale a client esterni tramite l'app `apis`, seguendo l'architettura REST:

| Metodo HTTP | Endpoint | Autenticazione | Descrizione |
|---|---|---|---|
| **GET** | `/api/songs/` | Pubblico | Lista dei brani musicali con paginazione. Supporta filtri per `artist` e `genre` (es. `?artist=Queen`). |
| **POST** | `/api/songs/` | Richiesta (Token/Session) | Creazione di un nuovo brano. |
| **GET** | `/api/songs/<id>/` | Pubblico | Dettagli di un brano specifico. |
| **PUT/PATCH** | `/api/songs/<id>/` | Richiesta (Token/Session) | Modifica parziale o totale di un brano specifico. |
| **DELETE** | `/api/songs/<id>/` | Richiesta (Token/Session) | Eliminazione di un brano. |

*(La sicurezza dell'API è implementata con Policy `IsAuthenticatedOrReadOnly` e `TokenAuthentication` nativa di DRF).*
