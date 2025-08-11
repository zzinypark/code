from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, DetailView

from member.forms import SignupForm, LoginForm
from member.models import UserFollowing
from utils.email import send_email

User = get_user_model()


class SignupView(FormView):
    template_name = "auth/signup.html"
    form_class = SignupForm

    def form_valid(self, form):
        user = form.save()

        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        sign_dump = signing.dumps(signed_user_email)

        # decoded_sign_dump = signing.loads(sign_dump)
        # email = signer.unsign(decoded_sign_dump)
        #
        url = f"{self.request.scheme}://{self.request.META['HTTP_HOST']}/verify/?code={sign_dump}"

        subject = "[Pystagram]이메일 인증을 완료해주세요"
        message = f'다음 링크를 클릭해주세요 <br><a href="{url}">{url}</a>'

        send_email(subject, message, user.email)

        return render(self.request, "auth/signup_done.html", {"user": user})


def verify_email(request):
    code = request.GET.get("code", "")

    signer = TimestampSigner()
    try:
        email = signer.unsign(code, max_age=60 * 30)

    except (TypeError, SignatureExpired):
        return render(request, "auth/not_verified.html")

    user = get_object_or_404(User, email=email, is_active=False)
    user.is_active = True
    user.save()
    return redirect(reverse("main"))


class LoginView(FormView):
    template_name = "auth/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.get(email=email)
        login(self.request, user)

        next_page = self.request.GET.get("next")
        if next_page:
            return HttpResponseRedirect(next_page)

        return HttpResponseRedirect(self.get_success_url())


class UserProfileView(DetailView):
    model = User
    template_name = "profile/detail.html"
    slug_field = "nickname"
    slug_url_kwarg = "slug"
    queryset = User.objects.all().prefetch_related(
        "post_set", "post_set__images", "following", "followers"
    )

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data["is_follow"] = UserFollowing.objects.filter(
                to_user=self.object,
                from_user=self.request.user,
            )

        return data


class UserFollowingView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        pk = kwargs.get("pk", 0)
        to_user = get_object_or_404(User, pk=pk)

        if to_user == self.request.user:
            raise Http404

        # 만약 이미 팔로우가 되어있으면 취소
        following, created = UserFollowing.objects.get_or_create(
            to_user=to_user,
            from_user=self.request.user,
        )

        if not created:
            following.delete()

        return HttpResponseRedirect(
            reverse("profile:detail", kwargs={"slug": to_user.nickname})
        )
        # 안되어있으면 팔로우
