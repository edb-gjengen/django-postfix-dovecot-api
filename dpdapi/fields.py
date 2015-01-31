from django.core.exceptions import ValidationError
from django.utils import six


from rest_framework.fields import CharField, EmailValidator
from django.utils.translation import ugettext_lazy as _


def domain_alias_validator(value):
    if not value.startswith('@'):
        raise ValidationError('Not valid')

    EmailValidator().validate_domain_part(value.split('@'))


class EmailOrDomainAliasField(CharField):
    default_error_messages = {
        'invalid': _('Enter a valid email address or domain alias.'),
    }

    def to_internal_value(self, data):
        return six.text_type(data).strip()

    def to_representation(self, value):
        email_validator = EmailValidator(message=self.default_error_messages['invalid'])
        # Try email validation first
        try:
            email_validator(value)
            return six.text_type(value).strip()  # Valid email
        except ValidationError:
            pass

        # Try domain forward validation
        try:
            domain_alias_validator(value)
            return six.text_type(value).strip() # Valid domain alias
        except ValidationError:
            pass

        raise ValidationError(self.default_error_messages, code='invalid')