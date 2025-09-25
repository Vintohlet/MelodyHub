-- -- Топ-10 стран по суммарной выручке
select c.country, sum(i.total)
from invoice i
join customer c on i.customer_id = c.customer_id
group by c.country
order by sum(i.total) desc
limit 10;

-- Кто принёс больше всего денег магазину
SELECT c.first_name || ' ' || c.last_name AS customer,
       ROUND(SUM(i.Total), 2) AS total_spent
FROM Invoice i
JOIN Customer c ON i.Customer_id = c.Customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- Какие жанры покупают чаще всего
SELECT g.Name AS genre, COUNT(il.track_id) AS tracks_sold
FROM invoice_line il
JOIN Track t ON il.track_id = t.track_id
JOIN Genre g ON t.genre_id = g.genre_id
GROUP BY g.Name
ORDER BY tracks_sold DESC
LIMIT 10;

-- Сравнение цен на музыку по жанрам
SELECT g.Name AS genre, ROUND(AVG(il.unit_price), 2) AS avg_price
FROM invoice_line il
JOIN Track t ON il.track_Id = t.track_Id
JOIN Genre g ON t.genre_Id = g.Genre_Id
GROUP BY g.Name
ORDER BY avg_price DESC;

-- Сравнение цен на музыку по жанрам
SELECT g.Name AS genre, ROUND(AVG(il.unit_price), 2) AS avg_price
FROM invoice_line il
JOIN Track t ON il.track_id = t.track_id
JOIN Genre g ON t.genre_id = g.genre_id
GROUP BY g.Name
ORDER BY avg_price DESC;

-- Какие жанры содержат самые длинные и короткие треки
SELECT g.Name AS genre, ROUND(AVG(t.Milliseconds) / 60000.0, 2) AS avg_length_min
FROM Track t
JOIN Genre g ON t.genre_id = g.genre_id
GROUP BY g.Name
ORDER BY avg_length_min DESC;

-- Альбомы, которые принесли наибольшую выручку
SELECT a.Title AS album, ar.Name AS artist, ROUND(SUM(il.unit_price * il.Quantity), 2) AS revenue
FROM invoice_line il
JOIN Track t ON il.track_id = t.track_id
JOIN Album a ON t.Album_Id = a.Album_Id
JOIN Artist ar ON a.Artist_Id = ar.Artist_Id
GROUP BY a.album_id, a.Title, ar.Name
ORDER BY revenue DESC
LIMIT 10;

-- Сколько денег приносил магазин по годам
select extract(year from i.invoice_date) as year,
       round(sum(i.total), 2) as revenue
from invoice i
group by year
order by year;

-- Сравнение покупательной способности по странам
SELECT c.Country, ROUND(AVG(i.Total), 2) AS avg_invoice
FROM Invoice i
JOIN Customer c ON i.customer_id = c.customer_id
GROUP BY c.Country
ORDER BY avg_invoice DESC
LIMIT 10;

-- Какие исполнители продаются лучше всего
SELECT ar.Name AS artist, ROUND(SUM(il.unit_price * il.Quantity), 2) AS revenue
FROM invoice_line il
JOIN Track t ON il.track_id = t.track_id
JOIN Album a ON t.album_id = a.album_id
JOIN Artist ar ON a.artist_id = ar.artist_id
GROUP BY ar.Name
ORDER BY revenue DESC
LIMIT 10;

-- Отбор треков с максимальной ценой
SELECT t.Name AS track, g.Name AS genre, il.unit_price
FROM invoice_line il
JOIN Track t ON il.track_id = t.track_id
JOIN Genre g ON t.genre_id = g.genre_id
ORDER BY il.unit_price DESC
LIMIT 10;


