from django.http import HttpResponse, Http404
from django.shortcuts import render
# Create your views here.
from django.template import loader

from refresher.models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('refresher/index.html')
    context = {
        'latest_question_list': latest_question_list
    }

#    return HttpResponse(template.render(context, request))
    return render(request, 'refresher/index.html', context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    return render(request, "refresher/detail.html", {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s." % question_id
    return HttpResponse(response)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
