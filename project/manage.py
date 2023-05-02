#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('content', models.TextField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]

from django.contrib import admin

from .models import Article

admin.site.register(Article)

from django.apps import AppConfig

class BlogConfig(AppConfig):
    name = 'blog'

from django import forms

from .models import Article

class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields =[
            'title',
            'content',
            'active',
        ]

from django.db import models
from django.urls import reverse

class Article(models.Model):
    title   = models.CharField(max_length=120)
    content = models.TextField()
    active  = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("articles:article-detail", kwargs={"id": self.id})

from django.test import TestCase

from django.urls import path
from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
)

app_name = 'articles'
urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('<int:id>/', ArticleDetailView.as_view(), name='article-detail'),
    path('<int:id>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('<int:id>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]

from django.test import TestCase

from django.urls import path
from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
)

app_name = 'articles'
urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('<int:id>/', ArticleDetailView.as_view(), name='article-detail'),
    path('<int:id>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('<int:id>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]

class ArticleUpdateView(UpdateView):
    template_name = 'articles/article_create.html'
    form_class = ArticleModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ArticleDeleteView(DeleteView):
    template_name = 'articles/article_delete.html'
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Article, id=id_)

    def get_success_url(self):
        return reverse('articles:article-list')
    
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
    ]
    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
            ],
        ),
    ]

from django.contrib import admin

from django.apps import AppConfig

class CoursesConfig(AppConfig):
    name = 'courses'

from django import forms

from .models import Course

class CourseModelForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title'
        ]
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title.lower() == 'abc':
            raise forms.ValidationError("This is not a valid title")
        return title

from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=120)

from django.test import TestCase   

from django.urls import path
from .views import (
    CourseView,
    CourseListView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView
    # my_fbv
)

app_name = 'courses'
urlpatterns = [
    path('', CourseListView.as_view(), name='courses-list'),
    # path('', my_fbv, name='courses-list'),
    

    path('create/', CourseCreateView.as_view(), name='courses-create'),
    path('<int:id>/', CourseView.as_view(), name='courses-detail'),
    path('<int:id>/update/', CourseUpdateView.as_view(), name='courses-update'),
    path('<int:id>/delete/', CourseDeleteView.as_view(), name='courses-delete'),
]

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .forms import CourseModelForm
from .models import Course 
# BASE VIEW CLass = VIEW

class CourseObjectMixin(object):
    model = Course
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj 

class CourseDeleteView(CourseObjectMixin, View):
    template_name = "courses/course_delete.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('/courses/')
        return render(request, self.template_name, context)

class CourseUpdateView(CourseObjectMixin, View):
    template_name = "courses/course_update.html" # DetailView
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(Course, id=id)
        return obj

    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = CourseModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = CourseModelForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)
    
class CourseCreateView(View):
    template_name = "courses/course_create.html" # DetailView
    def get(self, request, *args, **kwargs):
        # GET method
        form = CourseModelForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # POST method
        form = CourseModelForm(request.POST)
        if form.is_valid():
            form.save()
            form = CourseModelForm()
        context = {"form": form}
        return render(request, self.template_name, context)

class CourseListView(View):
    template_name = "courses/course_list.html"
    queryset = Course.objects.all()

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset()}
        return render(request, self.template_name, context)

class CourseView(CourseObjectMixin, View):
    template_name = "courses/course_detail.html" # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)

    # def post(request, *args, **kwargs):
    #     return render(request, 'about.html', {})

# HTTP METHODS
def my_fbv(request, *args, **kwargs):
    print(request.method)
    return render(request, 'about.html', {})

from django.contrib import admin

from django.apps import AppConfig

class PagesConfig(AppConfig):
    name = 'pages'

from django.db import models

from django.test import TestCase

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs): # *args, **kwargs
    print(args, kwargs)
    print(request.user)
    #return HttpResponse("<h1>Hello World</h1>") # string of HTML code
    return render(request, "home.html", {})

def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})

def about_view(request, *args, **kwargs):
    my_context = {
        "title": "abc this is about us",
        "this_is_true": True,
        "my_number": 123,
        "my_list": [1313, 4231, 312, "Abc"],
        "my_html": "<h1>Hello World</h1>"

    }
    return render(request, "about.html", my_context)

def social_view(request, *args, **kwargs):
    return HttpResponse("<h1>Socail Page</h1>")

from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10000)),
                ('summary', models.TextField()),
            ],
        ),
    ]

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='summary',
            field=models.TextField(blank=True),
        ),
    ]

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20180702_2213'),
    ]
    operations = [
        migrations.AlterField(
            model_name='product',
            name='summary',
            field=models.TextField(),
        ),
    ]

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20180702_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]

