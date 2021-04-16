from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.storage import get_storage_class
from django.test import TestCase
from django.urls import reverse

from datetime import datetime, timedelta

from api.models import Image, ExpirableLink, AccountPlanAssignement


User = get_user_model()
Storage = get_storage_class()


class TestExperibableLinkExpired(TestCase):
    def setUp(self) -> None:
        self.storage = Storage()
        self.user = User.objects.create_user('test_user_name')
        self.account_plan_assignement = AccountPlanAssignement.objects.create(user=self.user, account_plan_id=3)
        self.image = Image.objects.create(
            uploader=self.user, image_file=File(open('api/image.jpg', 'rb'))
        )
        self.expirable_link = ExpirableLink.objects.create(
            image=self.image, creator=self.user,
            time_created=datetime(2000, 1, 1, 1),
            experation_period=timedelta(300)
        )

    def test_expired(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('expirable-link'))
        self.assertEqual(len(response.data), 0)

    def tearDown(self) -> None:
        self.image.delete()
        self.expirable_link.delete()
        self.user.delete()


class TestExperibableLinkValid(TestCase):
    def setUp(self) -> None:
        self.storage = Storage()
        self.user = User.objects.create_user('test_user_name')
        self.account_plan_assignement = AccountPlanAssignement.objects.create(user=self.user, account_plan_id=3)
        self.image = Image.objects.create(
            uploader=self.user, image_file=File(open('api/image.jpg', 'rb'))
        )
        self.expirable_link = ExpirableLink.objects.create(
            image=self.image, creator=self.user,
            time_created=datetime.now(),
            experation_period=timedelta(4000)
        )

    def test_expired(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('expirable-link'))
        self.assertEqual(len(response.data), 1)

    def tearDown(self) -> None:
        self.image.delete()
        self.expirable_link.delete()
        self.user.delete()


class TestCreateExperibableLink(TestCase):
    def setUp(self) -> None:
        self.storage = Storage()
        self.user = User.objects.create_user('test_user_name')
        self.account_plan_assignement = AccountPlanAssignement.objects.create(user=self.user, account_plan_id=3)
        self.image = Image.objects.create(
            uploader=self.user, image_file=File(open('api/image.jpg', 'rb'))
        )

    def test_expired(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('expirable-link'), data={
                'creator': self.user.id,
                'image': self.image.id,
                'experation_period': '5:00'
            }
        )
        self.assertIn('experation_period', response.data)
        self.assertIn('creator', response.data)
        self.assertIn('image', response.data)

        response = self.client.get(reverse('expirable-link'))
        self.assertEqual(len(response.data), 1)

    def tearDown(self) -> None:
        self.image.delete()
        self.user.delete()
