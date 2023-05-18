from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_not_exceed_current_year(value):
    """Validate that the year field value is below the current year."""
    if value > timezone.now().year:
        raise ValidationError(
            'Release year may not be above the current year.'
        )
