from django.db import models


class Challenges(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=4)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.code)

    class Meta:
        verbose_name = 'Challenge'
        verbose_name_plural = 'Challenges'
        db_table = 'challenges'
        unique_together = ('code', )


class Questions(models.Model):
    challenge = models.ForeignKey(Challenges)
    order = models.IntegerField(default=0)
    text = models.TextField(default="")
    image = models.FileField(upload_to='images/', max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    counter_time = models.IntegerField(default=60, blank=True, null=True)

    # Answers
    answer1 = models.TextField(blank=True, null=True)
    answer2 = models.TextField(blank=True, null=True)
    answer3 = models.TextField(blank=True, null=True)
    answer4 = models.TextField(blank=True, null=True)

    # Which is the correct answer
    is_correct_answer1 = models.BooleanField(default=False)
    is_correct_answer2 = models.BooleanField(default=False)
    is_correct_answer3 = models.BooleanField(default=False)
    is_correct_answer4 = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({})".format(self.text, self.challenge)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        db_table = 'questions'


class Responses(models.Model):
    question = models.ForeignKey(Questions)
    response_answer1 = models.IntegerField(default=0)
    response_answer2 = models.IntegerField(default=0)
    response_answer3 = models.IntegerField(default=0)
    response_answer4 = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.question)

    class Meta:
        verbose_name = 'Response'
        verbose_name_plural = 'Responses'
        db_table = 'responses'
