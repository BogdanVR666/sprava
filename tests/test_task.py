from pytest import fixture, raises, mark
from unittest.mock import patch, mock_open
from datetime import datetime

from ..task import Deadline, Task, TaskFile


class TestDeadline:
	init_values = [
		None,
		"2025-03-07",
		datetime(2027, 11, 4),
		]


	@mark.parametrize("input_value", init_values)
	def test_init(self, input_value):
		deadline = Deadline(input_value)


	def test_string_errors(self):
		with raises(ValueError):
			deadline = Deadline("invalid_date")


	@mark.parametrize("input_value", init_values)
	def test_date_is_datetime(self, input_value):
		deadline = Deadline(input_value)

		assert isinstance(deadline.date, datetime)


	@mark.parametrize("input_value", init_values)
	def test_done(self, input_value):
		deadline = Deadline(input_value)

		assert deadline.is_done == False

		deadline.done()

		assert deadline.is_done == True


class TestTask:
	init_values = [
		("Some text", Deadline(i)) for i in TestDeadline.init_values
	]
	without_deadline = [("Some text",)]


	@mark.parametrize("input_values", init_values)
	def test_init(self, input_values):
		task = Task(*input_values)

		assert task.text == "Some text"
		assert task.deadline == input_values[1]


	def test_init_without_deadline(self):
		task = Task("Some text")

		assert task.text == "Some text"
		assert task.deadline is None


	@mark.parametrize("input_values", init_values + without_deadline)
	def test_str(self, input_values):
		task = Task(*input_values)

		assert len(str(task).split("\t")) == 2


	@mark.parametrize("input_values", init_values + without_deadline)
	def test_bool(self, input_values):
		task = Task(*input_values)

		assert bool(task) == True

		if not task.deadline is None:
			task.deadline.done()

			assert bool(task) == False


class TestTaskFile:
	file_content = """\
1	Test1	someday
2	Test2	2025-06-22 07:24:19.344759
3	Test3	2025-03-07 00:00:00
"""


	def test_init(self):
		file = TaskFile(".todo")

		assert file.filename == ".todo"


	def test_write(self, tmp_path):
		test_file = tmp_path / "test_tasks.todo"
		taskfile = TaskFile(str(test_file))
		
		task_args = TestTask.init_values + TestTask.without_deadline

		tasks = [Task(*args) for args in task_args]

		taskfile.write(tasks)

		assert test_file.exists()


	@patch("builtins.open", mock_open(read_data=file_content))
	def test_read(self):
		file = TaskFile(".todo")
		tasks = file.read()

		for task in tasks:
			assert task.text.startswith("Test")
			if task.text[-1] == "1": 
				assert task.deadline is None
				continue
			assert task.deadline is not None

