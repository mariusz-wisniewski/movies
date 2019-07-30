# API Specification 
Following project support three endpoint:

## Content
1. [Movies](#movies)
    - POST
    - GET
2. [Comments](#comments)
    - POST
    - GET
3. [Top](#top)

## Movies

### Creating a movie:
```POST /movies```

Request:

  | Attribute                | Description                                                                        | Optional |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `title`                  | The title of the movie - max 255 chars.                                            | no       |

Responses:
- 201 - movie created

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `id`                     | The ID of the movie.                                                               | no       |
  | `title`                  | The title of the movie received from OMDB API.                                     | no       |
  | `details`                | Dynamic object containing movie's details retrieved from OMDB API.                 | no       |

- 400 - bad request (no title specified/empty title/)

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `title`                  | Error message.                                                                     | no       |
- 409 - movie with given title exists

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `title`                  | Error message.                                                                     | no       |
- 500 - OMDB Authorization error - not valid API key. Movie cannot be created

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `OMDB API`               | Error message.                                                                     | no       |
- 503 - OMDB API unavailable or returns an error. Movie cannot be created

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `OMDB API`               | Error message.                                                                     | no       |

### Getting movie/movies:
```GET /movies```

Query params:

  | Param                    | Description                                                                        | Optional |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `title`                  | The tile of the movie.                                                             | yes      |

Response:
200 - ok

List of movies:

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `id`                     | The ID of the movie.                                                               | no       |
  | `title`                  | The title of the movie received from OMDB API.                                     | no       |
  | `details`                | Dynamic object containing movie's details retrieved from OMDB API.                 | no       |

### Getting list of single movie:

```GET /movies/?movie_id=1```

Response:
200 - ok

Movie details 

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `id`                     | The ID of the movie.                                                               | no       |
  | `title`                  | The title of the movie received from OMDB API.                                     | no       |
  | `details`                | Dynamic object containing movie's details retrieved from OMDB API.                 | no       |

## Comments

### Creating a comment:

```POST /comments```

Request:

  | Attribute                | Description                                                                        | Optional |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `movie_id`               | The ID of the [movie](#movies).                                                    | no       |
  | `comment`                | Comment to the movie.                                                              | no       |

Responses:
* 201 - comment created
  
  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `id`                     | The ID of the comment.                                                             | no       |
  | `movie_id`               | The ID of the movie.                                                               | no       |
  | `comment`                | Comment to the movie.                                                              | no       |
* 400 - bad request (no/empty comment)

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `comment`                | Array with `comment` related errors details.                                       | yes*     |
  
  * at least one of the attributes must not be null
  
* 415 - POST sent with inproper content type

### Getting list of comments:

```GET /comments```

Query params:

  | Param                    | Description                                                                        | Optional |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `movie_id`               | The ID of the movie.                                                               | yes      |

Responses:
* 200 - ok

List of comments:
  
  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `id`                     | The ID of the comment.                                                             | no       |
  | `movie_id`               | The ID of the movie.                                                               | no       |
  | `comment`                | Comment to the movie.                                                              | no       |
* 404 - movie with given `movie_id` not found

## Top

Return 5 movies with the greatest rank. Rank is calculated based on the number of comments in given time period.

```GET /top```

Query params:

  | Param                    | Description                                                                        | Optional |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `start`                  | Period start date in format `YYYY-MM-DD`                                           | yes      |
  | `end`.                   | Period end date in format `YYYY-MM-DD`                                             | yes      |

Responses:
* 200 - ok

  List of top movies:
  
  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `movie_id`               | The ID of the movie.                                                               | no       |
  | `total_comments`         | Number of comment written in given time period                                     | no       |
  | `rank`                   | Rank calculated based on total_comments                                            | no       |
  
* 400 - bad request - `start` or `end` params are given in wrong format

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `error`                  | Error details.                                                                     | no       |
 
* 404 - missing `start` or `end` param

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `error`                  | Error details.                                                                     | no       |
