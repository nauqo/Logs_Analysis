# Log Analysis Project
This is the third project for the Full stack web developer nanodegree program at [udacity](https://udacity.com/).

The assignment are to fetch data from a database using python as the programing language.

The data to fetch are
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### Getting Started

##### Views

There are two views that were used for this project and must be created in order for the program to work correctly.

```
CREATE VIEW totalrequests AS
SELECT DATE_TRUNC('day', time) AS day,
       COUNT(time) AS requests
FROM log
GROUP BY day
ORDER BY day;
```

```
CREATE VIEW totalerrors AS
SELECT DATE_TRUNC('day', time) AS day,
       COUNT(time) AS errors
FROM log
WHERE status = '404 NOT FOUND'
GROUP BY day
ORDER BY day;
```

##### How to start
To start the program you only need to run the **log.py** file using your favorite terminal shell.

```
python log.py
```

### Design
All the heavy work were done by the SQL querry using joins, aggregations, and where clause to extract the informations needed for python to only print.

##### Three most popular articles
To get the three most popular articles were achived by joining the tables `articles` and `log` .

The `articles.slug` where used to match each `log.path` to get the desired numbers.
```
SELECT articles.title,
       count(log.path) as views
FROM articles, log
WHERE log.path like ('%' || articles.slug)
GROUP BY articles.title
ORDER BY views DESC
LIMIT 3;
```

##### Most popular authors
Almost the same as the article querry, but need the `authors` table and adding `authors.id = articles.author` to get all articles written by the same author to be added to the author.
```
SELECT authors.name,
       count(log.path) as num
FROM log, articles, authors
WHERE log.path LIKE ('%' || articles.slug)
      AND authors.id = articles.author
GROUP BY authors.name
ORDER BY num DESC;
```

##### Day(s) leading to more than 1%
To get this, two views were added.
The `totalrequests` view were to get total number of requests for each day.
The `totalerrors` view were to get total errors for each day.

A simply division could then be used that will lead to number of procentage of errors

```
SELECT totalrequests.day,
       round(100*totalerrors.errors::decimal/totalrequests.requests, 2) AS fail
FROM totalerrors, totalrequests
WHERE totalrequests.day = totalerrors.day
AND (totalerrors.errors::decimal/totalrequests.requests > 0.01);
```
