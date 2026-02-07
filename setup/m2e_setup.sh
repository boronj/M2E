#####M2E setup#####

DIRECTORY="$1" #Set directory path to download M2E from (first argument)

#Setting up venv in M2E folder
sudo apt install python3.12-venv
pip install --upgrade virtualenv
python3 -m venv M2E
source "$DIRECTORY/M2E/bin/activate"
cd M2E && pip install --upgrade flatbuffers #Activates it?

#Setup for basic Python tools to most recent version
python -m pip install --upgrade pip setuptools wheel
python -m pip install jedi

#Install + reinstall ffmpeg
python -m pip uninstall ffmpeg -y
sudo apt remove ffmpeg -y
sudo apt install ffmpeg -y
python -m pip install ffmpeg-python -y

#Install M2E + dependencies
python -m pip install -e "$DIRECTORY/M2E/" --use-pep517 --verbose
pip show m2e #This should show the package, otherwise look back and figure out wtf went wrong 
