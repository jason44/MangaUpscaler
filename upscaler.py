from PIL import Image
from pathlib import Path
import os
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser(description="directories and quality")
parser.add_argument('-i', '--input', type=str, help="Path to the input directory")
parser.add_argument('-o', '--output', type=str, help="Path to the output directory")
parser.add_argument('-q', '--quality', type=int, help="Quality of the upscaled image")
args = parser.parse_args()

in_dir = args.input
out_dir = args.output
quality = args.quality

def compress(in_path, out_path, quality):
	try:
		with Image.open(in_path) as img:
			#img.save(out_path, "JPEG", optimize=True, quality=quality)
			#img.save(out_path, optimize=True, compression_level=9)
			img.save(out_path, optimize=True, quality=quality)
		print(f"{out_path}")
		print("compressed!")
	except Exception as e:
		print(f"ERROR: {str(e)}")

def split(string):
	return string.replace(' ', '\ ')

def browse_directory(_dir):
	manga = Path(_dir)
	for chapter in manga.iterdir():
		if chapter.is_dir():
			for page in chapter.iterdir():
				if page.is_file():
					ftype = page.suffix[1:].lower()
					if ftype == "jpg" or ftype == "jpeg" or ftype == "png" or ftype == "webp":
						# PIL wants to escape spaces by itself, Path also seems to want to use unescaped paths
						out_file_unsplit = f"{out_dir}{chapter.name}/{page.with_suffix('.webp').name}"
						if Path(out_file_unsplit).exists():
							print(f"skipping {out_file_unsplit}")
							continue
						try:
							out_file = f"{out_dir}{split(chapter.name)}/{split(page.with_suffix('.webp').name)}"	
							command = f"./realesrgan-ncnn-vulkan -i {split(str(page.resolve()))} -o {out_file} -s 2 -f webp"
							print(out_file)
							output = subprocess.check_output(command, shell=True, universal_newlines=True)
						except subprocess.CalledProcessError as e:
							print(f"{e}")
						compress(out_file_unsplit, out_file_unsplit, quality)
				else: 
					print(f"{page} is not a jpeg image")
		else:
			print(f"{chapter} is not a directory")


browse_directory(in_dir)
