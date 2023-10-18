from openapi.codegen import generate_code as generate_openapi_code
from scribe.codegen.codegen import generate_code as generate_scribe_code

if __name__ == "__main__":
    generate_openapi_code()
    generate_scribe_code()