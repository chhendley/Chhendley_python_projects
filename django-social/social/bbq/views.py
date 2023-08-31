from django.shortcuts import render, redirect
from .forms import BBQ_post_Form
from .models import BBQ_post, Profile

def dashboard(request):
    form = BBQ_post_Form(request.POST or None)
    if request.method == "POST":
        form = BBQ_post_Form(request.POST)
        if form.is_valid():
            bbq_post = form.save(commit=False)
            bbq_post.user = request.user
            bbq_post.save()
            return redirect('bbq:dashboard')
    followed_posts = BBQ_post.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")

    return render(
        request,
        "bbq/dashboard.html",
        {"form": form, "Posts": followed_posts},
    )

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    #double folder name is used to avoid confusing django
    return render(request, "bbq/profile_list.html", {"profiles": profiles})

def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()


    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "bbq/profile.html", {"profile": profile})
