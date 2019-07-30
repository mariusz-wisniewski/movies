from rest_framework import serializers
from .models import Movie, Comment


class MovieSerializers(serializers.ModelSerializer):
    comments = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='comment'
    )

    class Meta:
        model = Movie
        fields = ('id', 'title', 'details', 'comments')


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie_id', 'comment')
