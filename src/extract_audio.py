from datasets import *
import numpy as np
import soundfile as sf
import json

MELD_URL = "https://huggingface.co/datasets/WiktorJakubowski/MELD-splits/resolve/main/data/"

dataset = {
	"CREMA-D": load_dataset('confit/cremad-parquet', data_files={
		"test":"data/test-00000-of-00001.parquet",
		"train":"data/train-00000-of-00001.parquet",
		"validation":"data/train-00001.parquet"
		}),
	"MELD": load_dataset('parquet', data_files={
		"test": [MELD_URL + x for x in [
			"test-00000-of-00006.parquet"
		]]
		})
	#MEAD?
}

#Return tuple containing filepath, dataset + emotion
def extractAudio(set_, split, number):

	#Extract audio & sampling rate 
	audio = dataset[set_][split].select(range(number))
	sampling_rate = audio['audio'][0]['sampling_rate']

	#Convert float format to PCM int-16 format
	sf.write("../data/output.wav", audio['audio'][0]['array'], sampling_rate, subtype="PCM_16")
	#Return information abt filepath, audio information + emotion
	#NP array doesn't have to be put in here as wav2vec will be used
	#to extract audio
	audioTuple = (audio['file'][0], set_, )

	if dataset=="CreamaD": return  audioTuple + (audio['emotion'][0],)
	elif dataset=="MELD": return audioTuple + (audio['major_emotion'][0],)