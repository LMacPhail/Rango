from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    return render(request, 'rango/index.html', context_dict)


def about(request):
    #prints out whether method is GET or POST
    print(request.method)
    #prints username, if no one is logged in will print 'AnonymousUser'
    print(request.user)
    return render(request, 'rango/about.html', {})


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            #saves new category to the database
            form.save(commit=True)
            #Now the most recent category added is on the index page
            #So the user is directed back there
        return index(request)
    else:
        #the supplied form conatined errors
        #so it's printed to the terminal
        print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        #tries to find a category name slug with given name
        #if not found, raises a DoesNotExist exception
        # the .get() method returns one model instance or raises exception
        category = Category.objects.get(slug=category_name_slug)

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


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    #Initially set to false, will change to true when registration succeeds
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILE['picture']

            profile.save()

            registered = True
        else:

            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})