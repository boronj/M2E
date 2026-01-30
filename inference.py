import os, csv, json, subprocess, sys, gspread, ffmpeg
from colorama import Fore, Style #Color styles for error messaging
from google.colab import auth#, drive #Mounting for Google Drive
from google.auth import default
import pandas as pd
DIRECTORY = "/content"
MODEL = "MeshTalk"
DATASET = "CREMA-D"
SPLIT = "test"
PATH = os.path.join(DIRECTORY, f"\'My Drive\'/output_spreadsheets/{MODEL}", f"{DATASET}_{SPLIT}_metadata.gsheet")
print(PATH)

###These depend on the analysis section being done###

#Grab CSV data from spreadsheet & convert to JSON data
###MAKE SURE THE KEYS FOR JSON DATA MATCH THAT FOR THE FILE###
def getCSVData(file_path, keys):
  csv_reader = None
  try:
    if file_path.split(".")[1] == "csv": #CSV file
      with open(file_path, mode='r') as file:
          csv_reader = csv.reader(file)
    else: #Google Sheet file
        #Access using GSpread and convert to CSV using some trickery
        a=0
  except Exception as e:
    throw_error(e, f"failed to open {Fore.YELLOW}{file_path}{Style.RESET_ALL}")
  else:
    return [
        {x: data} for x in keys for data in row for row in csv_reader
    ]


#Write data to CSV file
def writeCSVData(file_path, JSON_data):
  with open(file_path, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([result[x] for x in JSON_data.keys()])

if f"{directory}/M2E/src" not in sys.path:
  sys.path.append(f"{directory}/M2E/src/") #Include this b/c the "editable project" points to this location
from m2e import *
crema_d = dataset['CREMA-D']

print(crema_d)
#spreadsheet = getCSVData(PATH, ['file', 'emotion'])
#`datasets` is 1-index so start from the one after that
#lastFile = len(spreadsheet)+1
snippets = crema_d[SPLIT].select(range(0,5)) #First 5 entries in CREMA-D dataset
print(snippets)

#os.environ['CUDA_HOME'] = '/usr/local/cuda-12.4'
#os.environ['PATH'] = '/usr/local/cuda-12.4/bin:' + os.environ['PATH']
#os.environ['LD_LIBRARY_PATH'] = '/usr/local/cuda-12.4/lib64:' + os.environ['LD_LIBRARY_PATH']

EGM_total = []
consensus_emotions = []

os.environ["FFMPEG_BINARY"] = '/usr/bin/ffmpeg'
output_gemaps_path = f"/content/GEMAPS_tables/{MODEL}/{DATASET}_{SPLIT}"
output_path = f"/content/data/{MODEL}/{DATASET}_{SPLIT}".replace("-", "_")
output_video_path = f"/content/data/outputs/{MODEL}/{DATASET}_{SPLIT}/".replace("-", "_")
os.makedirs(output_gemaps_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)
os.makedirs(output_video_path, exist_ok=True)
for x in snippets:
  #Write audio to an output path
  print(x['audio']['path'])
  if not os.path.exists(f"{output_path}/{x['audio']['path']}"):
    open(f"{output_path}/{x['audio']['path']}", "w") # Not using this to write to the file, just to create it.
  metadata = extract_audio(x, f"{output_path}/{x['audio']['path']}", DATASET)
  consensus_emotions.append(metadata[2])
  print(f"Wrote {Fore.YELLOW}{metadata[0]}{Style.RESET_ALL} to {Fore.YELLOW}{output_path}/{x['audio']['path']}{Style.RESET_ALL}")

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
