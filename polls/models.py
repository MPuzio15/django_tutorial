from django.db import models


# Question:
# - content
# - data

class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="Question")
    pub_date = models.DateTimeField(verbose_name="Date published")

    def __str__(self):
        return f'"{self.question_text}"'


# Answer:
# - content
# - question related to that answer
# - how many votes
# tutaj django tworzy relacje odwrotna - ForeignKey -
# dzieki niemu mozemy sie dowiedziec jakie pytania zostaly przypisane do danego pytania
# zeby sie do niego dostac w shell: zmienna = Question.objects.first() zmienna.choice_set.all()
# choice set
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'"{self.choice_text}"'
