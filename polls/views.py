from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from .models import  Question, Choice
from django.utils import timezone
from .forms import SearchForm
from django.forms.models import modelformset_factory
class IndexView(generic.ListView):
    template_name= 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):

        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(req, question_id):
    p = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = p.choice_set.get(pk=req.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        return render(req, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
def search_form(req):
    form = SearchForm()
    return render(req, 'polls/search_form.html', {"form": form})
def search(req):
    if req.method == 'GET':

        if req.GET.get('question_id'):
          questions = Question.objects.filter(id=req.GET["question_id"])
        elif req.GET.get("question_text"):
          questions = Question.objects.filter(question_text__icontains=req.GET["question_text"])
        formset = modelformset_factory(Question, form=SearchForm)
        form = formset(queryset=questions)
        zipped = zip(form, questions)
        return render(req, 'polls/search.html', {'questions': questions, 'form': form, 'zipped': zipped})
    else:
        form = SearchForm()
        return HttpResponseRedirect(reverse('polls:index'))
def edit(req, question_id):
    q = get_object_or_404(Question,pk=question_id)

    if req.method == 'POST':


        forms = SearchForm(req.POST, instance=q)
        forms.save()
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        form = SearchForm(instance=q)

    return render(req, 'polls/edit.html', {'form': form})
