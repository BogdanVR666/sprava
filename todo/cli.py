"""CLI for task tracking. All CLI operations are here"""
import click
from rich.table import Table
from rich.console import Console
from rich import box
from .task import Task, TaskFile


console = Console()

todo_filename = ".todo"
done_filename = ".done"


@click.group()
def cli(): pass


@cli.command()
@click.argument("text")
@click.option("--deadline", default=None, help="deadline in ISO format")
def add(text, deadline):
	task = TaskFile(todo_filename).add(Task(text, deadline))
	console.print("Task Writed" if task else "Nothing to add")


@cli.command()
@click.option(
	"--recursive", 
	is_flag=True, 
	help="recursive show in subdirectories",
)
def list(recursive):
	if not recursive:
		tasks = TaskFile(todo_filename).read()

		if tasks == []: 
			console.print("Nothing to do!")
			return None

		table = Table(
			"ID", "Task", "Deadline", 
			title="Tasks in .",
			box=box.ASCII,
		)

		for task in tasks:
			table.add_row(*str(task).strip().split("\t"))

		console.print(table)


@cli.command()
@click.option("--id", help="index of task to done")
def done(**kwargs):
	task_id = int(kwargs.get("id"))
	tasks = TaskFile(todo_filename)
	dones = TaskFile(done_filename)
	for task in tasks.read():
		if task.task_id == task_id:
			dones.add(task)
			tasks.remove(task_id)
			console.print("Task done")
			break


@cli.command()
@click.option("--id", help="index of task to remove")
def remove(**kwargs):
	task_id = int(kwargs.get("id"))
	tasks = TaskFile(todo_filename)
	for task in tasks.read():
		if task.task_id == task_id:
			tasks.remove(task_id)
			console.print("Task removed")
			break
	else:
		console.print(f"Task with id {task_id} not found")



if __name__ == "__main__": cli()