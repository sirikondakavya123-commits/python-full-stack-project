# Travel Diary – Travel Bucket List

## Project Description
The **Travel Bucket List** project is a personal travel management application that allows users to maintain a list of destinations they wish to visit. Users can add, track, and manage destinations, mark them as visited, add notes, and optionally organize them by categories.  

This project is built with **Python** and **Streamlit** for the frontend and uses **Supabase (PostgreSQL)** as the backend database for secure storage and authentication.

---


## Features
- **User Authentication:** Secure signup and login using Supabase Auth.
- **Add Destinations:** Users can add new places they want to visit.
- **Mark as Visited:** Track visited destinations.
- **Add Notes:** Keep personal notes for each destination.
- **Organize by Categories:** Group destinations into categories such as Beach, Mountain, City, etc.
- **Filter & Search:** Easily find destinations by country, category, or visited status.

---

TRAVEL DAIRY/
|
|---src/              # core application logic
|   |---logic.py      #Business logic and task
|   |---db.py         #database operations
|
|---API/              #backend API
|   |---main.py       #FastAPI endpoints
|  
|---frontend/         #frontend application
|   |---app.py        #streamlit web interface
|
|---requirements.txt  #install python dependencies
|---README.md         #project documentation
|---.env              #python Variables 



## Tech Stack
- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **Database:** Supabase (PostgreSQL)  

---

## Database Schema

### 1. Users Table
| Column       | Type      | Description                          |
|--------------|-----------|--------------------------------------|
| user_id      | UUID      | Primary Key; unique user ID (Supabase Auth ID) |
| user_email   | TEXT      | Unique email for login               |
| user_name    | TEXT      | Optional user name                   |
| signup_date  | TIMESTAMP | Account creation date                |

---

### 2. Bucket_List Table
| Column       | Type      | Description                          |
|--------------|-----------|--------------------------------------|
| id           | SERIAL    | Primary Key                          |
| user_id      | UUID      | Foreign Key → users.user_id (owner of the destination) |
| destination  | TEXT      | Name of the place                     |
| country      | TEXT      | Country of the destination            |
| visited      | BOOLEAN   | True if the user has visited the place |
| notes        | TEXT      | Optional notes about the destination |
| category_id  | INT       | Optional Foreign Key → categories.id |
| created_at   | TIMESTAMP | Defaults to CURRENT_TIMESTAMP        |

---

### 3. Categories Table
| Column | Type   | Description                   |
|--------|--------|-------------------------------|
| id     | SERIAL | Primary Key                   |
| name   | TEXT   | Name of the category (e.g., Beach, Mountain) |

---

## Getting Started

### Prerequisites
- Python 3.9+
- Supabase account
- Streamlit installed
- FastAPI installed

### Installation
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd travel-diary
