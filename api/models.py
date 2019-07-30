from django.db import models
from django.contrib.postgres.fields import JSONField


class Movie(models.Model):
    # Max_length set to 255 seems to be safe. Longest movie title
    # (based on https://www.filmcomment.com/article/top-20-longest-movie-titles/) is 229
    title = models.CharField(max_length=255)
    # Details stores all movie information returned by omdbapi
    details = JSONField()


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    # creation timestamp
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
