import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from .models import TODO
from .forms import TODOForm, TODOModifyForm

class TestModelsTest(TestCase):
    def setUp(self):
        self.author = mommy.make(User)
        self.todo = mommy.make(
                TODO, 
                author=self.author
                )

    def test_whatever_creation(self):
        todo = self.todo
        self.assertIn(todo.status, ('i', 'c', 'e'))


class FormsTest(TestCase):
    def setUp(self):
        self.author = mommy.make(User)
        self.todo = mommy.make(
            TODO,
            author=self.author
        )

    def test_todo_form_due_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = TODOForm(data={
            'title': self.todo.title,
            'due_date': date,
            })
        self.assertFalse(form.is_valid())
    
    def test_todo_form_due_date_today(self):
        date = datetime.date.today()
        form = TODOForm(data={
            'title': self.todo.title,
            'due_date': date,
            })
        self.assertTrue(form.is_valid())

    def test_todo_modify_form_due_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = TODOForm(data={
            'title': self.todo.title,
            'due_date': date,
            })
        self.assertFalse(form.is_valid())
    
    def test_todo_modify_form_due_date_today(self):
        date = datetime.date.today()
        form = TODOForm(data={
            'title': self.todo.title,
            'due_date': date,
            })
        self.assertTrue(form.is_valid())
