#Other dependencies
from datasets import *
from m2e.error_handling import throw_error
from colorama import Fore, Style
import numpy as np
import soundfile as sf
import json, argparse, opensmile, sys 

#Set up audio DBs
MELD_URL = "https://huggingface.co/datasets/WiktorJakubowski/MELD-splits/resolve/main/data/"

dataset = {
	"CREMA-D": load_dataset('confit/cremad-parquet', data_files={
		"test":"data/test-00000-of-00001.parquet",
		"train":"data/train-00000-of-00001.parquet",
		"validation":"data/validation-00000-of-00001.parquet"
		}).cast_column("audio", Audio()),
	"MELD": load_dataset('parquet', data_files={
		"test": [MELD_URL + x for x in [
			"test-00000-of-00006.parquet"
		]]
		}).cast_column("audio", Audio())
	#MEAD?
}


def get_dataset():
	return dataset

#Get length of a dataset
def get_length(set_, split):
	return len(dataset[set_][split])

#Extract eGeMAPS parameters from an audio file
def extract_EGM_parameters(audio_path):
	audio, sampling_rate = sf.read(audio_path)

	GEMAPS_parameters = opensmile.Smile(feature_set = opensmile.FeatureSet.eGeMAPSv01a, feature_level = opensmile.FeatureLevel.Functionals)
	return GEMAPS_parameters.process_signal(audio, sampling_rate)

#Return tuple containing filepath, dataset + emotion
def extract_audio(set_, split, number, output_file):

	#Extract audio & sampling rate 
	audio = dataset[set_][split].select(range(number))
	#print(audio['audio'])
	#print("\n")
	sampling_rate = audio['audio'][0]['sampling_rate']

	#Convert float format to PCM int-16 format
	sf.write(output_file, audio['audio'][0]['array'], sampling_rate, subtype="PCM_16")
	#Return information abt filepath, audio information + emotion
	#NP array doesn't have to be put in here as wav2vec will be used
	#to extract audio
	audioTuple = (audio['file'][0], set_, )
	print(audioTuple)
	if dataset=="CreamaD": return audioTuple + (audio['emotion'][0],)
	elif dataset=="MELD": return audioTuple + (audio['major_emotion'][0],)

def main():
	#Set up argument parser using argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--db", type=str)
	parser.add_argument("--split", type=str)
	parser.add_argument("--number", type=int)
	parser.add_argument("--output_path", type=str, default="../data/output.wav")
	args = parser.parse_args()
	print(args)


	#Write & extract audio given CL args
	try:
		audioInfo = extract_audio(args.db, args.split.lower(), args.number, args.output_path)
	except Exception as e:
		throw_error(e, f"failed to write {args.db}[`{args.split.lower()}`], #{args.number} to {Fore.YELLOW}{args.output_path}{Style.RESET_ALL}")
	else:
		print(f"{Fore.GREEN}[SUCCESS]{STYLE.RESET_ALL} audio information written to {Fore.YELLOW}{args.output_path}{Style.RESET_ALL}: {args.db}[`{args.split.lower()}`], #{args.number}")

if __name__ == "__main__":
	main()