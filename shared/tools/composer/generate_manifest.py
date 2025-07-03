import json
import os
from pathlib import Path

# filename = "generator_tmp.py"
filepath = os.path.dirname(__file__)
print(filepath)
parent = Path(__file__).parents[3]
print("PARENT", parent)
get_version = os.getenv("CIRCLE_TAG")

manifest = {"name": "OpenCTI Connectors contracts", "contracts": []}

# test add in manifest
json_files = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith("connector_schema.json"):
            json_files.append(os.path.join(root, file))
print(json_files)

for connector_contract in json_files:
    with open(connector_contract, encoding="utf-8") as file:
        test = json.load(file)
        manifest["contracts"].append(test)

manifest = json.dumps(manifest, indent=2)

manifest_path = os.path.join(parent, "manifest.json")
with open(manifest_path, "w", encoding="utf-8") as manifest_file:
    manifest_file.write(manifest)
