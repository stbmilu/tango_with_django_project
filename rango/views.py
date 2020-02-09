from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    # Construct a dictionary to pass to the template engine as its context
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    # could i mix up the qotation marks here as the propose to reduce similarity?
    # context_dict = {"boldmessage": 'Crunchy, creamy, cookie, candy, cupcake!'}
    
    # Query the database for a list of All categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5
    # Place the list in context dirt dictionnary (with our boldmessage!)
    # that will be passed to the template engine.
    
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list


    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    # could i mix up the qotation marks here as the propose to reduce similarity?
    return render(request, "rango/index.html", context=context_dict)

def index2(request):
    return HttpResponse("Hello, my friend!")

def about(request):
    return render(request, "rango/about.html")


def show_category(request, category_name_slug):
    
    context_dict = {}

    try:
        #The .get()method returns one model instance or raises an exception
        category = Category.objects.get(slug=category_name_slug)

        #Retrieve all of the associated pages.
        # filter(): return a list of page objects or an empty list
        # in what order will the pages list return?
        pages = Page.objects.filter(category=category)


        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # to verify the category exists.
        context_dict['category'] = category

    except Category.DoesNotExist:
        # the template will display " no category"
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    # request.post is the name?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # check if we provide a valid form
        if form.is_valid():
            # Save the new category to database.
            form.save(commit=True)
            # The category is saved, and send user back to index page 
            return redirect(reverse('rango:index'))
        else:
            # The supplied form contained errors
            # just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                #ensure that the page haven't been passed to database through commit = False?
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug':
                                                                        category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    # Set False initially, changes to True when registration succeeds.
    registered = False
    
    if request.method == 'POST':
        # Attempt to grap the raw form information, both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Hash the password, and update the user object
            user.set_password(user.password)
            user.save()
            # The commit = False delays saving the model until we avoid the integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # if user provide a picture, we get it from input form, put it in UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            # Update the status of registered variable
            registered = True
        else:
            # Invalid form or forms - mistakes or something? print it in the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so render the forms, these forms will be blank for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render depending on the status or forms
    return render(request, 'rango/register.html', context = {'user_form': user_form, 
                                                             'profile_form': profile_form, 
                                                             'registered': registered})

def user_login(request):
    # try to pull out the information
    if request.method == 'POST':
        # from the login form, request.POST.get('') returns none if none while
        # request.POST[''] raise a keyError exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # if username and password combination is valid return a user object
        # Django machinery
        user = authenticate(username=username, password=password)

        if user:
            # check the account have been disabled or not
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    # The request is not a Http post, display the login form, a http GET?
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
