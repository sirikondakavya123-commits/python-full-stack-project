# Travel Diary 

## Project Description
The **Travel Dairy** project is a personal travel management application that allows users to maintain a list of destinations they wish to visit. Users can add, track, and manage destinations, mark them as visited, add notes, and optionally organize them by categories.  

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

## Project Structure

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

## Quick Start

## Prerequisites

- Python 3.8 or higher
- A Supabase account
- Git(Push,cloneing)

### 1. clone or Download the project
# Option 1: Clone with Git
git clone <repository-url>

# Option 2:Download and extract the ZIP file
### 2. Install Dependencies
pip install -r requirements.txt

### 3.Set Up supabase Datebase

1.create a supabase Project:

2.create a tasks table:
-Go to the SQL Editor in your supabase dashboard
-Run this SQL command:
CREATE TABLE users (
    user_id UUID PRIMARY KEY,                 
    user_email TEXT UNIQUE NOT NULL,            
    user_name TEXT,                             
    signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,             
    category_name TEXT NOT NULL                  
);

CREATE TABLE destinations (
    id SERIAL PRIMARY KEY,                       
    user_id UUID REFERENCES users(user_id),      
    destination_name TEXT NOT NULL,              
    country_name TEXT NOT NULL,                   
    is_visited BOOLEAN DEFAULT FALSE,             
    notes TEXT,                                   
    category_id INT REFERENCES categories(category_id),  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP       
);

3.**Get Your Credentials:
### 4.Configure Environment Variables

1.create a`.env` file in the project root.
2.add your Credentials to `.env`:
SUPABASE_URL="https://zcastpfxbgxiizesbycb.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpjYXN0cGZ4Ymd4aWl6ZXNieWNiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIzODAsImV4cCI6MjA3MzY1ODM4MH0.BN-ZC6S3doCluO_VuE-eWoC882L0s1-oQ3lLs9vKgjU"

### 5.Run the Application

## Stremlit Frontend

streamlit run frontend/app.py
The app will own in your browser at `http://localhost:8501`

## FastAPI Backend

cd api
The api will be available at `http://localhost:8501`

## how to use


## **How to Use**

1. **Setup**
   - Install dependencies:
     ```bash
     pip install streamlit supabase
     ```
   - Configure your Supabase project:
     - Create a project on [Supabase](https://supabase.com/)
     - Enable **Auth** for email/password
     - Create the required tables (`bucket_list`, optional `categories`)
     - Copy **Supabase URL** and **API Key** into your Python app

2. **Run the App**
   ```bash
   streamlit run streamlit_app.py


## Technical Details


## Technical Details

### Architecture
The Travel Bucket List project is designed with a frontend that handles user interaction and a backend database that stores user data and destinations. Each user has a private bucket list that they can manage securely.

### Authentication
- Users sign up and sign in with email and password.
- Each user is assigned a unique ID that links their destinations to their account.

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


## Technologies Used

- **Frontend:** Streamlit (Python web framework)
- **Backend:** FastAPI  (Python REST API framework)
- **Database:** Supabase (PostgreSQL-based backend-as-a-service)  
- **Language** Python 3.8+
---

### Key Components

1. **`src/db.py`**: Database operations
   -Handles all CRUD operations with Supabase
2. **`src/logic.py`**:Business logic Task validation and processing
3. **`API/main.py`**:FastAPI endpoints
4. **frontend/app.py**:streamlit web interface
5. **`.env`**:A file that securely stores environment variables and configuration settings
6. **`requirements.txt`** A file listing all Python packages and their versions needed for a project.

## Trouble Shooting
## common issues
1.Environment Setup:
.env file missing or misconfigured
Incorrect Python version

2.Dependencies:
Missing packages or incorrect versions (pip install -r requirements.txt)
Conflicts between package versions

3.Database:
Database connection errors (wrong credentials, DB not running)
Missing tables or migrations

4.File Paths:
Incorrect paths for assets or configuration files

### Future Enhancements

### Future Enhancements
### Future Enhancements

**1. Social Login**
Integrate Google, Facebook, or other social login options for easier signup and sign-in.

**2. Real-time Notifications**
Add real-time notifications for user actions, updates, or reminders.

**3. Search & Filter**
Implement search and filter functionality to quickly find destinations or items.

**4. Image Uploads**
Allow users to upload images for destinations, notes, or experiences.

**5. Analytics Dashboard**
Provide a dashboard to track visited destinations versus wishlist items.

**6. Multi-language Support**
Enable support for multiple languages to reach a wider audience.

**7. Mobile Responsiveness**
Optimize the interface for mobile devices and improve overall user experience.

**8. Offline Mode**
Add offline mode or local caching to allow access without an internet connection.

### Support
If you encounter any issues or have questions, please email: `sirikondakavya123@gmail.com`.

