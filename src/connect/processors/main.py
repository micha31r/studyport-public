import os, glob, json, logging
from django.conf import settings
from connect.processors import assessment, results, student, subject


logger = logging.getLogger(__name__)

PROCESSORS = {
	"subjects": 	subject,
	"assessments": 	assessment,
	"results": 		results,
	"students": 	student,
}


def process(save_path, data_names=[]):
	if not data_names:
		data_names = [save_path]

	paths = glob.glob(os.path.join(settings.KAMAR_CACHE_ROOT, save_path, "*.json"))
	for path in paths:
		with open(path, 'r+') as f:
			try:
				data = json.loads(f.read())["SMSDirectoryData"]
			except Exception as e:
				logger.error(f"{e}: path={path} (skipped)")
				continue

			success = False
			for name in data_names:
				if name in data:
					try:
						success, unsynced_data = PROCESSORS[name].run(data)
						data[name] = unsynced_data
					except Exception as e:
						logger.critical(f"{e} path={path} processor={name}")

			if not success:
				# Update file with unsynced data
				f.seek(0)
				f.truncate(0)
				json.dump({"SMSDirectoryData": data}, f, indent=4)

		if success:
			# Delete data file if sync is 100% succesfull
			os.remove(path)




