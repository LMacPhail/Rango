from django.shortcuts import render
from django.http import HttpResponse
#from rango.models import Category

def index(request):
    return HttpResponse("Rango says hey there partner!")
    #constructs a dictionary to pass to the template engine as its context
    #Not the key boldmessage is the same as {{boldmessage}} in the template
    context_dict = {'boldmessage': "urgh"}

    #Returns a rendered response to send to the client
    #We make us of the shortout function to make our lives easier
    #Note that the first parameter is the template we wish to use
    return render(request, 'rango/index.html', context_dict)

def about(request):
    HttpResponse("Here is the about page")
    # prints out whether the method is a GET or a POST
    print(request.method)
    #prints out the user name, if no one is logged in it prints 'AnonymousUser'
    print(request.user)
    return render(request, 'rango/about.html', {})


