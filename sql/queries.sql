
SELECT date, product_id, SUM(units) AS units, AVG(price) AS avg_price, SUM(revenue) AS revenue
FROM sales
GROUP BY date, product_id
ORDER BY date;


SELECT s.date, p.promo_name, s.product_id, s.units, s.price, s.revenue
FROM sales s
LEFT JOIN promotions p ON s.promo_id = p.promo_id
WHERE date BETWEEN '2020-01-01' AND '2020-12-31';
