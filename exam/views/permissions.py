from abc import ABC, abstractmethod
from typing import Any
from django.http import HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from functools import wraps

from ..models import ExamSimpleUser, TestModel, TestToUser

class PermissionABC(ABC):
    def decorator(self):
        @wraps
        def decorator_inner(func):
            @wraps
            def wrapper(self_inner, request, *args, **kwargs):
                permission = self.checker(request, *args, **kwargs)
                if permission:
                    return func(self_inner, request, *args, **kwargs)
                else:
                    return self.on_deny()
            
            # wrapper.__name__ = decorator_inner.__name__
            # wrapper.__doc__ = decorator_inner.__doc__
            return wrapper
        
        # decorator_inner.__name__ = self.decorator.__name__
        # decorator_inner.__doc__ = self.decorator.__doc__
        return decorator_inner
    
    @abstractmethod
    def checker(self):
        pass
    
    @abstractmethod
    def on_deny(self):
        pass


class LoginRequired(PermissionABC):
    def __call__(self):
        return self.decorator()

    def checker(self, request: HttpRequest, *args, **kwargs):
        return request.user.is_authenticated
    
    def on_deny(self):
        return HttpResponseRedirect("/exam/login")


class PermissionRequired(PermissionABC):
    def __call__(self):
        return self.decorator()

    def checker(self, request: HttpRequest, test_number, *args, **kwargs):
        self.request = request
        self.test_number = test_number

        self._get_user()

        self._get_test()

        return self._compare()
    
    def on_deny(self):
        raise Http404("You don\'t have permission do that!!")
    
    def _get_user(self):
        self.user = get_object_or_404(ExamSimpleUser, user=self.request.user)

    def _get_test(self):
        self.test = get_object_or_404(TestModel, pk=self.test_number)

    def _compare(self):
        try:
            self.test_to_user = TestToUser.objects.get(test=self.test, user=self.user)
        except:
            return False
        else:
            return True

