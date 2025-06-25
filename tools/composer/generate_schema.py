import os
import subprocess

# filename = "generator_tmp.py"
# filepath = os.path.dirname(__file__)
# print(filepath)

result = subprocess.run(['sh', './tools/composer/generate_schema.sh'])