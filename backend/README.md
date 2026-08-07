# GraphHire AI Backend

GraphHire AI Backend is a Flask-based API service that powers the GraphHire AI talent intelligence platform.

The backend provides developer search, developer directory data, dashboard analytics, recommendations, and graph-powered talent intelligence through a modular Flask architecture.

## Technology Stack

- Python
- Flask
- Gunicorn
- Neo4j-compatible graph database
- CognoDB Cloud
- Neo4j Python Driver
- Parameterized Cypher queries

## Architecture

The backend follows a modular architecture that separates application configuration, database access, business logic, request handling, routes, validation, serialization, and error handling.

```text
backend/
├── app.py
├── config.py
├── database.py
├── seed.py
├── controllers/
│   └── developer_controller.py
├── middleware/
│   └── error_handlers.py
├── models/
├── queries/
│   └── developer_queries.py
├── routes/
│   └── developer_routes.py
├── services/
│   └── developer_service.py
├── utils/
│   ├── serialization.py
│   └── validation.py
├── test/
│   └── smoke.py
└── requirements.txt
````

## Main Components

### `app.py`

Creates and configures the Flask application and registers the API routes.

### `config.py`

Loads application configuration and environment variables.

### `database.py`

Provides the graph database connection and database access layer using the Neo4j-compatible driver.

### `seed.py`

Provides the graph data seeding entrypoint.

### `routes/`

Contains Flask route definitions and API endpoints.

### `controllers/`

Handles incoming API requests and coordinates responses.

### `services/`

Contains application and business logic used by the controllers.

### `queries/`

Contains parameterized Cypher queries used to interact with the graph database.

### `middleware/`

Contains error handling and related Flask middleware.

### `utils/`

Contains validation and response serialization helpers.

## Environment Variables

Create a `.env` file in the project root.

The backend expects the required CognoDB/database configuration and application configuration to be supplied through environment variables.

Example:

```env
COGNODB_URI=your_cognodb_uri
COGNODB_USERNAME=your_username
COGNODB_PASSWORD=your_password
SECRET_KEY=your_secret_key
PORT=5000
```

Never commit the `.env` file or database credentials to GitHub.

Use `.env.example` as the safe template for environment configuration.

## Installation

From the project root:

```powershell
pip install -r backend/requirements.txt
```

## Run Locally

Start the Flask backend with:

```powershell
python -m backend.app
```

The local API is available at:

```text
http://127.0.0.1:5000
```

## API

The backend currently provides API functionality for areas including:

* Developer directory
* Developer search
* Dashboard analytics
* Recommendations
* Graph-powered search

Example endpoints:

```text
GET /developers
GET /dashboard
GET /recommendations/<developer_email>
GET /search
```

## Health and Database Behavior

The API is designed to handle database availability issues gracefully.

Database-dependent endpoints can return empty or fallback payloads when the graph database is unavailable rather than causing the Flask application to crash.

## Graph Database

GraphHire AI uses CognoDB as the graph database layer.

The database follows a Neo4j-compatible model and uses Cypher queries to represent relationships between developers, skills, companies, technologies, projects, and other talent signals.

Parameterized queries are used to avoid constructing database queries directly from untrusted request input.

## Production Deployment

The backend is designed to run on Render using Gunicorn.

### Render Configuration

Set the Render service root directory to:

```text
backend
```

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
gunicorn app:app
```

Set the required environment variables in the Render dashboard instead of committing secrets to the repository.

After deployment, Render provides a public API URL similar to:

```text
https://your-graphhire-backend.onrender.com
```

The frontend uses this URL to communicate with the backend.

## Local Development

For local development, run the backend:

```powershell
python -m backend.app
```

and run the React frontend from a second terminal:

```powershell
npm run dev
```

The frontend communicates with the Flask API through the configured API base URL.

## Testing

The backend contains smoke-test and database-check utilities under:

```text
backend/test/
backend/check/
```

These utilities can be used during development to verify application and database connectivity.

## Security Notes

* Never commit `.env` files.
* Never expose CognoDB credentials in frontend code.
* Store production secrets in Render environment variables.
* Use parameterized Cypher queries.
* Keep development and production credentials separate.

````

---

# 2. Main React `README.md`

Replace your root:

```text
README.md
````

with this:

````markdown
# GraphHire AI

GraphHire AI is a graph-powered talent intelligence platform for exploring developers, skills, companies, technologies, and relationships in a connected talent network.

The application combines a React + Vite frontend with a Flask API backend and a CognoDB Cloud graph database.

## Overview

GraphHire AI provides a developer-focused interface for exploring graph-powered talent signals.

The platform includes:

- Developer directory
- Developer search
- Dashboard analytics
- Developer recommendations
- Graph-powered talent relationships
- Technology and skill exploration
- Interactive graph-based intelligence

## Technology Stack

### Frontend

- React
- Vite
- React Router
- Axios
- CSS


### Backend

- Python
- Flask
- Gunicorn
- Flask modular architecture
- Neo4j Python Driver
- Parameterized Cypher queries

### Database

- CognoDB Cloud
- Neo4j-compatible graph database

## Architecture



                    GitHub
                       │
             GraphHire-AI repository
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
       Vercel                    Render
      Frontend                   Backend
       React                     Flask
          │                         │
          └──────────┬──────────────┘
                     │
                     ▼
                 CognoDB
                Graph Database


## Project Structure

```text
GraphHire AI/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── seed.py
│   ├── controllers/
│   ├── middleware/
│   ├── models/
│   ├── queries/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── test/
│   └── requirements.txt
│
├── public/
│
├── src/
│   ├── components/
│   ├── context/
│   ├── layouts/
│   ├── pages/
│   ├── services/
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
│
├── .env.example
├── .gitignore
├── index.html
├── package.json
├── package-lock.json
└── vite.config.js
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/GraphHire-AI.git
cd GraphHire-AI
```

## Frontend Setup

Install the frontend dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:3000
```

