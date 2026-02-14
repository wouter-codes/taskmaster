from django.test import TestCase
from .models import Category, Task
from .forms import TaskForm


class TaskFormTest(TestCase):
    """Test suite for TaskForm"""

    def setUp(self):
        """Set up test data before each test method"""
        self.category = Category.objects.create(name="Test Category", slug="test-category")

    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            "title": "Test Task",
            "due_date": "2026-02-14",
            "category": self.category.id
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_title(self):
        """Test form missing required title field"""
        form_data = {
            "due_date": "2026-02-14",
            "category": self.category.id
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_missing_category(self):
        """Test form missing required category field"""
        form_data = {
            "title": "Test Task",
            "due_date": "2026-02-14"
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)

    def test_form_save_creates_task(self):
        """Test that form.save() creates a Task object"""
        form_data = {
            "title": "Test Task",
            "due_date": "2026-02-14",
            "category": self.category.id
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.category, self.category)
        self.assertEqual(str(task.due_date.date()), "2026-02-14")
        self.assertFalse(task.completed)

    def test_form_date_input_type(self):
        """Test that due_date input type is date"""
        form = TaskForm()
        self.assertIn("type=\"date\"", str(form["due_date"]))
