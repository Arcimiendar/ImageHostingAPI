from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.storage import get_storage_class
from django.test import TestCase
from django.urls import reverse

from datetime import datetime, timedelta
import pytz

from api.models import Image, ExpirableLink, AccountPlanAssignement


User = get_user_model()
Storage = get_storage_class()


class TestExperibableLink(TestCase):
    def test_expired(self):
        user = User.objects.create_user('test_user_name')
        AccountPlanAssignement.objects.create(user=user, account_plan_id=3)
        image = Image.objects.create(
            uploader=user, image_file=File(open('static/test_image.jpg', 'rb'))
        )
        self.expirable_link = ExpirableLink.objects.create(
            image=image,
            time_created=datetime(2000, 1, 1, 1, tzinfo=pytz.UTC),
            experation_period=timedelta(300)
        )

        self.client.force_login(user)
        response = self.client.get(reverse('expirable-link'))
        self.assertEqual(len(response.data), 0)

        user.delete()

    def test_not_expired(self):
        user = User.objects.create_user('test_user_name')
        AccountPlanAssignement.objects.create(user=user, account_plan_id=3)
        image = Image.objects.create(
            uploader=user, image_file=File(open('static/test_image.jpg', 'rb'))
        )
        self.expirable_link = ExpirableLink.objects.create(
            image=image,
            time_created=datetime.now(tz=pytz.UTC),
            experation_period=timedelta(4000)
        )

        self.client.force_login(user)
        response = self.client.get(reverse('expirable-link'))
        self.assertEqual(len(response.data), 1)

        user.delete()

    def test_create(self):
        user = User.objects.create_user('test_user_name')
        AccountPlanAssignement.objects.create(user=user, account_plan_id=3)
        image = Image.objects.create(
            uploader=user, image_file=File(open('static/test_image.jpg', 'rb'))
        )

        self.client.force_login(user)
        response = self.client.post(
            reverse('expirable-link'), data={
                'image': image.id,
                'experation_period': '5:00'
            }
        )
        self.assertIn('experation_period', response.data)
        self.assertIn('image', response.data)

        response = self.client.get(reverse('expirable-link'))
        self.assertEqual(len(response.data), 1)

        user.delete()

    def test_failed_to_create(self):
        user1 = User.objects.create_user('test_user_name1')
        user2 = User.objects.create_user('test_user_name2')
        AccountPlanAssignement.objects.create(user=user1, account_plan_id=3)
        AccountPlanAssignement.objects.create(user=user2, account_plan_id=3)
        image = Image.objects.create(
            uploader=user1, image_file=File(open('static/test_image.jpg', 'rb'))
        )

        self.client.force_login(user2)
        response = self.client.post(
            reverse('expirable-link'), data={
                'image': image.id,
                'experation_period': '5:00'
            }
        )
        self.assertEqual(response.status_code, 400)

        user1.delete()
        user2.delete()


class TestImage(TestCase):
    def test_list(self):
        user = User.objects.create_user('test_user_name')
        AccountPlanAssignement.objects.create(user=user, account_plan_id=3)
        Image.objects.create(
            uploader=user, image_file=File(open('static/test_image.jpg', 'rb'))
        )

        self.client.force_login(user)
        response = self.client.get(reverse('image'))
        self.assertEqual(len(response.data), 1)

        user.delete()

    def test_list_failed(self):
        user = User.objects.create_user('test_user_name')
        AccountPlanAssignement.objects.create(user=user, account_plan_id=1)
        Image.objects.create(
            uploader=user, image_file=File(open('static/test_image.jpg', 'rb'))
        )

        self.client.force_login(user)
        response = self.client.get(reverse('image'))
        self.assertEqual(response.status_code, 403)

        user.delete()

    def test_create(self):
        user = User.objects.create_user('test_user_name')
        AccountPlanAssignement.objects.create(user=user, account_plan_id=1)

        self.client.force_login(user)
        with open('static/test_image.jpg', 'rb') as f:
            response = self.client.post(reverse('image'), data={
                'image_file': f
            })
        self.assertIn('image_file', response.data)
        self.assertIn('id', response.data)

        user.delete()


class TestThumbnails(TestCase):
    def test_get_basic_thumbnails(self):
        user = User.objects.create_user('test_user_name')
        AccountPlanAssignement.objects.create(user=user, account_plan_id=2)
        Image.objects.create(
            uploader=user, image_file=File(open('static/test_image.jpg', 'rb'))
        )

        self.client.force_login(user)
        response = self.client.get(reverse('thumbnails'))
        self.assertEqual(len(response.data), 2)

        user.delete()
