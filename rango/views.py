from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #constructs a dictionary to pass to the template engine as its context
    #Not the key boldmessage is the same as {{boldmessage}} in the template
    context_dict = {'boldmessage': "O.O"}

    #Returns a rendered response to send to the client
    #We make us of the shortout function to make our lives easier
    #Note that the first parameter is the template we wish to use
    return render(request, 'rango/index.html', context=context_dict)


