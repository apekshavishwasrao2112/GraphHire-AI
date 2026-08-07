# GraphHire AI

GraphHire AI is a graph-powered developer networking platform for exploring relationships between developers, skills, companies, projects, technologies, certifications, and locations.

## Overview

This project combines a Flask backend with a premium React + Vite frontend to create a production-style SaaS experience for graph-based talent intelligence.

## Architecture

- Frontend: React, Vite, React Router, Tailwind CSS, Framer Motion, Recharts, React Flow
- Backend: Flask with Blueprint architecture, services, controllers, queries, and error handling
- Database: CognoDB Cloud / Neo4j-compatible graph database
- API communication: Axios and TanStack React Query

## Project structure

- backend/: Flask app, config, API routes, services, queries
- src/: React app shell, pages, layouts, services, styling, context
- public/: static assets

## Installation

### Frontend

1. Install dependencies
   npm install
2. Start the dev server
   npm run dev

### Backend

1. Install Python dependencies
   pip install -r backend/requirements.txt
2. Create an environment file
   copy .env.example .env
3. Start the Flask server
   python backend/app.py

## Environment variables

Create a .env file in the project root with values for:

- COGNODB_URI
- COGNODB_USERNAME
- COGNODB_PASSWORD
- SECRET_KEY
- PORT

## CognoDB Setup

1. Create a CognoDB Cloud instance from the provider dashboard.
2. Retrieve the Bolt URI, username, and password.
3. Add them to the environment variables above.
4. Ensure the Flask app can reach the database over the network.

## Flask to CognoDB connection

The backend uses the official Neo4j Python driver and parameterized Cypher queries. The connection is configured in the database layer and reads credentials from environment variables.

## API documentation

Available endpoints include:

- GET /developers
- GET /developer/<id>
- GET /companies
- GET /company/<id>
- GET /projects
- GET /project/<id>
- GET /skills
- GET /skill/<id>
- GET /recommendations/<developer>
- GET /search
- GET /graph/<developer>
- GET /dashboard

## Graph model

Key node types:

- Developer
- Skill
- Project
- Company
- Technology
- Certification
- Location

Key relationships:

- HAS_SKILL
- WORKED_AT
- BUILT
- USES
- LEARNED
- INTERESTED_IN
- CERTIFIED_IN
- LOCATED_IN
- COLLABORATED_WITH
- MENTORS

## Why a graph database

A graph database is ideal for this product because developer relationships, collaboration patterns, shared skills, and career trajectories are inherently connected. This makes recommendation systems and network exploration far more expressive than relational tables alone.

## Deployment

- Frontend: Vercel
- Backend: Render
- Environment variables should be configured separately for both deployment targets.

## Screenshots placeholder

Add screenshots of the landing page, dashboard, developer directory, analytics, and graph explorer here.

## Future improvements

- Live CognoDB-backed seed data ingestion
- Authentication and role-based access control
- Recommendation scoring and ranking improvements
- Advanced graph filtering and clustering
- Admin console for graph management
