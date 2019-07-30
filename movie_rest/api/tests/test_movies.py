from rest_framework.test import APITestCase
from django.urls import reverse
from unittest.mock import Mock

from rest_framework import status
from ..models import Movie, Comment


class MovieViewSetTestCase(APITestCase):
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

    def test_create_existing_movie(self):
        """Try to create movie which exists in database."""
        url = reverse('movie-list')
        data = {'title': 'Movie 1'}
        response = self.client.post(url, data)
        paypload = response.json()
        self.assertEqual(
            paypload,
            {"Error": ["Movie with given title already exists."]})
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_new_movie(self):
        """Try to create movie which exists in database."""
        url = reverse('movie-list')
        data = {'title': 'Spotlight'}
        response = self.client.post(url, data)
        paypload = response.json()
        self.assertEqual(
            paypload,
            {
                "id": paypload["id"],
                "title": "Spotlight",
                "details": {
                    "Title": "Spotlight",
                    "Year": "2015",
                    "Rated": "R",
                    "Released": "20 Nov 2015",
                    "Runtime": "129 min",
                    "Genre": "Crime, Drama",
                    "Director": "Tom McCarthy",
                    "Writer": "Josh Singer, Tom McCarthy",
                    "Actors": "Mark Ruffalo, Michael Keaton, Rachel McAdams, Liev Schreiber",
                    "Plot": "The true story of how the Boston Globe uncovered the massive scandal of child molestation and cover-up within the local Catholic Archdiocese, shaking the entire Catholic Church to its core.",
                    "Language": "English",
                    "Country": "USA",
                    "Awards": "Won 2 Oscars. Another 119 wins & 138 nominations.",
                    "Poster": "https://m.media-amazon.com/images/M/MV5BMjIyOTM5OTIzNV5BMl5BanBnXkFtZTgwMDkzODE2NjE@._V1_SX300.jpg",
                    "Ratings": [
                        {
                            "Source": "Internet Movie Database",
                            "Value": "8.1/10"
                        },
                        {
                            "Source": "Rotten Tomatoes",
                            "Value": "97%"
                        },
                        {
                            "Source": "Metacritic",
                            "Value": "93/100"
                        }
                    ],
                    "Metascore": "93",
                    "imdbRating": "8.1",
                    "imdbVotes": "366,728",
                    "imdbID": "tt1895587",
                    "Type": "movie",
                    "DVD": "23 Feb 2016",
                    "BoxOffice": "N/A",
                    "Production": "Open Road Films",
                    "Website": "http://SpotlightTheFilm.com",
                    "Response": "True"
                },
                "comments": []
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_without_title(self):
        """Check title presence validation"""
        url = reverse('movie-list')
        response = self.client.post(url)
        payload = response.json()
        self.assertEqual(
            payload,
            {"Error": ["Mandatory \"title\" parameter is missing."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_too_long_title(self):
        """Try to create movie with too long title (>255 chars)"""
        url = reverse('movie-list')
        response = self.client.post(url, {'title': ' '})
        payload = response.json()
        self.assertEqual(
            payload,
            {"Error": ["Mandatory \"title\" parameter is missing."]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)