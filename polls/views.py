from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError

from .models import Question, Choice


# 1.widok wszystkich opublikowanych pytan

def index(request):
    questions = Question.objects.all()
    title = "Wypełnij ankietę i sprawdź, czy prowadzisz ekologiczny tryb życia"
    context = {
        "questions": questions,
        "title": title,
    }
    return render(request, 'polls/index.html', context)


# 2.Widok szczegolowy danego pytania
def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, id=question_id)
    title = f' {question.question_text}'
    context = {
        "question": question,
        "title": title,
    }
    return render(request, 'polls/detail.html', context)


# 3.widok, ktory reaguje na zaglosowanie przez uzytkownika

def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    choice_form = request.POST.get('choice')

    try:
        selected_choice = question.choice_set.get(id=choice_form)
    except Choice.DoesNotExist:
        return redirect('polls:detail', question_id)

    selected_choice.votes += 1
    selected_choice.save()
    return redirect('polls:results', question_id)


# 4. widok z wynikami dla danego pytania

def results(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    title = f'Wyniki dla pytania:\n {question.question_text}'
    context = {
        "question": question,
        "title": title,
    }
    return render(request, 'polls/results.html', context)
