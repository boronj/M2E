from setuptools import setup, find_packages
setup(
	name = "m2e",
	version = "0.0.1",
	python_requires=">3",
	author = "Jacob Boron, Logan Garcia, Henry H., Arpandeep Khatua, Ethan Lu",
	install_requires = [
		"pandas==2.2.2",
		"opensmile",
		"tqdm",
		"soundfile",
		"ffmpeg",
		"datasets[audio]==4.0.0",
		"colorama",
		"numpy==2.0.0",
		"matplotlib==3.10.0",
		"h5py==3.14.0",
		"torchcodec==0.5.0"
	],
	packages=["m2e", "m2e.extract_audio", "m2e.analyze_video", "m2e.error_handling"],
	package_dir = {'':'src'},

)