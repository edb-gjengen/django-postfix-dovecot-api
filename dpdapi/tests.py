from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from dpdapi.models import Domain, Alias


class RegexTestCase(APITestCase):
    aliases = ['ops-alert@example.com', 'yolo-announce@example.com']

    def setUp(self):
        user = User.objects.create(username='yolo')
        d = Domain.objects.create(name='example.com')
        for a in self.aliases:
            Alias.objects.create(source=a, destination='ninja@example.com', domain=d)
        self.client.force_login(user)

    def test_get_all(self):
        res = self.client.get(reverse('alias-list'))
        self.assertEqual(len(res.data), len(self.aliases))

    def test_domain_filter(self):
        params = {'domain__name': 'example.com'}
        res = self.client.get(reverse('alias-list'), data=params)
        self.assertEqual(len(res.data), len(self.aliases))

    def test_domain_filter_no_hits(self):
        params = {'domain__name': 'zexample.com'}
        res = self.client.get(reverse('alias-list'), data=params)
        self.assertEqual(len(res.data), 0)

    def test_regex_filter(self):
        params = {'source__regex': '^ops-|^ops@'}
        res = self.client.get(reverse('alias-list'), data=params)
        self.assertEqual(len(res.data), 1)
