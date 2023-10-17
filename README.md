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

# Automatic code generation

## Web client event handlers
- In `packages/tools/sio_client_handler_generator`
- Run `python main.py`
- This looks in `packages/server/sim_app/sessiounrouter.py` for `emits(event_name, data_type)` decorators in the `SimSessionRouter` class
- It then generates a schema for each event, and uses json-schema-to-typescript (`json2ts`) to generate typescript types
- Then, we give this to GPT to generate an abstract class which automatically connects the socketio handlers to the events
- This gets put in `packages/frontend/src/sioevents`