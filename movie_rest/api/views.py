from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, status, mixins, viewsets
from django.db.models import Case, F, Sum, When
from django.db.models.expressions import Window
from django.db.models.fields import IntegerField
from django.db.models.functions import DenseRank, Coalesce
from .models import Movie, Comment
from .serializers import MovieSerializers, CommentSerializers
from requests.exceptions import ConnectionError, HTTPError
import omdb, json, datetime
from movie_rest import settings

# Create your views here.


class MovieView(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')

        # Verify mandatory "title" parameter
        if title is None or title.strip() == "":
            return Response({
                'Error': ['Mandatory "title" parameter is missing.']
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(title) > 255:
            return Response({
                'Error': ['Title is too long, maximum size is 255.']
            }, status=status.HTTP_400_BAD_REQUEST)
        title = title.strip()

        # Set omdb client properties
        omdb.set_default('apikey', settings.OMDB_API_KEY)
        omdb.set_default('timeout', settings.OMDB_API_TIMEOUT)

        # Check if movie with given title exists
        if Movie.objects.filter(title=title).exists():
            return Response({
                'Error': ['Movie with given title already exists.']
            }, status=status.HTTP_409_CONFLICT)

        try:
            omdb_response = json.loads(omdb.request(t=title).content)
        except ConnectionError as e:
            return Response({
                'OMDBAPI': [
                    'External service is unavailable. Please try again later.',
                ],
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except HTTPError as e:
            return Response({
                'OMDBAPI': [
                    json.loads(e.response.content)["Error"],
                ],
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        omdb_response.pop('Title', None)  # Removing title for details. Title is stored on root level

        # Check if movie with given title exists in omdb
        if omdb_response['Response'] == 'False':
            return Response({
                'OMDBAPI': [
                    omdb_response['Error']
                ],
            }, status=status.HTTP_400_BAD_REQUEST)
        movie = Movie(title=title, details=omdb_response)
        movie.save()
        return Response(MovieSerializers(movie).data, status.HTTP_201_CREATED)

    def get_queryset(self):
        query_set = Movie.objects.all()
        title = self.request.query_params.get('title', None)

        if title is None:
            return query_set
        else:
            return Movie.objects.filter(title=title)


class CommentView(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentSerializers

    def get_queryset(self):
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id is None:
            return Comment.objects.all()
        else:
            try:
                movie_id = int(movie_id)
            except ValueError:
                raise exceptions.ValidationError({
                    'movie_id': [
                        'Incorrect movie_id type. Expected int.',
                    ],
                })
            query_set = Comment.objects.filter(movie_id=movie_id)
            if not query_set:
                raise exceptions.ValidationError({
                    'movie_id': [
                        'Movie with given is was not found.',
                    ],
                })
            return query_set


class TopMovies(APIView):
    def get_dates(self, request):
        start_date = request.query_params.get('start', None)
        end_date = request.query_params.get('end', None)

        # Check for mandatory top request parameters
        if start_date is None:
            raise exceptions.NotFound('Query parameter "start" not found.')
        if end_date is None:
            raise exceptions.NotFound('Query parameter "end" not found.')

        # Check if date format is valid
        format = '%Y-%m-%d'
        try:
            start_date = datetime.datetime.strptime(start_date, format)
        except ValueError:
            raise exceptions.ValidationError('Please verify "start" parameter. Expected format: YYYY-MM-DD')

        try:
            end_date = datetime.datetime.strptime(end_date, format)
            # Coalesce used in query does not include last day so that we need to add one day
            end_date += datetime.timedelta(days=1)
        except ValueError:
            raise exceptions.ValidationError('Please verify "end" parameter. Expected format: YYYY-MM-DD')

        if end_date <= start_date:
            raise exceptions.ValidationError('Start date have to be less than or equal end date')

        return start_date, end_date

    def get(self, request):
        start_date, end_date = self.get_dates(request)

        """ Query assign rank based on the number of comment written in given time range 
            and returns five movies with greatest rank """

        movies_query = Movie.objects.annotate(
            total_comments=Coalesce(
                Sum(Case(
                    When(comments__created__range=[start_date, end_date], then=1),
                    output_field=IntegerField()
                )),
                0
            ),
            rank=Window(
                expression=DenseRank(),
                order_by=F('total_comments').desc(),
            )
        ).order_by('-total_comments', 'id')[:5]

        movies = [
            {
                'movie_id': movie.id,
                'total_comments': movie.total_comments,
                'rank': movie.rank
            } for movie in movies_query
        ]
        return Response(movies)
