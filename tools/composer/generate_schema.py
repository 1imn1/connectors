import os
import json
import subprocess

# filename = "generator_tmp.py"
# filepath = os.path.dirname(__file__)
# print(filepath)

result = subprocess.run(['sh', './tools/composer/generate_schema.sh'])

# test add in manifest
# json_files = []
# for root, dirs, files in os.walk('.'):
#     for file in files:
#         if file.endswith('connector_schema.json'):
#             json_files.append(os.path.join(root, file))
# print(json_files)
#
#
# def load_connector_infos(json_file_path=None, filename=None) -> dict:
#     """
#     Utility function to load a json file to a dict
#     :param json_file_path: json_file_path in string
#     :return:
#     """
#     filepath = json_file_path if json_file_path else os.path.join(os.path.dirname(__file__), ".", filename)
#     with open(filepath, encoding="utf-8") as json_file:
#         return json.load(json_file)
#
#
# for json_file_path in json_files:
#     connector_infos = load_connector_infos(json_file_path)
#     manifest_infos = load_connector_infos(json_file_path=None, filename="manifest.json")





