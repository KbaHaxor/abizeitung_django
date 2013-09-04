from django.contrib import messages
from django.contrib.auth import login as do_login, logout as do_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.template.context import RequestContext

def login(request):
    #messages.debug(request, "Debug!")
    #messages.info(request, "Info!")
    #messages.success(request, "Success!")
    #messages.warning(request, "Warning!")
    #messages.error(request, "Error!")
    
    if request.user.is_authenticated():
        return redirect("/student")
    
    context = {}
    if request.method == "POST":
        form = AuthenticationForm(None, request.POST)
        if form.is_valid():
            user = form.get_user()
            print user
            if user.is_active:
                do_login(request, user)
                return redirect("/student")
            else:
                messages.error(request, "Benutzeraccount ist deaktiviert!")
    else:
        form = AuthenticationForm()
    context["form"] = form
    return render(request, "session/login.html", context, context_instance=RequestContext(request))

def logout(request):
    if request.user.is_authenticated():
        messages.info(request, "Erfolgreich ausgeloggt!")
        do_logout(request)
    return redirect("/login")