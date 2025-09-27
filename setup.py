from setuptools import setup, find_packages
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
		"numpy",
		"nvidia-nccl-cu12==2.27.3"
	],
	package_dir = {'':'src'},
	packages=['m2e.extract_audio', 'm2e.analyze_video', 'm2e.error_handling']
)