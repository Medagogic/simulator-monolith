from packages.server.sim_app.medsim import Router_MedSim
import json
from packages.server.sim_app.static_api import MedagogicAPI

from packages.server.web_architecture.sessionserver import SessionServer

def generate_code(verbose=False):
    async def generate():
        server = SessionServer(session_handler_class=Router_MedSim, static_api_class=MedagogicAPI)
        app = server.app

        schema = app.openapi()

        if verbose:
            for path, details in schema["paths"].items():
                print(path)

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

    import asyncio
    asyncio.run(generate())


if __name__ == "__main__":
    generate_code(verbose=True)