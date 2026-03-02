from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.http import HttpResponse, Http404, HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from django.views import generic

from .forms import NameForm, ContactForm, AddQuestionForm, LoginForm
from .models import Question, Choice
from django.core.mail import send_mail

class IndexView(generic.ListView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/polls/login")
        return super().dispatch(request, *args, **kwargs)

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def all(request):

        return render(
            request,
            "polls/all.html",
            {"questions": Question.objects.all()},
        )



def add_question(request):
    if request.method == "POST":
        question_text = request.POST.get("question_text", "").strip()
        choices = []

        for i in range(5):
            text = request.POST.get("choice_text"+str(i), "").strip()
            if text:
                choices.append(text)

        if question_text and choices:
            q = Question.objects.create(
                question_text=question_text,
                pub_date=timezone.now()
            )

            for text in choices:
                Choice.objects.create(
                    question=q,
                    choice_text=text
                )

            return HttpResponseRedirect(reverse("polls:add_question"))

    return render(request, "polls/add_question.html")

def statistics(request):

    total_questions = Question.objects.all().count()
    total_choices = Choice.objects.all().count()
    total_votes = Choice.objects.all().aggregate(sum=Sum("votes"))["sum"]
    mean_votes_per_question = Choice.objects.all().aggregate(sum=Sum("votes"))["sum"] / total_questions
    most_popular_question = Question.get_most_popular()
    least_popular_question = Question.get_least_popular()


    return render(
        request,
        "polls/statistics.html",
        {
            "total_questions": total_questions,
            "total_choices": total_choices,
            "total_votes": total_votes,
            "mean_votes_per_question": mean_votes_per_question,
            "most_popular_question": most_popular_question,
            "least_popular_question": least_popular_question,
         },

    )


def frequency(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    return render(
        request,
        "polls/frequency.html",
        {
            "question" : question,
            "choices": question.get_choices()},
    )

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "polls/name.html", {"form": form})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]

            recipients = ["info@example.com"]
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)

            return HttpResponseRedirect("/thanks/")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})

def add_question2(request):
    if request.method == "POST":
        question_text = AddQuestionForm(request.POST)
        choices = []


        for i in range(5):
            text = request.POST.get("choice_"+str(i), "").strip()
            if text:
                choices.append(text)

        if question_text and choices:
            q = Question.objects.create(
                question_text=question_text,
                pub_date=timezone.now()
            )

            for text in choices:
                Choice.objects.create(
                    question=q,
                    choice_text=text
                )
    else:
        form = AddQuestionForm()




    return render(request, "polls/add_question2.html",{"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("../")  # change si besoin

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next")
            return redirect(next_url or "../")
        else:
            messages.error(request, "Identifiants invalides.")

    return render(request, "auth/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/polls/login")


@login_required
def home_view(request):
    return render(request, "index.html")