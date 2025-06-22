from pytest import fixture, raises, mark
from datetime import datetime

from ..task import Deadline, Task, TaskFile


class TestDeadline:

	init_values = [
		None,
		"2025-03-07",
		datetime(2027, 11, 4),
		]

	# === Unit tests ===

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
	# Fixtures
	pass
	# Unit tests


class TestTaskFile:
	# Fixtures
	pass
	# Unit tests


class TestTaskList:
	# Fixtures
	pass
	# Unit tests



