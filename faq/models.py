from django.db import models


class Faq(models.Model):
    """
    A model to create and manage FAQs
    """

    question = models.CharField(
        max_length=250,
        unique=True,
        blank=False,
        null=False
    )

    answer = models.TextField(
        max_length=500,
        unique=True,
        blank=False,
        null=False
    )

    def __str__(self):
        return self.question
