from background_task import background
from background_task.models import Task
from .processors.main import process


@background(schedule=0)
def process_students():
	process("part", ["students"])


@background(schedule=0)
def process_subjects():
	process("part", ["subjects"])


@background(schedule=0)
def process_assessments():
	process("assessments")


@background(schedule=0)
def process_results():
	process("results")


@background(schedule=0)
def process_full():
	process("full", ["subjects", "students"])
	process("assessments")
	process("results")
	

# if not Task.objects.filter(verbose_name="process_full_sync").exists():
	# process_full_sync(repeat=Task.DAILY, verbose_name="process_full_sync", repeat_until=None)
