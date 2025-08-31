from datasets import *
import numpy as np
import soundfile as sf
import json, opensmile


#Class to extract audio samples from CREMA-D/MELD datasets
class AudioExtraction:
	def __init__(self):
		#Features for CREMA-D dataset - file, audio, emotion, label
		self.dataset_CremaD = load_dataset('confit/cremad-parquet',data_files={"test":"data/test-00000-of-00001.parquet", "train":"data/train-00000-of-00001.parquet", "validation":"data/validation-00000-of-00001.parquet"})
		
		#Features for MELD dataset - file, audio, major_emotion (the rest aren't needed for this)
		MELD_URL = "https://huggingface.co/datasets/WiktorJakubowski/MELD-splits/resolve/main/data/"
		self.dataset_MELD = load_dataset('parquet', data_files={"test":[MELD_URL + x for x in ["test-00000-of-00006.parquet"]  ]})
		print(self.dataset_MELD)
	#Get split size for a given split in CREMA-D database
	def getSplitSize_CremaD(self, split):
		return self.dataset_CremaD[split]['num_rows']

	#Write audio from a given dataset+split to test/output.wav
	#dataset - CremaD, MELD, or MEAD
	#split - test, train, or validation
	#number - 1...n
	def writeAudio(self, dataset, split, number):
		audio = eval(f"self.dataset_{dataset}")[split].select(range(number))
		sampling_rate = audio['audio'][0]['sampling_rate']
		
		#Convert float format to PCM int-16 format
		sf.write("test/output.wav", audio['audio'][0]['array'], sampling_rate, subtype="PCM_16")
		#Return information abt filepath + emotion
		if dataset=="CreamaD": return (audio['file'][0].split("/")[::-1][0], audio['emotion'][0])
		elif dataset=="MELD": return (audio['file'][0], audio['major_emotion'][0])

	#Extract eGEMAPS features from a given audio
	def getEGMFeatures(audio_path = "test/output.wav"):

		#Read signal + sampling rate from audio file
		audio, sampling_rate = sf.read(audio_path)

		#Set up eGEMAPS parameter set
		GEMAPS_parameters = opensmile.Smile(feature_set = opensmile.FeatureSet.eGeMAPS, feature_level = opensmile.FeatureLevel.Functionals)

		#Extract GEMAPS parameters from an audio
		return GEMAPS_parameters.process_signal(audio, sampling_rate)


#Set up TH models

#Run experiments

	#Convert audio from DBs to TH videos

	#Analyze TH videos for arousal and AUs

	#Save to .csv file (include backup mechanism in case an error
	#randomly occurs during experimenting)



'''
#########
TESTING SPACE (to make sure stuff works)
#########
'''
audio = AudioExtraction()

file, emotion = audio.writeAudio("MELD", "test", 1)
print(emotion)