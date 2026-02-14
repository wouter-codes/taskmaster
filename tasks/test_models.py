from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Task, Category


class TaskModelTest(TestCase):
    """Test suite for Task model"""

    def setUp(self):
        """Set up test data before each test method"""
        self.category = Category.objects.create(name="Test Category")
        self.task = Task.objects.create(
            title="Test Task",
            category=self.category,
            due_date="2026-02-14",
            completed=False
        )

    def test_task_creation(self):
        """Test creating a task with all fields"""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.category, self.category)
        self.assertEqual(self.task.due_date, "2026-02-14")
        self.assertFalse(self.task.completed, False)

    def test_task_string_representation(self):
        """Test the __str__ method returns task title"""
        self.assertEqual(str(self.task), "Test Task")

    def test_task_default_completed_status(self):
        """Test that completed defaults to False"""
        self.assertFalse(self.task.completed)

    def test_task_with_category(self):
        """Test task association with category"""
        self.assertEqual(self.task.category.name, "Test Category")

    def test_task_without_due_date(self):
        """Test creating a task without due_date (null allowed)"""
        task_no_due = Task.objects.create(
            title="Task without due date",
            category=self.category,
            completed=False
        )
        self.assertIsNone(task_no_due.due_date)       

    def test_category_related_name(self):
        """Test accessing tasks through category.tasks"""
        tasks = self.category.tasks.all()

    # generate a unit test that checks for an error if the title is longer than 100 characters
    def test_task_title_length(self):
        """Test that creating a task with a title longer than 100 characters raises an error"""
        long_title = "A" * 101  # 101 characters
        with self.assertRaises(ValidationError):
            Task.objects.create(
                title=long_title,
                category=self.category,
                due_date="2026-02-14",
                completed=False
            )