from django.test import TestCase, Client
from django.urls import reverse
from .models import Task, Category
from .forms import TaskForm


class IndexViewTest(TestCase):
    """Test suite for index view"""

    def setUp(self):
        """Set up test data before each test method"""
        self.client = Client()
        self.url = reverse("index")
        self.category = Category.objects.create(name="Test Category", slug="test-category")

    def test_index_view_get_request(self):
        """Test GET request returns 200 and uses correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")

    def test_index_view_context_contains_form(self):
        """Test that context contains TaskForm instance"""
        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], TaskForm)

    def test_index_view_displays_todo_tasks(self):
        """Test that incomplete tasks appear in To Do section"""
        Task.objects.create(
            title="Incomplete Task",
            category=self.category,
            completed=False
        )
        response = self.client.get(self.url)
        self.assertContains(response, "Incomplete Task")

    def test_index_view_displays_done_tasks(self):
        """Test that completed tasks appear in Done section"""
        Task.objects.create(
            title="Completed Task",
            category=self.category,
            completed=True
        )
        response = self.client.get(self.url)
        self.assertContains(response, "Completed Task")

    def test_index_view_post_valid_form(self):
        """Test POST request with valid data creates task and redirects"""
        form_data = {
            "title": "New Task",
            "due_date": "2026-02-14",
            "category": self.category.id
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful POST
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_index_view_post_invalid_form(self):
        """Test POST request with invalid data returns form with errors"""
        form_data = {
            "title": "",  # Title is required, so this is invalid
            "due_date": "2026-02-14",
            "category": self.category.id
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        self.assertFalse(response.context["form"].is_valid())

    def test_index_view_post_missing_required_fields(self):
        """Test POST request missing required fields returns errors"""
        form_data = {
            "due_date": "2026-02-14",
            "category": self.category.id
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())

    def test_index_view_empty_todo_list(self):
        """Test rendering when no incomplete tasks exist"""
        response = self.client.get(self.url)
        self.assertContains(response, "No tasks to do!")

    def test_index_view_empty_done_list(self):
        """Test rendering when no completed tasks exist"""
        response = self.client.get(self.url)
        self.assertContains(response, "No completed tasks yet!")

    def test_index_view_csrf_token_present(self):
        """Test that CSRF token is present in form"""
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")