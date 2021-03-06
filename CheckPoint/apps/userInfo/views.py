from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from .forms import UpdateUser

#a default index view
def index(request):
    return HttpResponse("Hello, world. You're at the user app")

"""
The user info view will based on the post request you send check if change your user info if its a a valid input
"""
#a view that shows the user info and form for editing
def user_info(request):
    #user is the user you are loged in with
    user = request.user
    #args is the arguments that are sent to the template
    args = {}
    #checks if the user is loged inn
    if user.is_authenticated:
        #if the user clicks the submit button a POST request is sent
        if request.method == 'POST':
            #if the post request was from the update button
            if "update_info" in request.POST:
                #get the form from the post request
                form = UpdateUser(request.POST)
                #if the form is valid go into the if statement
                if form.is_valid():
                    username = request.POST.get('username','')
                    emailAddress = request.POST.get('email','')
                    first_name = request.POST.get('first_name', '')
                    last_name = request.POST.get('last_name', '')
                    #only update the fields that are not empty
                    if username != '':
                        #set user.username to the post we got
                        user.username = username
                    #only update the fields that are not empty
                    if emailAddress != '':
                        #set user.email to the post we got
                        user.email = emailAddress
                    if first_name != '':
                        #set user.first_name to the post we got
                        user.first_name = first_name
                    if last_name != '':
                        #set user.last_name to the post we got
                        user.last_name = last_name
                    #save the new userinfo
                    user.save()
                    #rederect to the same page but now with updated info
                    return HttpResponseRedirect('../edit')
            else:
                #if the update button wasn't clicked, set the form empty
                form = UpdateUser();
            #if the post request was from the change password button
            if "change_password" in request.POST:
                #set change_password_form to the Password cahnge form and send the usr as a parameter
                #so it knows witch user who want to change password
                change_password_form = PasswordChangeForm(user, request.POST)
                if change_password_form.is_valid():
                    change_password_form.save()
                    update_session_auth_hash(request, user)
                    return HttpResponseRedirect('../edit')
            else:
                #if the update button wasn't clicked, set the form empty
                change_password_form = PasswordChangeForm(user)
            args['form'] = form
            args['change_password_form'] = change_password_form
        else:
            args['form'] = UpdateUser()
            args['change_password_form'] = PasswordChangeForm(user)
        return render(request, 'user/user.html', args)

    else:
        args['user'] = ''
        return render(request, 'user/user.html', args)
