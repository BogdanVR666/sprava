"""API for all task operations - lists of tasks, task files etc."""
from datetime import datetime, timezone
from typing import Self


class Task:
	_ZERO_DAY = datetime(1970, 1, 1, tzinfo=timezone.utc)


	def __init__(
			self, text: str, 
			deadline: datetime|str|None = None,
			task_id: int = 1,
		):
		self.text = text
		self.task_id = task_id

		if isinstance(deadline, datetime):
			self.deadline = deadline
		elif isinstance(deadline, str):
			self.deadline = datetime.fromisoformat(deadline)
		elif deadline is None:
			self.deadline = None


	def __str__(self) -> str:
		if self.deadline and sum(tuple(self.deadline.timetuple())[3:6]):
			date = str(self.deadline)
		elif self.deadline:
			date = str(self.deadline).split()[0]
		else:
			date = "someday"

		return f"{self.task_id}\t{self.text}\t{date}"


	def __bool__(self) -> bool:
		# AttributeError тут бути не може
		return self.deadline is None or not self.is_done


	def done(self) -> Self:
		self.deadline = Task._ZERO_DAY
		return self


	@property
	def is_done(self) -> bool:
		return self.deadline == Task._ZERO_DAY 


class TaskFile:
	def __init__(self, filename: str):
		"""TaskFile(".todo")"""
		self.filename = filename


	def write(self, task_list: list[Task]) -> None:
		"""
		TaskFile(name).write([Task(...), Task(...), ...]) -> file with tasks
		"""

		with open(self.filename, "w") as file:
			for task in task_list:
				file.write(str(task) + "\n")


	def read(self) -> list[Task]:
		"""TaskFile(name).read() -> [Task(...), Task(...), ...]"""

		result = list()
		try:
			with open(self.filename, "r") as file:
				for row in file:
					args = row.strip().split("\t")
					if args[2] != "someday":
						task = Task(
							args[1],
							datetime.fromisoformat(args[2]),
							task_id = int(args[0]),
						)
					else:
						task = Task(args[1], task_id = int(args[0]))
					result.append(task)
		except FileNotFoundError: pass
		return result


	def add(self, task: Task) -> Task|None:
		"""TaskFile(name).add(Task(...)) -> add task to end or do nothing"""
		
		tasks = self.read()

		for i in tasks:
			if task.text == i.text:
				return None

		with open(self.filename, "a") as file:
			task_edit = Task(task.text, task.deadline, task_id=len(tasks)+1)
			file.write(str(task_edit) + "\n")
			return task_edit


	def remove(self, task_id: int) -> None:
		"""TaskFile(name).remove(int) -> removes task from file"""
		tasks = self.read()

		for i in tasks:
			if task_id == i.task_id:
				tasks.remove(i)
				self.write(tasks)
				break