# Music Streaming Service

![Backend](https://img.shields.io/badge/Backend-Django_5-092E20?style=flat&logo=django)
![Frontend](https://img.shields.io/badge/Frontend-Bootstrap_5_|_Vanilla_JS_|_HTMX-563D7C?style=flat&logo=bootstrap)
![Database](https://img.shields.io/badge/Database-SQLite-003B57?style=flat&logo=sqlite)
![Architecture](https://img.shields.io/badge/Architecture-MVT-ff69b4?style=flat)

**Student:** Samuele Dell'Erba  
**Chosen Project Type:** Full-Stack Web Application - Music Streaming Service  
**Framework Used:** Django 5.x (with Bootstrap 5 & Vanilla JS)  
**Deployment Link:** https://samybravy15.pythonanywhere.com/

---

## 📖 Description

This project is a complete, dynamic **Music Streaming Service** built on a Monolithic MVT (Model-View-Template) architecture using Django. Its primary purpose is to provide a fully functional, interactive platform where users can discover, stream, and manage their favorite music while interacting with a vibrant community. The application is designed to handle different user roles (Listeners, Curators, and Moderators) to demonstrate robust permissions and access control. It goes far beyond basic CRUD operations by integrating real `.mp3` audio file handling, an automated JS-based duration extraction system, dynamic playlists, a friendship network, nested community comment threads, and a smart recommendation engine that analyzes user preferences in real-time. The ultimate goal was to build a secure, scalable, and highly interactive web application that mimics the core functionalities of modern streaming giants like Spotify or SoundCloud, entirely within the Django ecosystem.

## ✨ Implemented Features 

The platform uses a custom user model with an icon-based avatar system and strict role-based access control.

### Guest (Unauthenticated User)
- **Authentication:** Secure Login and Logout functionalities handled natively by Django.
- **Registration:** New users can register an account directly from the browser.

### Listener (Standard User)
- **Audio Playback & Catalog:** Browse the music catalog, filter by Genre, Search by Name/Artist, and filter specifically for tracks that have real audio files (`Has Audio` filter). Thanks to HTMX, audio playback persists seamlessly across page navigations.
- **Playlists:** Create and manage personal playlists. Set visibility to Private or Public (friends only). Follow and save other users' public playlists (or Editorial playlists) to your own library.
- **User Profiles:** View and edit your personal profile (change your emoji avatar and personal informations). Visit other users' public profiles to see their role, recent comments, and public playlists (filtered by friendship status).
- **Social & Community:** Send, accept, or reject friend requests. Add "Likes" to songs. Participate in nested comment threads (with likes on comments).
- **Smart Recommendations:** The homepage dynamically analyzes the user's liked songs and playlists to calculate their favorite Genre and Artist in real-time, proposing new tracks while hiding those they already know.

### Curator
- **Catalog Management:** Full CRUD access to the Song Catalog and Genres directly from the frontend interface.
- **Smart Audio Upload:** Upload real `.mp3` files. A custom JavaScript script intercepts the file, reads its metadata, and automatically extracts the exact duration in milliseconds, preventing manual input tampering.
- **Editorial Playlists:** Can create special "Editorial" playlists (e.g., Top 10 Global) to highlight specific tracks for all users.

### Moderator
- **Community Guidelines:** Control over the platform's social aspect. Can view and delete any comment from any user across the platform to combat spam or inappropriate behavior.

### Administrator (Superuser)
- **System Control:** Full access to the protected Django Administration panel to manage the database natively.

---

## 🛠️ Local Installation Instructions

**Requirements:** Python 3.10+

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. **Create and Activate the Virtual Environment**
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
   The application will be accessible at `http://127.0.0.1:8000`.

> **Note on Database (`db.sqlite3`):** The repository includes a pre-populated `db.sqlite3` file containing demo data (users, real songs, playlists). If you ever need to recreate the database from scratch with perfect test data, run `python seed_data.py` after migrating.

---

## 🔐 Pre-Populated Demo Accounts

The `db.sqlite3` database includes the following accounts ready for testing:

| Username | Password | Role | Notes |
|---|---|---|---|
| `admin_demo` | `admin12345` | Administrator | Has `is_superuser=True`. Full admin panel access. |
| `curator_demo` | `curator12345` | Curator | Can add/edit/delete songs and upload audio files. |
| `moderator_demo`| `moderator12345`| Moderator | Can delete any comment on the platform. |
| `listener_demo`| `listener12345`| Listener | Standard user for browsing and playlists. |
| `alice` / `bob` / `charlie` / `dave` / `eve` / `frank` | `password123` | Listener | Secondary accounts used to demonstrate friend requests and community interactions. |
| `sara_curates` / `mike_curates` | `password123` | Curator | Additional staff accounts for catalog management. |
| `john_mod` / `lisa_mod` | `password123` | Moderator | Additional staff accounts for community moderation. |
| `spambot` | `password123` | Listener | A dummy account used to test moderation (has posted a spam link). |

---

## 🧪 Testing Scenario (Browser-based Workflow)

To quickly test the main workflows, roles, and permissions of the project, follow this short scenario (not all functionalities are tested in these tests):

### 1. Playback, Social & Moderation Test
- Go to the application and **Login** as `moderator_demo` (password: `moderator12345`).
- Navigate to the **Music Catalog**. Test the **"Has Audio"** checkbox filter and hit Search.
- Open the song **"Bohemian Rhapsody"**.
- Click the play button on the audio player to hear the real `.mp3` file.
- Scroll down to see a complex, nested comment thread featuring interactions between Listeners, Curators, and the Admin.
- Notice a comment left by `spambot` containing a scam link. Since you are logged in as a Moderator, you will see a red **Delete** button next to it. Click it to remove the comment.
- Reply to bob's comment and like alice's comment.
- Go to a different page and notice the song continuing to play.

### 2. Curator Test (Catalog Management)
- **Login** as `curator_demo` (password: `curator12345`).
- Go to the **Music Catalog**. You will now see the green **"+ Add Song"** button and the **"Manage Genres"** button.
- Add a new genre.
- Click **"+ Add Song"** (or edit one), fill in a Title, Artist, and select the new Genre. **Upload an audio file**; you will see the *Duration* field auto-fill.
- Click **Save**.
- If you created a new song, go to the **Home** page and notice it appears in the **Latest Additions** section.
- Go to **Playlists** and create a new playlist with **Editorial** visibility, and add the new song to it.
- **Verify (Access Denied):** Logout, log in as `listener_demo`, and try to manually visit the URL `/music/songs/add/`. You will get a **403 Forbidden** error because Listeners cannot perform CRUD operations on the catalog.
- Go to **Playlists** and notice the Editorial playlist with your new song in the **Famous Playlists** section, add it to your favorited playlists and see if it's in the **"My Favorites"** section.

### 3. Smart Recommendation Test
- While logged in as `listener_demo`, go to the **Music Catalog** and click the **Heart (🤍)** on a few Rock songs.
- Go to the **Playlists** tab and see the songs you liked in the "My Favorites" playlist.
- Return to the **Home** page.
- **Verify:** The "Recommended for you" section will analyze your recent likes and playlists in real-time, suggesting new Rock tracks while automatically hiding the ones you already liked.

### 4. Playlist Privacy & Social Connections Test
- **Login** as `alice` (password: `password123`).
- Go to the **Playlists** section. You will see Alice has a private playlist called "Guilty Pleasures".
- Go to the **Social / Friends** page. Accept the pending friend requests from Dave and Eve.
- **Verify Privacy:** Logout and log in as `dave` (password: `password123`). Go to Alice's **Profile** (by clicking her name on a comment or through the **Social** tab). You will see her public playlist ("Alice's Favorites"), but her "Guilty Pleasures" playlist remains completely hidden. Also notice her comments on **Recent Activity**.
- Click on your name in the top bar to go to your **Profile**. Edit your bio and icon, and save changes.

### 5. UI/UX and Theme Persistence Test
- Regardless of whether you are logged in or not, click the **Theme Toggle** (moon/sun icon) in the navigation bar to switch between light and dark mode.
- **Verify:** Refresh the page or close and reopen the browser tab. The application remembers your choice via `LocalStorage`, maintaining the high-contrast aesthetic seamlessly.

### 6. Admin Database Access Test
- **Login** as `admin_demo` (password: `admin12345`). You have all Curator and Moderator permissions.
- Click the **⚙️ Control Panel** button in the navigation bar.
- **Verify:** You are granted access to the native Django administration interface where you can bypass frontend logic and manually inspect users, comments, and relationships.

---

## 🤖 Main Use of AI

During the development of this project, AI assistants were mainly utilized for:
- **README.md:** Assisting in structuring and formatting this documentation for clarity and professional presentation.
- **Data Seeding (`seed_data.py`):** Helping to generate realistic mock data (users, songs, playlists, comments) and creating the script to populate the database for demonstration purposes.
- **General Refactoring:** Providing suggestions for code cleanup, organizing logic, and improving overall code structure.