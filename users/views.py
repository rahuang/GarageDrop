from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from users.models import Profile


class LoginPage(TemplateView):
    template_name = 'users/login.html'
    
    
class RegisterPage(TemplateView):
    template_name = 'users/register.html'
    
    
class LogoutPage(View):
    """ Log the user out. """
    
    def get(self, request):
        logout(request)
        return redirect('users_test')
        
        
class ProcessLog(View):
    """ Log the user in. """
    
    def post(self, request):
        
        #################
        # Get POST data #
        #################
        
        postData = request.POST
        
        try:
            username = postData['username']
            password = postData['password']
            
        except KeyError as e:
            response = "FAIL_POSTDATA::{}".format(e)
            return HttpResponseBadRequest(response)
            
            
        ##################
        # Authentication #
        ##################
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Everything is OK
                return redirect('users_test')
                
            else:
                # Account Disabled
                return HttpResponse('FAIL_ACC_DISABLED')
                
        else:
            # Authentication Failed
            return HttpResponse('FAIL_AUTH')
            
            
class ProcessReg(View):
    """ Process the registration form. """
    
    class InvalidData(Exception):
        ''' The POST data that we received is bad in some way. '''
        pass
    
    def post(self, request):
        
        #################
        # Get POST data #
        #################
        
        postData = request.POST
        
        try:
            username = postData['username']
            firstName = postData['firstname']
            lastName = postData['lastname']
            email = postData['email']
            password = postData['password']
            
            gender = postData['gender']
            
        except KeyError as e:
            response = "FAIL_POSTDATA::{}".format(e)
            return HttpResponseBadRequest(response)
            
            
        ##############################
        # Serverside data validation #
        ##############################
        
        try:
            if '@' not in email or '.' not in email:
                raise self.InvalidData("Invalid Email")
                
            if gender not in (choice[0] for choice in Profile.GENDER_CHOICES):
                raise self.InvalidData("Invalid Gender")
                
            if User.objects.filter(username=username).exists():
                raise self.InvalidData("Username Taken")
                
            if User.objects.filter(email=email).exists():
                raise self.InvalidData("Email Taken")
                
        except self.InvalidData as e:
            response = "FAIL_POSTDATA::{}".format(e)
            return HttpResponseBadRequest(response)
            
            
        #################
        # User creation #
        #################
        
        try:
            newUser = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=firstName,
                    last_name=lastName,
                )
                
        except Exception as e:
            response = "FAIL_USER::{}::{}".format(
                    str(e),
                    str(dict(postData)),
                )
            return HttpResponseBadRequest(response)
            
            
        ####################
        # Profile creation #
        ####################
        
        try:
            newProfile = Profile(user=newUser, gender=gender)
            newProfile.save()
            
        except Exception as e:
            response = "FAIL_PROFILE::{}::{}".format(
                    str(e),
                    str(dict(postData)),
                )
            return HttpResponseBadRequest(response)
            
            
        #######################
        # Log the new user in #
        #######################
        
        user = authenticate(username=username, password=password)
        login(request, user)
        
        
        ####################
        # Everything is OK #
        ####################
        
        return redirect('users_test')
        
        
class LoginTestView(View):
    """ Tests if the user is logged in. """
    
    def get(self, request):
        user = request.user
        
        if user.is_authenticated():
            return HttpResponse("USER '{}' LOGGED IN".format(user.username))
        else:
            return HttpResponse("NOT LOGGED IN")
            
            