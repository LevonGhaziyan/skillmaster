from typing import Any
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpRequest, Http404

import json
import secrets
from django.core.cache import cache

from .permissions import LoginRequired

from .view_base import ViewBase

from .email_sender import EmailSender

from ..models import ExamSimpleUser, TestToUser

class UserBase(ViewBase):
    pass


class LogIn(UserBase):
    _template = "exam/login.html"

    _success_redirect = "/exam/"
        
    @property
    def context(self):
        return {}

    def get(self, request:HttpRequest):
        self.request = request

        return self.render_page()
    
    def post(self, request:HttpRequest):
        self.request = request

        self._get_from_POST()

        self._user_authenticate()

        if self.user:
            login(self.request, self.user)
            return HttpResponseRedirect(self._success_redirect)
        else:
            return self.render_page(error="Username or password was wrong!!")
    
    def _get_from_POST(self):
        self.username = self.request.POST.get("username")
        self.password = self.request.POST.get("password")

    def _user_authenticate(self):
        try:
            self.user = authenticate(username=self.username, password=self.password)
        except:
            raise Http404("Something went wrong!!")
    
class LogOut(UserBase):
    _success_redirect = "/exam/login/"

    def get(self, request:HttpRequest):
        self.request = request

        logout(request)

        return HttpResponseRedirect(self._success_redirect)

class SignUp(UserBase):
    _template = "exam/signup.html"

    @property
    def _success_redirect(self):
        return f"/exam/signup/verify?inner_key={self.inner_verification_key}&email={self.email}"
        
    @property
    def context(self):
        return {}

    def get(self, request:HttpRequest):
        self.request = request

        return self.render_page()
    
    def post(self, request:HttpRequest):
        self.request = request

        self._get_from_POST()

        # Validation code must be written

        self._set_verification_key()

        self._set_inner_verification_key()

        self._save_to_cache()

        self._send_email()

        return self.success_redirect()

    def _get_from_POST(self):
        self.firstname = self.request.POST.get("firstname", "")
        self.lastname = self.request.POST.get("lastname", "")
        self.email = self.request.POST.get("email", "")
        self.username = self.request.POST.get("username", "")
        self.password = self.request.POST.get("password", "")
    
    def _set_verification_key(self):
        self._verification_key = secrets.token_urlsafe(6)
    
    @property
    def _cache_value(self):
        return json.dumps({
            "verification_key": self._verification_key,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "username": self.username,
            "password": self.password,
                })
    
    def _set_inner_verification_key(self):
        self.inner_verification_key = secrets.token_urlsafe(10)
    
    def _save_to_cache(self):
        cache.set(self.inner_verification_key, self._cache_value, 60 * 60 * 0.5)
    
    @property
    def _email_notification_text(self):
        return f"Your verification code for {self.email} is {self._verification_key}.\n"\
              "It will expire after 30 minutes!"
    
    def _send_email(self):
        EmailSender("Email verification", self._email_notification_text, [self.email]).start()

class SignUpVerification(UserBase):
    _template = "exam/sign_up_verification.html"

    _success_redirect = "/exam/login/"
        
    @property
    def context(self):
        if self.request.GET.get("inner_key", False):
            return {"inner_key": self.request.GET.get("inner_key")}
        
        raise Http404("Something went wrong!!")

    def get(self, request):
        self.request = request
        
        return self.render_page()
    
    def post(self, request: HttpRequest):
        self.request = request

        self._get_from_POST()

        self._get_inner_verification_key()

        self._get_from_cache()

        if self.equivalence:
            self._create_user()

            self._create_exam_user()

            return HttpResponseRedirect(self._success_redirect)
        else:
            return self.render_page()
    
    def _get_from_POST(self):
        self.verification_key = self.request.POST.get("verification_code", "")
    
    def _get_inner_verification_key(self):
        self.inner_verification_key = self.request.GET.get("inner_key", "")
    
    def _get_from_cache(self):
        try:
            self.cache_value = json.loads(cache.get(self.inner_verification_key))
        except:
            raise Http404("Something went wrong!!")

        if not self.cache_value:
            raise Http404("Something went wrong!!")
    
    @property
    def equivalence(self):
        if self.cache_value["verification_key"] == self.verification_key:
            return True
        
        return False

    def _create_user(self):
        try:
            self.user = User.objects.create_user(first_name=self.cache_value["firstname"], last_name=self.cache_value["lastname"], email=self.cache_value["email"], username=self.cache_value["username"], password=self.cache_value["password"])
            
            self.user.save()
        except:
            raise Http404("Something went wrong!!")

    def _create_exam_user(self):
        try:
            examSimpleUser = ExamSimpleUser(user=self.user)

            examSimpleUser.save()
        except:
            raise Http404("Something went wrong!!")