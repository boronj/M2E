import os, csv, json, subprocess, sys, gspread, ffmpeg
from colorama import Fore, Style #Color styles for error messaging
from google.colab import auth#, drive #Mounting for Google Drive
from google.auth import default
import pandas as pd
ROOT_DIRECTORY = "/content"
MODEL = "MeshTalk"
DATASET = "CREMA-D"
SPLIT = "test"
NUMBER = 5
EGM_total = []
consensus_emotions = []

#Initialize M2E
def M2E_init():
  if f"{ROOT_DIRECTORY}/M2E/src" not in sys.path:
    sys.path.append(f"{ROOT_DIRECTORY}/M2E/src/") #Include this b/c the "editable project" points to this location
  from m2e import *

#Create folders for generated videos
def createFolders():
  global outputs_gemaps_path
  global output_path
  global output_video_path
  output_gemaps_path = f"{ROOT_DIRECTORY}/GEMAPS_tables/{MODEL}/{DATASET}_{SPLIT}"
  output_path = f"{ROOT_DIRECTORY}/data/{MODEL}/{DATASET}_{SPLIT}".replace("-", "_")
  output_video_path = f"{ROOT_DIRECTORY}/data/outputs/{MODEL}/{DATASET}_{SPLIT}/".replace("-", "_")
  os.makedirs(output_gemaps_path, exist_ok=True)
  os.makedirs(output_path, exist_ok=True)
  os.makedirs(output_video_path, exist_ok=True)

#Set required environment variables for CUDA and ffmpeg
def setEnvVariables():
  os.environ["FFMPEG_BINARY"] = '/usr/bin/ffmpeg'
  #os.environ['CUDA_HOME'] = '/usr/local/cuda-12.4'
  #os.environ['PATH'] = '/usr/local/cuda-12.4/bin:' + os.environ['PATH']
  #os.environ['LD_LIBRARY_PATH'] = '/usr/local/cuda-12.4/lib64:' + os.environ['LD_LIBRARY_PATH']

#Set to 0 to get all audios in a split
def selectSnippetRange(number=0):
  global section
  section = dataset[DATASET]
  if number == 0:
    number = len(section[SPLIT])
  section = section[SPLIT].select(range(0,number))


#Write audio file to a audio object's filepath 
def write_audio(audioObj):
  print(audioObj['audio']['path'])
  if not os.path.exists(f"{output_path}/{audioObj['audio']['path']}"):
    open(f"{output_path}/{audioObj['audio']['path']}", "w") # Not using this to write to the file, just to create it.
  metadata = extract_audio(audioObj, f"{output_path}/{audioObj['audio']['path']}", DATASET)
  consensus_emotions.append(metadata[2])
  print(f"Wrote {Fore.YELLOW}{metadata[0]}{Style.RESET_ALL} to {Fore.YELLOW}{output_path}/{audioObj['audio']['path']}{Style.RESET_ALL}")


M2E_init()
setEnvVariables()
selectSnippetRange(NUMBER)

for x in section:
  #Write audio to an output path
  write_audio(x)

  #Map eGEMAPS features for given audio
  EGM_features = extract_EGM_parameters(f"{output_path}/{x['audio']['path']}")
  EGM_features.to_csv(f"{output_gemaps_path}/{x['audio']['path'].replace(".wav","_1.csv")}", index=False)
  EGM_total.append(EGM_features)

  #Call MeshTalk model
  try:
    path_ = f"{output_video_path}{x['audio']['path'].replace(".wav",".mp4")}"
    k = subprocess.run([sys.executable, "/content/meshtalk/animate_face.py", "--model_dir", "/content/meshtalk_models/pretrained_models/", "--audio_file", f"{output_path}/{x['audio']['path']}", "--face_template", "/content/meshtalk/assets/face_template.obj", "--output", f"{path_}"], capture_output=True, text=True)
  except Exception as e:
    raise e
  else:
    if k.stderr is not None and "Warning:" not in k.stderr:
      print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {k.stderr}")
      sys.exit(1)
    elif k.returncode != 0:
      print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} failed to run {Fore.YELLOW}/meshtalk/animate_face.py{Style.RESET_ALL}")
      print(k.stderr)
    else:
      #Re-encode outputted video using ffmpeg
      new_path = f"{output_video_path}{x['audio']['path'].replace(".wav","_1.mp4")}"
      ffmpeg.input(path_).output(new_path).run(overwrite_output=True)
      os.remove(path_)
      print(k.returncode)
      print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {Fore.YELLOW}animate_face.py{Style.RESET_ALL} executed on {Fore.YELLOW}{output_path}/{x['audio']['path']}{Style.RESET_ALL}")
