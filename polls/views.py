
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView
from django.urls import reverse
from .forms import QuestionForm, ChoiceForm
from .models import Question, Choice


class MainPage(TemplateView):
    template_name = 'polls/main_page.html'
    extra_context = {
        "title": "Sprawdź, czy prowadzisz ekologiczny tryb życia"
    }


# 1.widok wszystkich opublikowanych pytan

# def index(request):
#     questions = Question.objects.all()
#     title = "Wypełnij ankietę i sprawdź, czy prowadzisz ekologiczny tryb życia"
#     context = {
#         "questions": questions,
#         "title": title,
#     }
#     return render(request, 'polls/index.html', context)

class IndexView(ListView):
    # model = Question == queryset = Question.objects.all()
    queryset = Question.objects.all()
    context_object_name = "questions"  # oryginalnie: object_list
    # lista wszystkich obiektow bedzie - object.List ale u nas sie nazywa context_object
    extra_context = {
        "title": "Lista pytań",
    }
    template_name = 'polls/index.html'


# 2.Widok szczegolowy danego pytania
# def detail(request, question_id):
#     # question = Question.objects.get(id=question_id)
#     question = get_object_or_404(Question, id=question_id)
#     title = f' {question.question_text}'
#     context = {
#         "question": question,
#         "title": title,
#     }
#     return render(request, 'polls/detail.html', context)

class Detail(DetailView):
    # pola klasy!!!
    # automatycznie ten widok dopisuje sobie.get(param=wartosc) wiec dopiero pozniej pobieramy konkretny egzemplarz
    queryset = Question.objects.all()
    # domyslnie pk - Primary key, bo domyslnie oczeuje pk wiec musimy te nazwe nadpisac
    pk_url_kwarg = "question_id"
    context_object_name = "question"  # oryginalnie: object
    template_name = 'polls/detail.html'
    # jezeli python napotka metode, to python nie wykonuje tresci tej metody, jezeli nie zostala wywowlana
    # dla dynamicznych a nie statycznych pol klasy musimy uzyc metody get context data-state sie zmienia!!!
    # a w stacie nie mozemy uzywac zadnych metod
    # get_context_data jest zdefiniowany u kilku rodzicow naszej klasy

    # key word arguments - takie argumenty funkcji. ktore musimy podac wpisując ich nazwy, czyli argumenty nazwane - są przechowywane w slowniku
    def get_context_data(self, **kwargs):
        context = {
            "title": f'{self.object.question_text}'
        }
        # rozszerza object rodzica o nasz context, wskazujemy ze to ma byc kwargs, ktory jest slownikiem
        context.update(kwargs)
        return super().get_context_data(**context)
    # super() w tym przypadku sprawi ze wewnatrz klasy Detail mozemy wykonac metode z klasy bazowej-nie ma jej w self
    #

# 3.widok, ktory reaguje na zaglosowanie przez uzytkownika


class ResultsView(DetailView):
    queryset = Question.objects.all()
    pk_url_kwarg = "question_id"
    template_name = 'polls/results.html'
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = {
            "title": f'Wynik dla pytania:\n {self.object.question_text}'
        }
        # rozszerza object rodzica o nasz context, wskazujemy ze to ma byc kwargs, ktory jest slownikiem
        context.update(kwargs)
        return super().get_context_data(**context)


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

# def results(request, question_id):
#     question = get_object_or_404(Question, id=question_id)
#     title = f'Wyniki dla pytania:\n {question.question_text}'

#     # sa to zmienne, ktore wyswietlamy na stronie, moga miec dowolna nazwe,
#     # wypisujemy je po to, zebysmy mogli korzystac z nich w templates - propsy!!!!
#     # zmienne ktore sa uzywane w szablonie bazy danych musza byc rowniez przekazane w context
#     # jedynie id nie trzeba definiowac
#     context = {
#         "question": question,
#         "title": title,
#     }
#     return render(request, 'polls/results.html', context)

# 5. widok - create question

class CreateQuestion(FormView):
    template_name = "polls/create_question.html"
    form_class = QuestionForm

    extra_context = {
        "title": "Nowe pytanie"
    }
