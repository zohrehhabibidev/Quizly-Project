from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .validators import (
    validate_question_options,
    validate_correct_answer,
)


class Quiz(models.Model):
    """Represents a quiz generated from a YouTube video."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the quiz title."""
        return self.title


class Question(models.Model):
    """Represents a question belonging to a quiz."""

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_title = models.TextField()
    question_options = models.JSONField(
        validators=[validate_question_options]
    )
    answer = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Validate the answer against the question options."""
        super().clean()
        try:
            validate_question_options(self.question_options)
        except ValidationError:
            return
        try:
            validate_correct_answer(self.answer, self.question_options)
        except ValidationError as error:
            raise ValidationError({"answer": error.messages}) from error

    def __str__(self):
        """Return the question title."""
        return self.question_title
