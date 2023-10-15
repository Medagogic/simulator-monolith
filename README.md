# About
- This is, at a high level, a framework for session-based apps to expose data via FastAPI and SocketIO
- We then have a web frontend that can connect to the backend and display the data
- Data types are decided by backend, exposed via FastAPI, converted with OpenAPI Generator to Typescript types, and used in the frontend

# Architecture Decision Records
- We use ADRs to document decisions made during development
- See [adr/0001-use-ADR.md](adr/0001-use-ADR.md) for more info

# Backend
- Set up a virtual env and install requirements.txt
- Run `python main.py` to start the server

# Frontend
- Install dependencies using npm
- Run `npm run dev` to start the dev server