from packages.tools.openapi.codegen import generate_code as generate_openapi_code
from packages.tools.scribe.codegen.codegen import generate_code as generate_scribe_code
import os
import shutil

if __name__ == "__main__":
    # Delete the folders
    path = os.path.dirname(os.path.realpath(__file__))

    api_path = f"{path}/../frontend/src/api"
    scribe_path = f"{path}/../frontend/src/scribe"

    if os.path.exists(api_path):
        shutil.rmtree(api_path)
    os.makedirs(api_path)

    if os.path.exists(scribe_path):
        shutil.rmtree(scribe_path)
    os.makedirs(scribe_path)

    generate_openapi_code()
    generate_scribe_code()