# tutaj uzywamy reverse -synchronicznie, zeby to zrobic asynchronicznie - reverse_lazy i zwroci nam promisa
# a promise sie wykona przy wywolaniu funkcji

    def get_success_url(self):
        return reverse("polls:detail", args=[self.object.id])
    # tworzymy object nowy

    def form_valid(self, form):
        self.object = Question(question_text=form.cleaned_data['question_text'],
                               pub_date=form.cleaned_data['pub_date']
                               )
        self.object.save()
        return super().form_valid(form)


# def create_question(request):
#     #     context = {}
#     # z request mozemy sie dostac np do metody jaka zostala uzyta
#     #     if request.method == "POST":
#     #         # pobranie wszystkich danych ktore zostaly przekazane metoda POST
#     #         data = request.POST

#     #         # weryfikacja danych (musimy sprawdzic czy dane od uzytkownika sa poprawne)
#     #         question_text = data.get('question_text')  # zwroci element lub None
#     #         pub_date = data.get('pub_date')

#     #         if not question_text or not pub_date:
#     #             # weryfikacja sie nie powiodla - bledy w formularzu -> wyswietl info o bledach
#     #             context['errors'] = "Popraw bledy w formularzu"
#     #             context['question_text'] = question_text
#     #             context['pub_date'] = pub_date

#     #         else:
#     #             new_question = Question(
#     #                 question_text=question_text, pub_date=pub_date)
#     #             new_question.save()

#     #         # weryfikacja powiodla sie - dodaj nowe question, zapisz je i przekieruj na liste wszystkich pytan
#     #             return redirect('polls:detail', new_question.id)

#     #     return render(request, 'polls/create_question.html', context)
#     form = QuestionForm()

#     if request.method == "POST":
#         # pobranie danych
#         form = QuestionForm(request.POST)

#         # weryfikacja danych
#         if form.is_valid():
#             # dane poprawne
#             new_question = Question(question_text=form.cleaned_data['question_text'],
#                                     pub_date=form.cleaned_data['pub_date'])

#             new_question.save()
#             # return redirect- przekierwoanie na inna strona
#             return redirect('polls:detail', new_question.id)

#     context = {
#         "form": form
#     }

#     return render(request, "polls/create_question.html", context)

class CreateChoice(CreateView):
    template_name = "polls/create_choice.html"
    form_class = ChoiceForm
    model = Choice
    # ograniczenie zeby nie mozna bylo dodawac opcji ktore maja zero votow- exclude to taki !filter
    # jak nie mamy zadnych odpowiedzi to zwraca NaN wiec trzeba to jakos obsluzyc
    # do tego sluzy object Q

    def get_question(self, question_id):
        # qs = Question.objects.annotate(votes_count=Sum(
        #     'choice__votes')).exclude(votes_count__gt=0)
        # WHERE votes_count = 0 or votes_couns is NULL
        logic = Q(votes_count=0) | Q(votes_count=None)
        qs = Question.objects.annotate(
            votes_count=Sum('choice__votes')).filter(logic)
        return get_object_or_404(qs, id=question_id)
    # wywolywana gdy widok obsluguje zadanie http get - gdy ktos laduje formularz po raz pierwszy
    # id jest uzyte w sciezce - question_id mamy do niego dostep za pomoca self.kwargs[question_id]
    # chcemy zablokowac mozliwosc dodawania wyborow do pytan na ktore juz ktos zaglosowal -
    # musimy sie dostac do vote

    def get(self, request, *args, **kwargs):
        self.question = self.get_question(self.kwargs['question_id'])
        # self.question = get_object_or_404(Question, id=self.question_id)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.question = self.get_question(self.kwargs['question_id'])
        # self.question = get_object_or_404(Question, id=self.question_id)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("polls:detail", args=[self.question.id])

    def get_context_data(self, **kwargs):
        context = {
            "title": f'Nowy wybór do pytania: {self.question}',
            "question": self.question

        }
        context.update(kwargs)
        return super().get_context_data(**context)

# dostajemy ten formularz jako argument do metody
# instance- instancja klasy
    def form_valid(self, form):
        form.instance.question = self.question
        return super().form_valid(form)

    # def form_valid(self, form):
    #     self.object = Choice(question=form.cleaned_data['question'],
    #                          choice_text=form.cleaned_data['choice_text']
    #                          )
    #     self.object.save()
    #     return super().form_valid(form)
