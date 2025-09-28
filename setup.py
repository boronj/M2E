from setuptools import setup, find_packages
setup(
	name = "m2e",
	version = "0.0.1",
	author = "Jacob Boron, Logan Garcia, Henry H., Arpandeep Khatua, Ethan Lu",
	install_requires = [
		"py-feat",
		"pandas==2.3.0",
		"tqdm",
		"soundfile",
		"ffmpeg",
		"datasets",
		"colorama",
		"numpy>=2.0.0",
		"nvidia-nccl-cu12==2.27.3",
		"matplotlib==3.10.0",
		"h5py==3.14.0"
	],
	packages=["m2e"],
	package_dir = {'m2e':'src/m2e/'},

	py_modules=['m2e', 'm2e.extract_audio', 'm2e.analyze_video', 'm2e.error_handling']
)