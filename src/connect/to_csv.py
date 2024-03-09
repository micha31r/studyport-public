import os, json, csv
from pathlib import Path
from django.conf import settings
from treelib import Node, Tree

class Converter():
	def __init__(self):
		self.directory = settings.KAMAR_CACHE_ROOT
		self.filename = "*.json"
		self.source_paths = []
		self.counter = -1
		self.target_name = "data"

	def build_tree(self, data, parent=None):
		if parent == None:
			parent = self.filename

		for k, v in data.items():
			self.tree.create_node(k + " (*)" if k == self.target_name else k, k, parent=parent)
			if type(v) == dict:
				self.build_tree(v, parent=k)

	def get_obj(self, data, counter=-1):
		for k, v in data.items():
			counter += 1
			if k == self.target_name:
				return v
			if type(v) == dict:
				return self.get_obj(v, counter=counter)

		return None

	def get_file_data(self, index=None):
		data = []
		paths = Path(self.directory).rglob(self.filename)
		for path in paths:
			with open(path, "r") as f:
				try:
					data.append(json.loads(f.read()))
					self.source_paths.append(str(path))
				except: pass

		return data

	def convert(self):
		self.tree = Tree()
		self.tree.create_node(f"\"{self.filename}\"", self.filename)
		self.build_tree(self.get_file_data(0)[0])
		self.tree.show()

		for index, data in enumerate(self.get_file_data()):
			data = self.get_obj(data)

			current_path = self.source_paths[index]
			new_base_directory = Path(self.directory + "_csv")
			path = str(new_base_directory) + ".".join(current_path.replace(self.directory, "").split(".")[:-1]) + ".csv"
			os.makedirs(os.path.dirname(path), exist_ok=True)

			with open(path, "w") as f:
				if type(data) == list:
					writer = csv.DictWriter(f, data[0].keys())
					counter = 0
					for obj in data[1:]:
						if counter == 0:
							# Writing headers
							writer.writeheader()
							counter += 1
						# Writing body
						writer.writerow(obj)

				elif type(data) == dict:
					writer = csv.DictWriter(f, data.keys())
					# Writing headers
					writer.writeheader()
					writer.writerow(obj.values())

				f.close()

Converter().convert()



