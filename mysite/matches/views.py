from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import NameForm,ContactForm,UploadFileForm
from django.forms import ModelForm

import os

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def sucess(request):
    return render(request, "matches/uploads_sucess.html")


# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == "POST":
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect("/matches")

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()

#     return render(request, "matches/uploads.html", {"form": form})

# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == "POST":
#         # create a form instance and populate it with data from the request:
#         form = ContactForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#            subject = form.cleaned_data["subject"]
#            message = form.cleaned_data["message"]
#            sender = form.cleaned_data["sender"]
#            cc_myself = form.cleaned_data["cc_myself"]

#            recipients = ["info@example.com"]
#            if cc_myself:
#                recipients.append(sender)

#            print("sendmail")
#           # send_mail(subject, message, sender, recipients)
#            return HttpResponseRedirect("/matches")

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = ContactForm()

#     return render(request, "matches/uploads.html", {"form": form})


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            file = request.FILES['file']
            # print ("is_valid: %s", title)
            print (form.cleaned_data["title"])
            # todo 
            f = open(os.path.join("C:\\3.Work\\Python_code\\csgoNadesAnalysis\\mysite","1.png"),"wb+")
            for chunk in file.chunks():
                f.write(chunk)
            f.close()
            return HttpResponseRedirect("/matches")
    else:
        form = UploadFileForm()
    return render(request, "matches/uploads.html", {"form": form})


# class FileFieldFormView(FormView):
#     form_class = FileFieldForm
#     template_name = "matches/uploads.html"  # Replace with your template.
#     success_url = "matches/uploads_sucess.html"  # Replace with your URL or reverse().

#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         files = form.cleaned_data["file_field"]
#         for f in files:
#             ...  # Do something with each file.
#         return super().form_valid()