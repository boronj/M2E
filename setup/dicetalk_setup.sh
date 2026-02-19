DIRECTORY="$1"

#Setup venv
sudo apt install python3.12-venv
pip install --upgrade virtualenv
python3 -m venv M2E
source "$DIRECTORY/M2E/bin/activate"

#Pytorch 2.2.2
pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu124

#Install other requirements
git clone https://github.com/toto222/DICE-Talk
cd DICE-Talk && pip install -r requirements.txt

#Set up huggingface-cli and create "checkpoints" stuff for model to use
python3 -m pip install "huggingface_hub[cli]"

huggingface-cli download EEEELY/DICE-Talk --local-dir  "$DIRECTORY/DICE-Talk/checkpoints"
huggingface-cli download stabilityai/stable-video-diffusion-img2vid-xt --local-dir  "$DIRECTORY/DICE-Talk/checkpoints/stable-video-diffusion-img2vid-xt"
huggingface-cli download openai/whisper-tiny --local-dir "$DIRECTORY/DICE-Talk/checkpoints/whisper-tiny"
