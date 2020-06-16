from django.shortcuts import render, redirect
from django.http import FileResponse
from django import forms
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db.models import Q
import os


# Create your views here.
class AddProjectForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput({"class": "form-control form-group"}),
                           label="Project name:", required=True, max_length=512)


class SearchForm(forms.Form):
    project = forms.CharField(widget=forms.TextInput({"class": "form-control form-group"}),
                              max_length=512, label="Project", required=False)
    name = forms.CharField(widget=forms.TextInput({"class": "form-control form-group"}),
                           max_length=512, label="Title", required=False)
    author = forms.CharField(widget=forms.TextInput({"class": "form-control form-group"}),
                             max_length=512, label="Author", required=False)


@csrf_exempt
@permission_required("PaperManager.add_project")
def add_project(request):
    if not request.method == "POST":
        return redirect("main.html,manage")
    add_project_form = AddProjectForm(request.POST)
    if add_project_form.is_valid():
        new_project = Project(
            user=request.user,
            name=add_project_form.cleaned_data['name'],
        )
        new_project.save()
    return redirect("main.html,manage")


@csrf_exempt
@permission_required("PaperManager.add_paper")
def add_paper(request):
    class AddPaperForm(forms.Form):
        filebin = forms.FileField(label="Upload paper:", required=True)
        project = forms.ChoiceField(choices=((x.id, x.name) for x in Project.objects.filter(user=request.user)),
                                    required=True)
        name = forms.CharField(widget=forms.TextInput({"class": "form-control form-group"}),
                               label="Title:", required=True, max_length=512)
        author = forms.CharField(widget=forms.TextInput({"class": "form-control form-group"}),
                                 label="Author:", required=True, max_length=512)

    if not request.method == "POST":
        return redirect("main.html,manage")
    add_paper_form = AddPaperForm(request.POST, request.FILES)
    if add_paper_form.is_valid():
        new_paper = Paper(
            user=request.user,
            project=Project.objects.get(id=add_paper_form.cleaned_data['project']),
            name=add_paper_form.cleaned_data['name'],
            author=add_paper_form.cleaned_data['author'],
            filename=request.FILES['filebin']._name,
            filebin=request.FILES['filebin'],
            filesize=request.FILES['filebin'].size / 1024 ** 2,
        )
        new_paper.save()
    return redirect("main.html,manage")


@csrf_exempt
@permission_required("PaperManager.delete_project")
def delete_project(request):
    if not request.method == "POST":
        return redirect("main.html,manage")
    for i in request.POST.getlist('delete-list'):
        try:
            item = Project.objects.get(id=i)
            item.delete()
        except:
            pass
    return redirect("main.html,manage")


@csrf_exempt
@permission_required("PaperManager.delete_paper")
def delete_paper(request):
    if not request.method == "POST":
        return redirect("main.html,manage")
    for i in request.POST.getlist('delete-list'):
        try:
            item = Paper.objects.get(id=i)
            os.remove("data/" + item.filebin.name)
            item.delete()
        except:
            pass
    return redirect("main.html,manage")


@csrf_exempt
@permission_required(("PaperManager.view_paper", "PaperManager.view_project"))
def main(request, init=None, search=None):
    class AddPaperForm(forms.Form):
        filebin = forms.FileField(label="Upload paper:", required=True)
        project = forms.ChoiceField(choices=((x.id, x.name) for x in Project.objects.filter(user=request.user)),
                                    required=True)
        name = forms.CharField(widget=forms.TextInput({"class": "form-control form-group"}),
                               label="Title:", required=True, max_length=512)
        author = forms.CharField(widget=forms.TextInput({"class": "form-control form-group"}),
                                 label="Author:", required=True, max_length=512)

        def __init__(self, *args, **kwargs):
            super(AddPaperForm, self).__init__(*args, **kwargs)
            self.fields['filebin'].widget.attrs.update({"class": "form-group"})
            self.fields['project'].widget.attrs.update({"class": "form-group form-control"})

    context = {
        'this_user': request.user.username,
        init + '_active_1': 'class="active"',
        init + '_active_2': 'in active',
        'add_project': AddProjectForm(),
        'add_paper': AddPaperForm(),
        'search_box': SearchForm(),
        'display_projects': Project.objects.filter(user=request.user),
        'display_papers': Paper.objects.filter(user=request.user),
    }
    if search and request.method == "POST":
        question = SearchForm(request.POST)
        if question.is_valid():
            context['display_result'] = Paper.objects.filter(
                Q(project__name__contains=question.cleaned_data['project']) &
                Q(name__contains=question.cleaned_data['name']) &
                Q(author__contains=question.cleaned_data['author']) &
                Q(user=request.user)
            )
    # GET
    all_size = sum([x.filesize for x in Paper.objects.filter(user=request.user)])
    all_space, _ = Space.objects.get_or_create(defaults={"user": request.user, "filesize": 0}, user=request.user)
    if all_size >= all_space.filesize:
        context['space_full'] = 'value="Space Used Up" disabled'
    return render(request, "main.html", context)


@permission_required('PaperManager.view_paper')
def download(request):
    index = int(request.path.lstrip('/download-'))
    filepath = Paper.objects.get(id=index).filebin.name
    return FileResponse(open("data/" + filepath, "rb"))
