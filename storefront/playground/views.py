from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# * It take a req and returns a response
# * Request Handler


def sayHello(req):
    # return HttpResponse("Hello World!")
    return render(req, 'hello.html', {'name': "Gaurav"})
