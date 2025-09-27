from setuptools import setup
setup(
	name = "m2e",
	version = "0.0.1",
	author = "Jacob Boron, Logan Garcia, Henry H., Arpandeep Khatua, Ethan Lu",
	install_requires = [
		"py-feat",
		"pandas",
		"tqdm",
		"soundfile",
		"ffmpeg",
		"datasets",
		"colorama",
		"numpy==2.0",
		"contourpy>=1.3", #Attempts to fix dependency clashes from here below
		"matplotlib>=3.10",
		"nvidia-nccl-cu12==2.27.3"
	],
	package_dir = {"":"src"},
	packages=find_packages(where="src"),
)