import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from dpdapi.models import Domain, Alias


class RegexTestCase(APITestCase):
    aliases = ['ops-alert@example.com', 'yolo-announce@example.com']

    def setUp(self):
        user = User.objects.create(username='yolo')
        self.domain = Domain.objects.create(name='example.com')
        for a in self.aliases:
            Alias.objects.create(source=a, destination='ninja@example.com', domain=self.domain)
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

    def test_delete_bulk_single(self):
        data = {'destination': 'ninja@example.com', 'source': 'ding@example.com', 'domain': self.domain.pk}
        Alias.objects.create(source=data['source'], destination=data['destination'], domain=self.domain)
        res = self.client.delete(reverse('alias-delete-bulk'), data=[data], format='json')
        self.assertEqual(res.status_code, 204, res.data)
