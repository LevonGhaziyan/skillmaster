from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect

class ViewBase(View):
    def render_page(self, *, error=None):
        if error:
            self.context["error"] = error

        return render(self.request, self._template, self.context)
    
    def success_redirect(self):
        return HttpResponseRedirect(self._success_redirect)