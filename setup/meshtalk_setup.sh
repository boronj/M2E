###MeshTalk setup###

#Setup up CUDA 12.4
wget https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda_12.4.0_550.54.14_linux.run
chmod +x cuda_12.4.0_550.54.14_linux.run
sudo sh cuda_12.4.0_550.54.14_linux.run --silent --toolkit
nvcc --version #Keep in here for now

#Building ninja (used to install pytorch3d>=1.5)
pip install ninja

#Dependencies
pip uninstall py-feat -y
pip uninstall torch torchvision torchaudio -y
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124

#Installing PyTorch3D
pip install --upgrade setuptools wheel
pip install "git+https://github.com/facebookresearch/pytorch3d.git@stable" --no-build-isolation

#Installing MeshTalk & ffmpeg
git clone https://github.com/boronj/meshtalk
echo "A" | sudo wget https://github.com/facebookresearch/meshtalk/releases/download/pretrained_models_v1.0/pretrained_models.zip -O /content/PTM.zip --no-check-certificate --continue
unzip /content/PTM.zip -d /content/meshtalk_models
export PYTHONPATH=/content/
  #Uninstall & reinstall ffmpeg for good measure
python -m pip uninstall ffmpeg-python -y
python -m pip uninstall ffmpeg -y
python -m pip install ffmpeg-python
