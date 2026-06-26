# BRIEF PROGETTO: Music Streaming Service (Full-Stack Web App & API-Ready)
**Framework Riferimento:** Django 4.0 / 5.x & Django REST Framework (Lezione 6)
**Architettura:** Ibrida (MVT Monolitica con predisposizione Endpoint RESTful)
**Database:** SQLite (Locale) | PostgreSQL (Produzione su Railway)

---

## 1. STRUTTURA DEL PROGETTO & MODULARITÀ (Riepilogo)
- **`django_project`:** Core dell'applicazione.
- **`pages`:** Gestione delle viste di atterraggio e della navigazione generale.
- **`music`:** Gestione del catalogo musicale, generi e logica CRUD.
- **`users`:** Gestione del modello utente personalizzato e dell'autenticazione.
- **`apis` (Nuova App - Lezione 6):** Blocco dedicato per isolare la logica degli endpoint REST sotto il prefisso `/api/`.

---

## 2. MODELLO DATI RELAZIONALE (ORM)
I modelli sono implementati in `music/models.py` ereditando da `models.Model`:
- **`Genre`:** `name` (CharField, unique), `description` (TextField).
- **`Song`:** `title` (CharField), `artist` (CharField), `genre` (ForeignKey verso `Genre`), `duration` (DurationField).
- **`Playlist`:** `name` (CharField), `owner` (ForeignKey verso il modello User), `songs` (ManyToManyField verso `Song`).

---

## 3. LOGICA DI PRESENTAZIONE & INTERFACCIA (MVT)
- **Ereditarietà a 3 livelli:** I template seguono la catena `base.html` -> `base_music.html` -> pagine specifiche (es. `song_list.html`).
- **Form e Validazione:** Utilizzo di `forms.ModelForm` con l'applicazione del filtro `{{ form|crispy }}` (tramite il pacchetto `django-crispy-forms`) per garantire layout puliti e DRY.
- **Metodi HTTP:** Richieste di lettura gestite via **GET**. Richieste di scrittura (creazione/modifica) gestite via **POST** accoppiate al tag obbligatorio `{% csrf_token %}`.

---

## 4. CONTROLLO ACCESSI & AUTORIZZAZIONE RIGIDA
- **Protezione Viste:** Uso del mixin `LoginRequiredMixin` (posto come primo argomento nelle CBV) e del decoratore `@login_required` nelle FBV.
- **Ruoli differenziati:** 
  - **Listener:** Può solo leggere il catalogo ed effettuare operazioni di scrittura limitate alle proprie playlist.
  - **Curator:** Utente con permessi di staff (`is_staff=True`). Le viste di inserimento canzoni sono protette a livello di backend tramite `PermissionRequiredMixin` impostando `permission_required = 'music.add_song'`.

---

## 5. PREDISPOSIZIONE REST API & SERIALIZZAZIONE (Vincoli Lezione 6)
Per esporre i dati del catalogo musicale a client esterni o script di test (Postman/curl), l'app `apis` implementerà i seguenti componenti nativi di DRF:

### A. Installazione e Registrazione
- Pacchetto installato nel sistema: `pip install djangorestframework`.
- Incluso nella sezione `INSTALLED_APPS` di `settings.py`: `"rest_framework"`.

### B. Serializzatori (`apis/serializers.py`)
Utilizzeremo `ModelSerializer` per convertire i querysets in tipi di dati nativi Python convertibili automaticamente in JSON:
```python
from rest_framework import serializers
from music.models import Song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'genre', 'duration')

```

### C. Viste API Generiche (`apis/views.py`)

Utilizzeremo le viste generiche di DRF per implementare endpoint puliti e robusti:

* **`SongAPIListView`:** Eredita da `generics.ListAPIView` per consentire la lettura in formato JSON del catalogo a chiunque.


* **`SongAPIDetailView`:** Eredita da `generics.RetrieveUpdateDestroyAPIView` per consentire la gestione completa del singolo brano (GET, PUT, PATCH, DELETE), blindata con permessi a livello di vista.



### D. Sicurezza dell'API: CORS & Autenticazione Stateless

* **CORS Headers:** Per evitare che il browser blocchi le chiamate provenienti da porte diverse durante lo sviluppo (es. un client frontend), installeremo `django-cors-headers` e configureremo `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` in `settings.py`.


* **Token Authentication:** L'API affiancherà all'autenticazione basata su sessione quella basata su Token (stateless, tramite l'app `authtoken` di Django), inserendo le configurazioni nel dizionario `REST_FRAMEWORK`.



### E. Funzionalità Advanced: Filtraggio e Paginazione

* **`django-filter`:** Integreremo il backend di filtraggio per permettere agli utenti dell'API di cercare brani tramite parametri nell'URL (es. `?title=icontains&genre=jazz`).


* **Paginazione:** Estenderemo la classe `PageNumberPagination` impostando un `page_size = 10` predefinito per frammentare i payload JSON di cataloghi molto grandi.