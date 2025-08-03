from django.shortcuts import render, redirect
from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    return render(request, "main/index.html", context)


def detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    context = {
        "question": question,
    }
    return render(request, "main/detail.html", context)

def vote(request, question_id):
    question = Question.objects.get(pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'main/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('detail', question.id)