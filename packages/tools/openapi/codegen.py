import fastapi
import socketio
from packages.server.sim_app.medsim import Router_MedSim
import json

def generate_code(verbose=False):
    app = fastapi.FastAPI(title="Medagogic Web Server")
    sio = socketio.AsyncServer(async_mode="asgi")
    router = Router_MedSim(app, sio)

    schema = app.openapi()

    # get the location of this file
    import os
    path = os.path.dirname(os.path.realpath(__file__))

    # write the schema to a file
    output_file = f"{path}/openapi_schema.json"
    with open(output_file, "w") as file:
        json.dump(schema, file, indent=4)
        if verbose:
            print(f"Saved API JSON to {output_file}")

    # run generate_api.sh
    import subprocess
    completed_process = subprocess.run(["bash", f"{path}/generate_api.sh", f"openapi_schema.json", f"../../frontend/src/api"], text=True, capture_output=True)

    if completed_process.stderr.strip():
        print(completed_process.stderr)

    print("Generated client API in frontend/src/api")


if __name__ == "__main__":
    generate_code(verbose=True)