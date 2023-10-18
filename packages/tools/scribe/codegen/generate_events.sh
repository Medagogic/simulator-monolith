#!/bin/bash

# Navigate to the directory where the script is located
cd "$(dirname "$0")"

# Execute the json2ts command with directory parameters
json2ts -i schemas/scribe.schema.json -o generated/scribetypes.d.ts