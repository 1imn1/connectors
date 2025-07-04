import json
import os
from pathlib import Path

get_version = os.getenv("CIRCLE_TAG")

manifest = {"name": "OpenCTI Connectors contracts", "contracts": []}

# Find all contracts
all_connector_schemas = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith("connector_schema.json"):
            all_connector_schemas.append(os.path.join(root, file))

# Add in manifest.json file
for connector_contract in all_connector_schemas:
    with open(connector_contract, encoding="utf-8") as file:
        connector_contract_schema = json.load(file)

        # Add in manifest if and only if manager_supported=true
        if connector_contract_schema["manager_supported"]:
            manifest["contracts"].append(connector_contract_schema)

# Format manifest
manifest = json.dumps(manifest, indent=2)

# Write and add manifest file in root
connector_root_path = Path(__file__).parents[3]
manifest_path = os.path.join(connector_root_path, "manifest.json")
with open(manifest_path, "w", encoding="utf-8") as manifest_file:
    manifest_file.write(manifest)
