# Analysis-tool

analysis-tool is a python tool written for a newspaper site to discover what kind of articles the site's readers like.
This tool answers three simple questions:

- What are the most popular three articles of all time?
- Who are the most popular article authors of all time?
- On which days did more than 1% of requests lead to errors?

# Usage

To run the code you must have the news database **AND CREATE THE VIEWS BELOW**
then type in terminal:
`$ python3 analysis-tool.py`
voilà it prints out the results

# Used Views

- ## ArticleViews:
  It's a view of every **article** and its **views** sorted in a _descending_ order.
  ````
   CREATE VIEW articleViews AS SELECT articles.title,
          sum(view.num) AS views
         FROM articles,
          ( SELECT log.path,
                  count(*) AS num
                 FROM log
                WHERE log.path LIKE '/article/%' AND log.status LIKE '2%'
                GROUP BY log.path
                ORDER BY num) AS view
        WHERE view.path LIKE concat('%', articles.slug, '%')
        GROUP BY articles.title
        ORDER BY views DESC;
        ```

  ````
- ## AuthorsView
  It's a view of every **author** and _the sum_ of his **articles' views** sorted in a _descending_ order.
  ```
    CREATE VIEW authorsView AS SELECT a.name,
      sum(b.views) AS views
     FROM ( SELECT authors.name,
              articles.title
             FROM authors,
              articles
            WHERE authors.id = articles.author) AS a,
      articleviews AS b
    WHERE a.title = b.title
    GROUP BY a.name
    ORDER BY (views) DESC;
  ```
- ## ErrorView
  It's a view of **each day** in the logs and its **Error rate** sorted in a _descending_ order.
  ```
  CREATE VIEW errorView AS SELECT a.day,
  round(a.errors * 100.0 / b.total * 1.0, 5) AS percent
  FROM ( SELECT CAST(time AS DATE) AS day,
          count(*) AS errors
         FROM log
        WHERE NOT log.status LIKE '2%'
        GROUP BY day) AS a,
  ( SELECT CAST(time AS DATE) AS day,
          count(*) AS total
         FROM log
        GROUP BY day) AS b
  WHERE a.day = b.day
  ORDER BY percent DESC;
  ```
