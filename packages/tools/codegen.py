import argparse
from packages.tools.openapi.codegen import generate_code as generate_openapi_code
from packages.tools.scribe.codegen.codegen import generate_code as generate_scribe_code
import os
import shutil
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Code generator')
    parser.add_argument('--api', action='store_true', help='Generate OpenAPI code only')
    parser.add_argument('--scribe', action='store_true', help='Generate Scribe code only')
    args = parser.parse_args()
    if "--api" in sys.argv:
        sys.argv.remove("--api")
    if "--scribe" in sys.argv:
        sys.argv.remove("--scribe")

    do_all = not args.api and not args.scribe

    if not do_all:
        if args.api:
            print("Running with --api -> OpenAPI")
        if args.scribe:
            print("Running with --scribe -> Scribe")
    
    path = os.path.dirname(os.path.realpath(__file__))

    if do_all or args.api:
        print("Generating OpenAPI code...")
        api_path = f"{path}/../frontend/src/api"
        if os.path.exists(api_path):
            shutil.rmtree(api_path)
        os.makedirs(api_path)
        generate_openapi_code()

    if do_all or args.scribe:
        print("Generating Scribe code...")
        scribe_path = f"{path}/../frontend/src/scribe"
        if os.path.exists(scribe_path):
            shutil.rmtree(scribe_path)
        os.makedirs(scribe_path)
        generate_scribe_code()