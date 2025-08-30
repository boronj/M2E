from datasets import *
import numpy as np
import soundfile as sf
import json


#Class to extract audio samples from CREMA-D/MELD datasets
class AudioExtraction:
	def __init__(self):
		#Features for CREMA-D dataset - file, audio, emotion, label
		self.dataset_CremaD = load_dataset('confit/cremad-parquet',data_files={"test":"data/test-00000-of-00001.parquet", "train":"data/train-00000-of-00001.parquet", "validation":"data/validation-00000-of-00001.parquet"})
		
		#Features for MELD dataset - N/A
		#This DB is ~10GB and I haven't been able to download it personally, so IDK what the features are
		self.dataset_MELD = load_dataset("webdataset", data_files="https://web.eecs.umich.edu/~mihalcea/downloads/MELD.Raw.tar.gz", streaming=True)
		print(dataset_MELD)

	def getSplitSize_CremaD(self, split):
		return self.dataset_CremaD[split]['num_rows']

	def writeAudio_cremaD(self, split, number):
		audio = self.dataset_CremaD[split].select(range(number))
		sampling_rate = audio['audio'][0]['sampling_rate']
		#Convert float format to PCM int-16 format
		sf.write("test/output.wav", audio['audio'][0]['array'], sampling_rate, subtype="PCM_16")
		#Return information abt filepath, emotion & label
		return (audio['file'][0].split("/")[::-1][0], audio['emotion'][0], audio['label'][0])

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

filePath, emotion, label = audio.writeAudio_CremaD("train", 1) #Write second(?) training file to test/output.wav
print(filePath)
print(emotion)
print(label) 