"""API for all task operations - lists of tasks, task files etc."""
from datetime import datetime, timezone
from typing import Self


class Deadline:
	# self.date завжди має бути type(datetime)
	_ZERO_DAY = datetime(1970, 1, 1, tzinfo=timezone.utc)


	def __init__(self, date: datetime|str|None = None):
		if isinstance(date, datetime):
			self.date = date
		elif isinstance(date, str):
			self.date = datetime.fromisoformat(date)
		elif date is None:
			self.date = datetime.now()
	

	def __str__(self) -> str:
		return str(self.date)


	def done(self) -> Self:
		self.date = Deadline._ZERO_DAY
		return self


	@property
	def is_done(self) -> bool:
		return self.date == Deadline._ZERO_DAY 


class Task:
	def __init__(self, text: str, deadline: Deadline|None = None):
		self.text = text
		self.deadline = deadline


	def __str__(self) -> str:
		return f"{self.text}\t{str(self.deadline or 'someday')}"


	def __bool__(self) -> bool:
		# AttributeError тут бути не може
		return self.deadline is None or not self.deadline.is_done


class TaskFile:
	def __init__(self, filename: str):
		"""TaskFile(".todo")"""
		self.filename = filename


	def write(self, task_list: list[Task]) -> None:
		"""
		TaskFile(name).write([Task(...), Task(...), ...]) -> file with tasks
		"""

		with open(self.filename, "w") as file:
			for index, task in enumerate(task_list, 1):
				file.write(str(index) + "\t" + str(task) + "\n")


	def read(self) -> list[Task]:
		"""TaskFile(name).read() -> [Task(...), Task(...), ...]"""

		result = list()
		with open(self.filename, "r") as file:
			for row in file:
				args = row.strip().split("\t")[1:]
				if args[1] != "someday":
					result.append(Task(args[0], Deadline(args[1])))
				else:
					result.append(Task(args[0]))
		return result
