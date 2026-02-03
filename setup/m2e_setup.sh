#####M2E setup#####

DIRECTORY="$1" #Set directory path to download M2E from (first argument)

#Setup for basic Python tools to most recent version
python -m pip install --upgrade pip setuptools wheel
python -m pip install jedi

#Install + reinstall ffmpeg
python -m pip uninstall ffmpeg -y
sudo apt remove ffmpeg
sudo apt install ffmpeg
python -m pip install ffmpeg-python

#Setting up venv in M2E folder
sudo apt install python3.12-venv
pip install --upgrade virtualenv
python3 -m venv M2E
python3 -m venv M2E
source "$DIRECTORY/M2E/bin/activate"

#Install M2E + dependencies
python -m pip install -e "$DIRECTORY/M2E/" --use-pep517
pip show m2e #This should show the package, otherwise look back and figure out wtf went wrong
