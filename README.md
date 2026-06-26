# Backend Project: Music Streaming Service

**Student:** Samuele Dell'Erba
**Project Type:** Full-Stack Web Application (with REST API support)  
**Framework Used:** Django 5.x + Django REST Framework  

---

## Project Description

This project involves the development of a web application for a music streaming service, structured on a **hybrid Monolithic MVT** architecture, with built-in support for **REST APIs**. The application allows managing a music catalog (genres, songs) and creating personal playlists by users.

The project includes an authentication system, role differentiation (Listener and Curator), and custom forms rendered with Bootstrap 5, fully complying with the assignment requirements.

### Advanced Features Implemented (Beyond basic requirements)
To make the application more realistic and engaging, the following extra features have been added:
- **Smart Recommendations:** The homepage suggests new tracks by analyzing the user's favorite "Genre" and "Artist" in real-time (based on "Likes" and songs in their playlists), automatically hiding already known tracks.
- **Social / Community Features:** Users can send **friend requests** (which can be accepted or rejected), write **comments** and nested replies under tracks, and view other users' public profiles.
- **Advanced Playlist Management:** Playlists can be set as Private, "Friends Only", or Editorial (Staff). 
- **Audio File Upload:** It is possible to upload real audio files (`.mp3`, `.wav`, etc.). A dedicated JavaScript script automatically extracts the duration from the file in milliseconds before saving it to the database, preventing manual input errors.
- **Dynamic Interface and Dark Mode:** The design uses a custom "Neo-Brutalism" aesthetic, featuring a persistent **Dark/Light mode** system saved in the browser's LocalStorage.

---

## Features by Role

The system uses a custom user model (`CustomUser`) with predefined roles that regulate access and content management.

### Role: **Listener** (Standard User)
- Free navigation and browsing of the song catalog and musical genres.
- Creation and viewing of personal playlists.
- Access and navigation to routes protected by `LoginRequiredMixin`.
- Read-only consumption of the APIs.

### Role: **Curator** (Staff Member)
- All the features of the Listener.
- Insertion, modification, and deletion (CRUD) of music tracks from the catalog (via protected Class-Based Views and via REST API).
- Management through the administration panel (`/admin`).
- Destructive or write operations are protected on the backend by the `PermissionRequiredMixin`.

---

## Installation and Startup Instructions (Local Development)

Requirements: Python 3.10+

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. **Create and activate the Virtual Environment**
   - On Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```
   The application will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

> **Note:** The `db.sqlite3` file is already included and populated, you can log in with the demo accounts below without running any additional commands.

---

## Pre-Populated Demo Accounts

The distributed SQLite database is already pre-populated with songs, genres, and test user accounts:

| Username | Password | Role | Notes |
|---|---|---|---|
| `admin_demo` | `admin12345` | Superuser | Full access and admin. |
| `curator_demo` | `curator12345` | Curator (Staff) | Permissions to add/edit/delete songs. |
| `listener_demo`| `listener12345`| Listener | Standard read-only user (catalog) and write access to their own playlists. |

---

## API Endpoints (Django REST Framework)

The system exposes the music catalog to external clients via the `apis` app, following the REST architecture:

| HTTP Method | Endpoint | Authentication | Description |
|---|---|---|---|
| **GET** | `/api/songs/` | Public | List of music tracks with pagination. Supports filters for `artist` and `genre` (e.g. `?artist=Queen`). |
| **POST** | `/api/songs/` | Required (Token/Session) | Creation of a new track. |
| **GET** | `/api/songs/<id>/` | Public | Details of a specific track. |
| **PUT/PATCH** | `/api/songs/<id>/` | Required (Token/Session) | Partial or full modification of a specific track. |
| **DELETE** | `/api/songs/<id>/` | Required (Token/Session) | Deletion of a track. |

*(API security is implemented with DRF's native `IsAuthenticatedOrReadOnly` Policy and `TokenAuthentication`).*

---

## Deployment Link

The application is regularly deployed and reachable online at the following address:
**[INSERT DEPLOYMENT LINK HERE (e.g. Render, Heroku)]**

---

## Testing Scenario (Browser-based Workflow)

As required by the specifications for Full-Stack projects, here is a short scenario to test the functioning of roles and permissions directly from the browser:

1. **Listener Permissions Test (Access Denied)**
   - Go to the site address and click on **Login**.
   - Log in with the `listener_demo` account (password: `listener12345`).
   - Go to the **Music Catalog** page. You will notice that the "Add Song", "Edit", or "Delete" buttons are **not** present.
   - (Optional) Try to force access to the track creation URL: add `/add/` to the catalog URL (e.g. `/music/songs/add/`). You will receive a 403 error (Access Denied) because you are a Listener and not a Curator.
   
2. **Curator Features Test (Creation and Management)**
   - **Logout** and log in again as `curator_demo` (password: `curator12345`).
   - Go to the **Music Catalog**. You will now see the green **"+ Add Song"** and **"Manage Genres"** buttons.
   - Click on **+ Add Song**.
   - Fill out the form: enter a title, an artist, and select a genre. Upload an audio file (the *Duration* field will auto-fill and lock to prevent tampering).
   - Click **Add**. You will be redirected to the catalog and see a green success message. Your new song is now in the catalog.
   
3. **Social and Playlist Test (User Interaction)**
   - From the Home or Catalog, click on the heart (🤍) next to the newly created song to add it to your favorites (it will turn into ❤️).
   - Expand the "Add to..." dropdown menu and create a new playlist called "My Hits".
   - Go back to the **Home**: you will notice that the recommendation system ("Recommended for you") has analyzed your Likes and Playlists, proposing similar tracks while automatically discarding the ones you already know!