## Backend Setup

Create and activate a Python virtual environment if required.

Install backend dependencies:

```powershell
pip install -r backend/requirements.txt
```

Create the environment file:

```powershell
copy .env.example .env
```

Configure the required database and application variables in `.env`.

Start the Flask backend:

```powershell
python -m backend.app
```

The backend will normally be available at:

```text
http://127.0.0.1:5000
```

## Running the Full Application Locally

The application uses two processes during development.

### Terminal 1 — Flask API

```powershell
python -m backend.app
```

### Terminal 2 — React frontend

```powershell
npm run dev
```

Then open:

```text
http://localhost:3000
```

The React frontend communicates with the Flask API on port `5000`.

## Environment Variables

Create a `.env` file for local development.

Typical configuration includes:

```env
COGNODB_URI=your_cognodb_uri
COGNODB_USERNAME=your_username
COGNODB_PASSWORD=your_password
SECRET_KEY=your_secret_key
PORT=5000
```

The frontend API URL can be configured through:

```env
VITE_API_URL=http://127.0.0.1:5000
```

Do not commit `.env` to GitHub.

Production secrets must be configured through the deployment platform's environment-variable settings.

## CognoDB Setup

GraphHire AI uses CognoDB Cloud as the graph database layer.

To configure the database:

1. Create a CognoDB Cloud instance.
2. Obtain the database connection URI.
3. Obtain the database username and password.
4. Add the credentials to the backend environment variables.
5. Ensure the backend can connect to the database.
6. Seed the graph data when required by the application.

The backend uses a Neo4j-compatible Python driver and Cypher queries to communicate with the graph database.

## API

The frontend communicates with the Flask API using Axios.

Current API functionality includes:

```text
GET /developers
GET /dashboard
GET /recommendations/<developer_email>
GET /search
```

The API provides graph-backed developer information, dashboard metrics, search, and recommendation functionality.

## Graph Model

The application models talent information as a connected graph.

### Main Node Types

```text
Developer
Skill
Company
Project
Technology
Certification
Location
```

### Main Relationships

```text
HAS_SKILL
WORKED_AT
BUILT
USES
LEARNED
INTERESTED_IN
CERTIFIED_IN
LOCATED_IN
COLLABORATED_WITH
MENTORS
```

The graph structure allows relationships between developers and their technical ecosystem to be queried and explored naturally.

## Why a Graph Database?

Developer talent data is highly interconnected.

For example:

```text
Developer
    │
    ├── HAS_SKILL ──> Java
    │
    ├── WORKED_AT ──> Infosys
    │
    ├── USES ───────> Neo4j
    │
    └── COLLABORATED_WITH ──> Another Developer
```

A graph database makes these relationships first-class data rather than requiring multiple relational joins.

This is useful for:

* Talent discovery
* Skill matching
* Developer recommendations
* Relationship exploration
* Company and technology analysis
* Network intelligence

## Deployment

The application uses separate deployment services for the frontend and backend.

### Frontend

The React/Vite application can be deployed to:

```text
Vercel
```

### Backend

The Flask API can be deployed to:

```text
Render
```

### Database

The graph database is hosted through:

```text
CognoDB Cloud
```

The production architecture is:

```text
User
 │
 ▼
Vercel
React Frontend
 │
 │ HTTPS API requests
 ▼
Render
Flask + Gunicorn
 │
 │ Neo4j-compatible connection
 ▼
CognoDB Cloud
Graph Database
```

## Render Backend Configuration

For the Render backend service:

### Root Directory

```text
backend
```

### Build Command

```text
pip install -r requirements.txt
```

### Start Command

```text
gunicorn app:app
```

The required backend environment variables should be configured in Render.

## Vercel Frontend Configuration

The frontend should use the deployed Render backend URL.

Configure the following environment variable in Vercel:

```text
VITE_API_URL=https://your-graphhire-backend.onrender.com
```

The frontend API service uses this value as the backend base URL.

## GitHub

The complete application is maintained in a single repository.

```text
GitHub Repository
        │
        ├── backend/  → Render
        │
        └── frontend  → Vercel
```

Keeping the frontend and backend in one repository makes the project easier to review and maintain.

## Development Notes

The project intentionally separates frontend and backend responsibilities.

The frontend handles:

* UI
* Routing
* Search interactions
* Data visualization
* Graph visualization

The backend handles:

* API requests
* Database access
* Cypher queries
* Business logic
* Validation
* Serialization
* Error handling

## Future Improvements

Potential improvements include:

* Authentication and authorization
* Role-based access control
* Advanced recommendation scoring
* Improved graph clustering
* Advanced graph filters
* Real-time graph updates
* Admin graph management
* Automated graph-data ingestion
* Expanded developer profiles
* More detailed analytics

