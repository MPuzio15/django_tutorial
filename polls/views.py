from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError

from .forms import QuestionForm
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

# 5. widok - create question


def create_question(request):
    #     context = {}

    #     if request.method == "POST":
    #         # pobranie danych
    #         data = request.POST

    #         # weryfikacja danych (musimy sprawdzic czy dane od uzytkownika sa poprawne)
    #         question_text = data.get('question_text')  # zwroci element lub None
    #         pub_date = data.get('pub_date')

    #         if not question_text or not pub_date:
    #             # weryfikacja sie nie powiodla - bledy w formularzu -> wyswietl info o bledach
    #             context['errors'] = "Popraw bledy w formularzu"
    #             context['question_text'] = question_text
    #             context['pub_date'] = pub_date

    #         else:
    #             new_question = Question(
    #                 question_text=question_text, pub_date=pub_date)
    #             new_question.save()

    #         # weryfikacja powiodla sie - dodaj nowe question, zapisz je i przekieruj na liste wszystkich pytan
    #             return redirect('polls:detail', new_question.id)

    #     return render(request, 'polls/create_question.html', context)
    form = QuestionForm()

    if request.method == "POST":
        # pobranie danych
        form = QuestionForm(request.POST)

        # weryfikacja danych
        if form.is_valid():
            # dane poprawne
            new_question = Question(question_text=form.cleaned_data['question_text'],
                                    pub_date=form.cleaned_data['pub_date'])

            new_question.save()
            return redirect('polls:detail', new_question.id)

    context = {
        "form": form
    }

    return render(request, "polls/create_question.html", context)
