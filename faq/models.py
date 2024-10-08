from django.db import models


class Faq(models.Model):
    """
    A model to create and manage FAQs
    """

    question = models.CharField(
        max_length=300,
        unique=True,
        blank=False,
        null=False
    )

    answer = models.TextField(
        max_length=800,
        unique=True,
        blank=False,
        null=False
    )

    def __str__(self):
        return self.question
