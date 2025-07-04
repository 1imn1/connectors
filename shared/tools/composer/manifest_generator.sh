#!/bin/bash

set -e  # exit on error

activate_venv() {
    # Method to activate isolate venv

    # Install dependencies
    requirements_file=$(find "$1" -name "requirements.txt")

    # Create isolated virtual environment in connector path
    venv_name=".temp_venv"
    echo '> Creating isolated virtual environment...'
    python -m venv "$1/$venv_name"

    # Activate virtual environment according to OS
    if [ -f "$1/$venv_name/bin/activate" ]; then
      source "$1/$venv_name/bin/activate"  # Linux/MacOS
    elif [ -f "$1/$venv_name/Scripts/activate" ]; then
      source "$1/$venv_name/Scripts/activate"  # Windows
    fi

    echo '> Installing requirements...'

    # -qq: Hides both informational and warning messages, showing only errors.
    python -m pip install -qq -r "$requirements_file"

    # Check if venv is well created
    venv_exists=$(find "$1" -name ".temp_venv")

    if [ -d "$venv_exists" ]; then
      echo "✅- Requirements installed !"
    else
      echo "❌- Requirements not installed..."
    fi
}

deactivate_venv() {
    # Method to deactivate venv and remove the folder
    echo -e "\n> Clean Up environment..."
    deactivate
    echo "> Removing temp venv..."
    rm -rf "$1"
}

# Find all parents directory of connector with config loader
# printf action with the %h format specifier, which prints the directory part (parent directory) of the file path
connector_directories_path=$(find . -name "__infos__" -printf '%h\n')
echo -e "Generate contract for: " "\n$connector_directories_path"

# Loop in each connector directory with infos
for connector_directory_path in $connector_directories_path
do
  if [ -d "$connector_directory_path" ]; then
    # Activate isolated venv
    activate_venv "$connector_directory_path"
    # create tmp_schema_generator
    generator_path=$(find . -name "generator.py.sample")
    cp "$generator_path" "$connector_directory_path""/generator_tmp.py"
    # apply generator
    python "$connector_directory_path""/generator_tmp.py"

    # Clean up
    # Remove tmp_schema_generator
#    rm "$connector_directory_path/generator_tmp.py"

#    deactivate_venv "$connector_directory_path/$venv_name"
  fi
done

generate_manifest=$(find . -name "generate_manifest.py")
echo -e "\nGenerating manifest file..."
python "$generate_manifest"

# Ensure manifest is created
manifest_exists=$(find "$(pwd)" -name "manifest.json")

if [ -f "$manifest_exists" ]; then
  echo "✅- Manifest well created !"
else
  echo "❌- Manifest not created !"
fi

