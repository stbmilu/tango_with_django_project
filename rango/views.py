from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # Construct a dictionary to pass to the template engine as its context
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    # could i mix up the qotation marks here as the propose to reduce similarity?
    context_dict = {"boldmessage": 'Crunchy, creamy, cookie, candy, cupcake!'}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    # could i mix up the qotation marks here as the propose to reduce similarity?
    return render(request, "rango/index.html", context=context_dict)

def index2(request):
    return HttpResponse("Hello, my friend!")

def about(request):
    return render(request, "rango/about.html")
