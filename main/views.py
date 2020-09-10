from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from users.MyForms import ProfileForm
from users.models import UserProfile


def main(request):
    pass
    return render(request, 'main/main.html')


def classify(request):
    pass
    return render(request, 'main/classify.html')


def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'main/mainProfile.html', {'user': user})


def classify(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'main/mainClassify.html', {'user': user})


def classifilePerson(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'main/person.html', {'user': user})


def classifilePoint(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'main/point.html', {'user': user})


def classifileVideo(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'main/video.html', {'user': user})


def classifileScenery(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'main/scenery.html', {'user': user})


def classifileCutScreen(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'main/cutScreen.html', {'user': user})


def personInfo(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()

            return HttpResponseRedirect(reverse('main:mainProfile', args=[user.id]))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                        'org': user_profile.org, 'telephone': user_profile.telephone, }
        form = ProfileForm(default_data)
    return render(request, 'main/mainPersonInfo.html', {'form': form, 'user': user})
