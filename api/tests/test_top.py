import datetime
from unittest.mock import Mock, patch

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Movie, Comment


class TopListTestCase(APITestCase):
    """Test retrieving movies top list"""
    def setUp(self):
        def create_dummy_movie(title):
            return Movie.objects.create(
                title=title,
                details={'Title': title},
            )

        self.movie1 = create_dummy_movie('Movie 1')
        self.movie2 = create_dummy_movie('Movie 2')
        mocked = datetime.datetime(1990, 1, 20, 1, 1, 1)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie2, comment="1st comment movie 2")
        mocked = datetime.datetime(1990, 1, 21, 1, 1, 1)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie2, comment="2nd comment movie 2")
        mocked = datetime.datetime(1990, 1, 22, 1, 1, 1)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie2, comment="3rd comment movie 2")
        mocked = datetime.datetime(1990, 1, 23, 1, 1, 1)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie1, comment="1st comment movie 1")
        mocked = datetime.datetime(1990, 1, 24, 1, 1, 1)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie1, comment="2st comment movie 1")
        mocked = datetime.datetime(1990, 1, 25, 1, 1, 1)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie1, comment="3rd comment movie 1")
        mocked = datetime.datetime(1990, 1, 26, 1, 1, 1)
        with patch('django.utils.timezone.now', Mock(return_value=mocked)):
            Comment.objects.create(movie_id=self.movie1, comment="4th comment movie 1")


    def test_top_all_comments(self):
        """Test fetching top with all comments"""
        url = reverse('top')
        response = self.client.get(url, {
            'start': '1990-01-01',
            'end': '1990-01-31',
        })
        payload = response.json()
        self.assertListEqual(
            payload,
            [
                {
                    'movie_id': self.movie1.id,
                    'total_comments': 4,
                    'rank': 1,
                },
                {
                    'movie_id': self.movie2.id,
                    'total_comments': 3,
                    'rank': 2,
                },
            ]
        )

    def test_top_one_day_comments(self):
        """Test fetching top for one day"""
        url = reverse('top')
        response = self.client.get(url, {
            'start': '1990-01-20',
            'end': '1990-01-20',
        })
        payload = response.json()
        self.assertListEqual(
            payload,
            [
                {
                    'movie_id': self.movie2.id,
                    'total_comments': 1,
                    'rank': 1,
                },
                {
                    'movie_id': self.movie1.id,
                    'total_comments': 0,
                    'rank': 2,
                },
            ]
        )

    def test_top_no_comments(self):
        """Test fetching top for one day"""
        url = reverse('top')
        response = self.client.get(url, {
            'start': '1990-01-01',
            'end': '1990-01-01',
        })
        payload = response.json()
        self.assertListEqual(
            payload,
            [
                {
                    'movie_id': self.movie1.id,
                    'total_comments': 0,
                    'rank': 1,
                },
                {
                    'movie_id': self.movie2.id,
                    'total_comments': 0,
                    'rank': 1,
                },
            ]
        )

    # Missing parameters
    def test_missing_start_param(self):
        url = reverse('top')
        response = self.client.get(url, {
               'end': '2019-01-31',
        })
        paypload = response.json()
        self.assertEqual(
            paypload,
            {"detail": "Query parameter \"start\" not found."})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_missing_end_param(self):
        url = reverse('top')
        response = self.client.get(url, {
            'start': '2019-01-31',
        })
        paypload = response.json()
        self.assertEqual(
            paypload,
            {"detail": "Query parameter \"end\" not found."})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Bad input data
    def test_invalid_start_param(self):
        url = reverse('top')
        response = self.client.get(url, {
            'start': '2019-99-01',
            'end': '2019-01-31'
        })
        paypload = response.json()
        self.assertEqual(
            paypload,
            ["Please verify \"start\" parameter. Expected format: YYYY-MM-DD"])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_end_param(self):
        url = reverse('top')
        response = self.client.get(url, {
            'start': '2019-01-01',
            'end': '2019-99-31'
        })
        paypload = response.json()
        self.assertEqual(
            paypload,
            ["Please verify \"end\" parameter. Expected format: YYYY-MM-DD"])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_after_end_param(self):
        url = reverse('top')
        response = self.client.get(url, {
            'start': '2029-01-01',
            'end': '2019-01-31'
        })
        paypload = response.json()
        self.assertEqual(
            paypload,
            ["Start date have to be less than or equal end date"])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
