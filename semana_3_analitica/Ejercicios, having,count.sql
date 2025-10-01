-- 1. Agregaciones con GROUP BY y HAVING 
--Calcula por cada región y canal de venta el número de ventas realizadas, el total de unidades vendidas y la facturación total. 
--Filtra sólo las combinaciones región mas canal donde la facturación total supere los 50.000 
--y se hayan realizado más de 50 ventas. Ordena los resultados de mayor a menor facturación.

SELECT r.region_name, sc.channel_name, 
	   COUNT (s.sale_id) AS numero_ventas, 
	   SUM(s.quantity_sold) AS unidades_vendidas,
	   SUM (s.sales_amount) AS facturacion_total
FROM Sales.sales s
INNER JOIN Sales.sales_reps sr 	   ON sr.sales_rep_id = s.sales_rep_id 
INNER JOIN Sales.regions r     	   ON r.region_id = sr.region_id
INNER JOIN Sales.sales_channels sc ON sc.sales_channel_id = s.sales_channel_id 
GROUP BY r.region_name, sc.channel_name
HAVING 	SUM(s.sales_amount) > 50000
    	AND COUNT(s.sale_id) > 50
ORDER BY facturacion_total DESC;


--2. Subconsulta Correlacionada
--Lista los productos cuyo precio unitario es superior al precio promedio de su misma 
--categoría. Muestra el identificador del producto, la categoría y el precio unitario, 
--ordenados de mayor a menor precio.
SELECT p.product_id, pc.category_name, p.unit_price 
FROM sales.products AS p
INNER JOIN sales.product_categories AS pc
	ON pc.product_category_id = p.product_category_id
WHERE p.unit_price > (SELECT AVG(p2.unit_price) AS Promedio
					  FROM sales.products AS p2 
					  WHERE p.product_category_id = p2.product_category_id)
ORDER BY p.unit_price DESC

--3 CTE (WITH) para agregación mensual
--Calcula la facturación mensual por región agrupando por mes y nombre de región 
--y muestra todos los registros ordenados por mes y región. 
WITH ventas_mensuales AS (
    SELECT 
        DATE_TRUNC('month', s.sale_date) AS mes,
        r.region_name,
        SUM(s.sales_amount) AS facturacion_mensual
FROM Sales.sales s
JOIN Sales.sales_reps sr ON s.sales_rep_id = sr.sales_rep_id
JOIN Sales.regions r     ON sr.region_id = r.region_id
GROUP BY mes, r.region_name
)
SELECT * FROM ventas_mensuales
ORDER BY mes, region_name;



-- 4.Función Ventana ROW_NUMBER 
--Obtén para cada vendedor la primera venta que realizó cronológicamente. 
--Muestra el nombre del vendedor, la fecha de venta y el monto.
SELECT * FROM  (SELECT ROW_NUMBER() OVER (PARTITION BY sr.sales_rep_name 
						  ORDER BY s.sale_date ASC) AS RN ,
sr.sales_rep_name,  s.sale_date, SUM (s.sales_amount) AS Amount
FROM sales.sales AS s 
INNER JOIN sales.sales_reps AS sr 
	ON s.sales_rep_id = sr.sales_rep_id
GROUP BY sr.sales_rep_name,  s.sale_date)
WHERE rn = 1


--4.1 Obtén las 3 ventas más grandes en cada región.

SELECT * FROM (SELECT ROW_NUMBER() OVER (PARTITION BY r.region_name
						  			     ORDER BY s.sales_amount DESC) AS rn,
r.region_name, s.sales_amount FROM sales.sales AS s 
INNER JOIN sales.sales_reps AS sr 
	ON s.sales_rep_id = sr.sales_rep_id
INNER JOIN sales.regions AS r
	ON sr.region_id = r.region_id)
WHERE rn <= 3

-- 5. Función Ventana RANK
--Determina los tres productos con mayor facturación dentro de cada categoría.
--Muestra la categoría, el identificador del producto y la facturación.


WITH rankin AS (SELECT RANK() OVER (ORDER BY p.unit_price DESC) AS Rk,
pc.category_name, p.product_id, p.unit_price FROM sales.product_categories AS pc
INNER JOIN sales.products AS p
	ON pc.product_category_id = p.product_category_id)
