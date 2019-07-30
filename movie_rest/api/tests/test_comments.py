from rest_framework.test import APITestCase
from django.urls import reverse
from unittest.mock import Mock

from rest_framework import status
from ..models import Movie, Comment


class CommentViewSetTestCase(APITestCase):
    """Test retrieving movies top list"""
    def setUp(self):
        def create_dummy_movie(title):
            return Movie.objects.create(
                title=title,
                details={'Title': title},
            )

        self.movie1 = create_dummy_movie('Movie 1')
        self.movie2 = create_dummy_movie('Movie 2')
        Comment.objects.create(movie_id=self.movie2, comment="1st comment movie 2")
        Comment.objects.create(movie_id=self.movie2, comment="2nd comment movie 2")
        Comment.objects.create(movie_id=self.movie2, comment="3rd comment movie 2")
        Comment.objects.create(movie_id=self.movie1, comment="1st comment movie 1")
        Comment.objects.create(movie_id=self.movie1, comment="2nd comment movie 1")
        Comment.objects.create(movie_id=self.movie1, comment="3rd comment movie 1")
        Comment.objects.create(movie_id=self.movie1, comment="4th comment movie 1")

    def test_get_comments(self):
        """Test fetching list of all comments"""
        url = reverse('comment-list')
        response = self.client.get(url)
        payload = response.json()
        self.assertListEqual(
            sorted([comment['comment'] for comment in payload]),
            ['1st comment movie 1',
             '1st comment movie 2',
             '2nd comment movie 1',
             '2nd comment movie 2',
             '3rd comment movie 1',
             '3rd comment movie 2',
             '4th comment movie 1'
             ]
        )

    def test_get_comments_for_movie(self):
        """Test fetching comments only for movie with specified id"""
        url = reverse('comment-list')
        response = self.client.get(url, {'movie_id': self.movie2.id})
        payload = response.json()
        self.assertListEqual(
            sorted([comment['comment'] for comment in payload]),
            ['1st comment movie 2', '2nd comment movie 2', '3rd comment movie 2']
        )

    def test_incorrect_movie_id_type(self):
        url = reverse('comment-list')
        data = {'movie_id': 'a'}
        response = self.client.get(url, data)
        payload = response.json()
        self.assertEqual(
            payload,
            {"movie_id": ["Incorrect movie_id type. Expected int."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_existing_movie_id_type(self):
        url = reverse('comment-list')
        data = {'movie_id': 123456}
        response = self.client.get(url, data)
        payload = response.json()
        self.assertEqual(
            payload,
            {"movie_id": ["Movie with given is was not found."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment(self):
        """Test creating valid simple comment"""
        url = reverse('comment-list')
        data = {
            'comment': 'New movie 1 comment',
            'movie_id': self.movie1.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        payload = response.json()
        self.assertEqual(
            payload,
            {'comment': 'New movie 1 comment', 'id': payload['id'], 'movie_id': 1})

    def test_empty_comment(self):
        """Test creating valid simple comment"""
        url = reverse('comment-list')
        data = {
            'movie_id': self.movie1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        payload = response.json()
        self.assertEqual(
            payload,
            {
                "comment": [
                    "This field is required."
                ]
            })
