# this converts a zst file to csv
#
# it's important to note that the resulting file will likely be quite large
# and you probably won't be able to open it in excel or another csv reader
#
# arguments are inputfile, outputfile, fields
# call this like
# python to_csv.py wallstreetbets_submissions.zst wallstreetbets_submissions.csv author,selftext,title

import zstandard
import os
import json
import sys
import csv
from datetime import datetime
import logging.handlers


# put the path to the input file
input_file_path = r"/home/ashagaire/Desktop/Python projects/Reddit_Scraping/data/Suomi_comments.zst"
# put the path to the output file, with the csv extension
output_file_path = r"/home/ashagaire/Desktop/Python projects/Reddit_Scraping/data/Suomi_comments.csv"
# if you want a custom set of fields, put them in the following list. If you leave it empty the script will use a default set of fields
fields = []
# specify the number of lines per chunk file
lines_per_file = 100000

log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
	chunk = reader.read(chunk_size)
	bytes_read += chunk_size
	if previous_chunk is not None:
		chunk = previous_chunk + chunk
	try:
		return chunk.decode()
	except UnicodeDecodeError:
		if bytes_read > max_window_size:
			raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
		return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)


def read_lines_zst(file_name):
	with open(file_name, 'rb') as file_handle:
		buffer = ''
		reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
		while True:
			chunk = read_and_decode(reader, 2**27, (2**29) * 2)
			if not chunk:
				break
			lines = (buffer + chunk).split("\n")

			for line in lines[:-1]:
				yield line, file_handle.tell()

			buffer = lines[-1]
		reader.close()


if __name__ == "__main__":
	if len(sys.argv) >= 3:
		input_file_path = sys.argv[1]
		output_file_path = sys.argv[2]
		fields = sys.argv[3].split(",")

	is_submission = "submission" in input_file_path
	if not len(fields):
		if is_submission:
			fields = ["title", "score", "text", "url"]  # Removed "created"
		else:
			fields = ["score", "body"]  # Removed "created"

	file_size = os.stat(input_file_path).st_size
	file_lines, bad_lines = 0, 0
	line, created = None, None
	file_count = 0

	def get_output_file():
		global file_count
		file_count += 1
		return open(f"{output_file_path.rsplit('.', 1)[0]}_{file_count}.csv", "w", encoding='utf-8', newline="")

	output_file = get_output_file()
	writer = csv.writer(output_file)
	writer.writerow(fields)

	try:
		for line, file_bytes_processed in read_lines_zst(input_file_path):
			try:
				obj = json.loads(line)
				output_obj = []
				for field in fields:
					if field == "text":
						if 'selftext' in obj:
							value = obj['selftext']
						else:
							value = ""
					else:
						value = obj.get(field, "")

					output_obj.append(str(value).encode("utf-8", errors='replace').decode())
				
				# Update the created timestamp for logging
				created = datetime.utcfromtimestamp(int(obj['created_utc']))
				
				writer.writerow(output_obj)
			except json.JSONDecodeError as err:
				bad_lines += 1
				log.error(f"JSON decode error: {err} on line: {line}")
			except KeyError as err:
				log.error(f"Missing key: {err} in line: {line}")
			except Exception as err:
				log.error(f"Unexpected error: {err} on line: {line}")

			file_lines += 1
			if file_lines % lines_per_file == 0:
				output_file.close()
				output_file = get_output_file()
				writer = csv.writer(output_file)
				writer.writerow(fields)
			if file_lines % 100000 == 0:
				log.info(f"{created.strftime('%Y-%m-%d %H:%M:%S')} : {file_lines:,} : {bad_lines:,} : {(file_bytes_processed / file_size) * 100:.0f}%")
	except Exception as err:
		log.error(f"Critical error: {err}")
	finally:
		output_file.close