SELECT * FROM rankin 
WHERE rk <=3


--6.Función Ventana LAG 
--Para cada región, calcula la facturación mensual y la diferencia respecto al mes 
--anterior. Debes mostrar el nombre de la región, el mes, la facturación, la 
--facturación del mes anterior y la variación entre ambas.

WITH Ventas_mensuales AS (
SELECT r.region_name, CONCAT(DATE_PART('year',s.sale_date),'-',DATE_PART('month',s.sale_date)) AS mes,
		SUM (s.sales_amount) AS Facturacion
FROM sales.sales AS s
INNER JOIN sales.sales_reps AS sr
	ON s.sales_rep_id = sr.sales_rep_id 
INNER JOIN sales.regions AS r
	ON sr.region_id = r.region_id
GROUP BY r.region_name, mes
ORDER BY r.region_name, mes
)
SELECT region_name, mes,Facturacion,
LAG(Facturacion) OVER(ORDER BY region_name) AS facturcion_mes_anterior,
Facturacion - LAG(Facturacion) OVER(ORDER BY region_name) AS Variacion
FROM Ventas_mensuales


--7. Función Ventana LEAD 
--Para cada producto, muestra la fecha de su próxima venta después de cada 
--registro. Debes mostrar el identificador del producto, la fecha de la venta actual y 
--la fecha de la próxima venta. 

SELECT p.product_id, s.sale_date,
	   LEAD(s.sale_date) OVER(PARTITION BY p.product_id ORDER BY s.sale_date ) AS Prox_venta
FROM sales.sales AS s
INNER JOIN sales.products AS p
	ON s.product_id = p.product_id



---8. Función Ventana de Participación (%) 
--Calcula el porcentaje de facturación de cada vendedor dentro de su región. Debes 
--mostrar la región, el nombre del vendedor, la facturación y su participación 
--porcentual dentro de la región.


SELECT sr.sales_rep_name, r.region_name , SUM(sales_amount) AS facturacion, facturacion_total,
		(SUM(sales_amount) / facturacion_total) *100 AS Porcentaje_participacion
FROM sales.sales AS s
INNER JOIN sales.sales_reps AS sr
	ON s.sales_rep_id = sr.sales_rep_id
INNER JOIN sales.regions AS r
	ON sr.region_id = r.region_id
   INNER JOIN 
		(SELECT r.region_name , SUM(sales_amount) AS facturacion_total
		 FROM sales.sales AS s
		 INNER JOIN sales.sales_reps AS sr
			ON s.sales_rep_id = sr.sales_rep_id
		 INNER JOIN sales.regions AS r
			ON sr.region_id = r.region_id
		GROUP BY r.region_name) AS mt
	ON r.region_name = mt.region_name

GROUP BY r.region_name, sr.sales_rep_name, facturacion_total
ORDER BY sr.sales_rep_name


--9. HAVING con medidas mixtas 
--Obtén las categorías de producto cuyo ticket promedio sea mayor a 300 y en las 
--que se hayan vendido al menos 1.000 unidades. Muestra la categoría, el ticket 
--promedio y las unidades vendidas.
SELECT pc.category_name,
    AVG(s.sales_amount) AS ticket_promedio,
    SUM(s.quantity_sold) AS unidades_vendidas
FROM Sales.sales s
JOIN Sales.products p ON s.product_id = p.product_id
JOIN Sales.product_categories pc ON p.product_category_id = pc.product_category_id
GROUP BY pc.category_name
HAVING AVG(s.sales_amount) > 300
   AND SUM(s.quantity_sold) >= 1000

--10. Promedio Móvil con Función Ventana 
--Calcula la facturación mensual total y el promedio móvil de 3 meses.
--Muestra el mes, la facturación y el promedio móvil de 3 meses.

WITH facturacion_mensual AS (
  SELECT DATE_TRUNC('month', s.sale_date) AS mes,
      	 SUM(s.sales_amount) AS facturacion
   FROM Sales.sales s
   GROUP BY DATE_TRUNC('month', s.sale_date)
)
SELECT mes,facturacion, 
ROUND(AVG(facturacion) OVER (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS promedio_movil_3m
FROM facturacion_mensual
ORDER BY mes





