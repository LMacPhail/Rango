from django.shortcuts import render
from rango.models import Category, Page
from django.http import HttpResponse


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        #tries to find a category name slug with given name
        #if not found, raises a DoesNotExist exception
        # the .get() method returns one model instance or raises exception
        category = Category.objects.get(slug=category)

        #Retrieve all associated pages
        #filter() returns a list of page objects or empty list
        pages = Page.objects.filter(category=category)

        #adds result list to the template context under name pages
        context_dict['pages'] = pages
        #adds category from the database to context dictionary
        #this is used in the template to show that the category exists
        context_dict['category'] = category
    except Category.DoesNotExist:
        #this will happen if the specified category isn't found
        #template will display "no category" message
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)
