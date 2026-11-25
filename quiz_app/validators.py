from django.core.exceptions import ValidationError


def validate_question_options(options):
    """Validate the four answer options of a question."""
    if not isinstance(options, list) or len(options) != 4:
        raise ValidationError("Exactly four options are required.")

    if not all(isinstance(option, str) and option.strip()
               for option in options):
        raise ValidationError("All options must be non-empty strings.")

    if len(set(options)) != 4:
        raise ValidationError("Answer options must be unique.")


def validate_correct_answer(answer, options):
    """Ensure the correct answer matches an option."""
    if answer not in options:
        raise ValidationError("The answer must match one of the options.")
