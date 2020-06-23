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

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'"{self.choice_text}"'
