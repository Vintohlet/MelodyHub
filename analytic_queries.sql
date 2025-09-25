-- name: q1
SELECT g.Name AS genre, COUNT(il.track_id) AS tracks_sold
FROM invoice_line il
JOIN Track t ON il.track_id = t.track_id
JOIN Genre g ON t.genre_id = g.genre_id
GROUP BY g.Name
ORDER BY tracks_sold DESC
LIMIT 10;

-- name: q2
SELECT a.Title AS album, ar.Name AS artist, 
       ROUND(SUM(il.unit_price * il.Quantity), 2) AS revenue
FROM invoice_line il
JOIN Track t ON il.track_id = t.track_id
JOIN Album a ON t.album_id = a.album_id
JOIN Artist ar ON a.artist_id = ar.artist_id
GROUP BY a.album_id, a.Title, ar.Name
ORDER BY revenue DESC
LIMIT 10;

-- name: q3
SELECT c.Country, ROUND(SUM(i.Total), 2) AS revenue
FROM Invoice i
JOIN Customer c ON i.Customer_id = c.Customer_id
JOIN Invoice_Line il ON i.Invoice_Id = il.Invoice_Id
GROUP BY c.Country
ORDER BY revenue DESC
LIMIT 10;

-- name: q4
SELECT EXTRACT(YEAR FROM i.Invoice_Date) AS year,
       ROUND(SUM(il.Unit_Price * il.Quantity), 2) AS revenue
FROM Invoice i
JOIN Invoice_Line il ON i.Invoice_Id = il.Invoice_Id
JOIN Track t ON il.Track_Id = t.Track_Id
GROUP BY year
ORDER BY year;

-- name: q5
SELECT g.Name AS genre, ROUND(AVG(t.Milliseconds) / 60000.0, 2) AS avg_length_min
FROM Track t
JOIN Genre g ON t.Genre_Id = g.Genre_Id
JOIN Invoice_Line il ON t.Track_Id = il.Track_Id
GROUP BY g.Name
ORDER BY avg_length_min DESC;

-- name: q6
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer,
    MIN(i.invoice_date) AS first_purchase,
    MAX(i.invoice_date) AS last_purchase,
    ROUND(SUM(il.unit_price * il.quantity), 2) AS revenue
FROM Customer c
JOIN Invoice i ON c.customer_id = i.customer_id
JOIN Invoice_Line il ON i.invoice_id = il.invoice_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY revenue DESC
LIMIT 20;

