from django.http import HttpResponse
from django.shortcuts import render

class HelloWorld():
    def home(self):
        return HttpResponse('Hello, World!')
