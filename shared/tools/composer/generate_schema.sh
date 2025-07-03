#!/bin/bash

set -e  # exit on error

# Get Python version
python_version=$(python --version)
echo -e "Version of Python is: $python_version\n"

# Create manifest json
cat <<EOF > manifest.json
{
  "name": "OpenCTI Connectors contracts",
  "contracts": []
}
EOF

# Find generator sample path
generator_path=$(find . -name "generator.py.sample")

# Find all parents directory
# printf action with the %h format specifier, which prints the directory part (parent directory) of the file path
connector_directories_path=$(find . -name "__infos__" -printf '%h\n')
echo "$connector_directories_path"

# Loop in each connector directory with infos
for connector_directory in $connector_directories_path
do
  if [ -d "$connector_directory" ]; then
    # Copy temporarily the generator script
    cp "$generator_path" "$connector_directory"/generator_tmp.py
    # Install dependencies
    requirements_file=$(find "$connector_directory" -name "requirements.txt")
    echo 'Found requirements.txt file: ' "$requirements_file"
    # Create isolated virtual environment
    venv_name=".temp_venv"
    project=$(echo "$requirements_file" | cut -d'/' -f1-3)
    echo 'Generate venv in project: ' "$project"

    echo 'Creating isolated virtual environment'
    python -m venv "$connector_directory/$venv_name"
    # Activate virtual environment according to OS
    if [ -f "$connector_directory/$venv_name/bin/activate" ]; then
      # shellcheck disable=SC1090
      source "$connector_directory/$venv_name/bin/activate"  # Linux/MacOS
    elif [ -f "$connector_directory/$venv_name/Scripts/activate" ]; then
      # shellcheck disable=SC1090
      source "$connector_directory/$venv_name/Scripts/activate"  # Windows
    fi

    echo -e '\nInstalling requirements...'
    python -m pip install -q -r "$requirements_file"

    echo "Clean Up environment..."
    echo -e '\nRemoving virtual environment'
#    deactivate
    #rm -rf "$venv_name"
  fi
done

# Copy generator sample in generator_tmp.py
#generator_path=$(find . -name "generator.py.sample")
#cp "$generator_path" "$current_path"/generator_tmp.py
#
#
## Install dependencies
#requirements_file=$(find $current_path -name "requirements.txt")
#echo 'Found requirements.txt file:' "$requirements_file"
#
#venv_name=".temp_venv"
#project=$(echo "$requirements_file" | cut -d'/' -f1-3)
#echo 'Generate venv in project: ' $project
#
#echo 'Creating isolated virtual environment'
#python -m venv "$current_path/$venv_name"
#if [ -f "$current_path/$venv_name/bin/activate" ]; then
#  source "$current_path/$venv_name/bin/activate"  # Linux/MacOS
#elif [ -f "$current_path/$venv_name/Scripts/activate" ]; then
#  source "$current_path/$venv_name/Scripts/activate"  # Windows
#fi
#
#echo -e '\nInstalling requirements...'
#python -m pip install -q -r "$requirements_file"

# Write Python version to manifest.json in the base directory
#echo -e "\nRun script and generate schema...\n"
#
#python $current_path/generator_tmp.py > "$current_path/__infos__/connector_schema.json"
#echo "Created connector schema in $current_path"

#echo "cleanup"
#echo 'Removing virtual environment'
#deactivate
##rm -rf "$venv_name"