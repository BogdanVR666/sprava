from datetime import datetime, timezone
from pathlib import Path


class Deadline:
	_ZERO_DAY = datetime(1970, 1, 1, tzinfo=timezone.utc)


	def __init__(self, date: datetime = datetime.now()):
		self.date = date


	def done(self) -> None:
		self.date = Deadline._ZERO_DAY


	def is_done(self) -> bool:
		return self.date == Deadline._ZERO_DAY 


class Task:
	def __init__(self, text: str, deadline: Deadline|None = None):
		self.text = text
		self.deadline = deadline


	def __bool__(self) -> bool:
		return bool(bool(self.text) \
			+ bool(self.deadline))


class TaskFile:
	def __init__(self, filename: str):
		self.filename = filename
		Path(filename).touch() # creates file if not exists 


	def write_task(self, task: Task) -> None:
		with open(self.filename, "a") as file:
			file.write(str(task))


	def read(self) -> list[Task]:
		result = list()
		with open(self.filename, "r") as file:
			for row in file:
				args = row.strip().split("\t")[1:]
				result.append(Task(args[0], Deadline()))
		return result


class TaskList:
	def __init__(self, file: TaskFile = TaskFile(".todo")):
		self.file = file
		self.tasks = file.read()


	def append(self, task: Task) -> None:
		if task not in self.tasks:
			self.tasks.append(task)


	def remove(self, task: Task) -> None:
		self.tasks.remove(task)


	def upload(self) -> None:
		if self.file:
			for task in self.tasks:
				self.file.write_task(task)



