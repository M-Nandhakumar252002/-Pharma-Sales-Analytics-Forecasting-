-- ============================================================
-- Create Database and Use It
-- ============================================================
CREATE DATABASE IF NOT EXISTS pharma_sales;
USE pharma_sales;

-- ============================================================
-- Drop old table if exists
-- ============================================================
DROP TABLE IF EXISTS sales_daily;

-- ============================================================
-- Create Table based on salesdaily.csv structure
-- ============================================================
CREATE TABLE sales_daily (
    id INT AUTO_INCREMENT PRIMARY KEY,
    datum DATE NOT NULL,
    M01AB DECIMAL(10,2),
    M01AE DECIMAL(10,2),
    N02BA DECIMAL(10,2),
    N02BE DECIMAL(10,2),
    N05B DECIMAL(10,2),
    N05C DECIMAL(10,2),
    R03 DECIMAL(10,2),
    R06 DECIMAL(10,2),
    Year INT NOT NULL,
    Month INT NOT NULL,
    Hour INT NOT NULL,
    Weekday_Name VARCHAR(20)
);

-- ============================================================
-- Forecasting & Analytics Queries (MySQL)
-- Save this file as pharma_forecasting.sql
-- ============================================================

------------------------------------------------------------
-- 1. Monthly Aggregates for Forecasting
------------------------------------------------------------
CREATE OR REPLACE VIEW monthly_sales AS
SELECT 
    Year,
    Month,
    SUM(M01AB + M01AE + N02BA + N02BE + N05B + N05C + R03 + R06) AS total_sales
FROM sales_daily
GROUP BY Year, Month
ORDER BY Year, Month;

------------------------------------------------------------
-- 2. Moving Average Forecast (3-month window)
------------------------------------------------------------
SELECT 
    Year,
    Month,
    total_sales,
    ROUND(AVG(total_sales) OVER (
        ORDER BY Year, Month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_forecast
FROM monthly_sales;

------------------------------------------------------------
-- 3. Month-over-Month Growth Rate
------------------------------------------------------------
SELECT 
    Year,
    Month,
    total_sales,
    ROUND(
        (total_sales - LAG(total_sales) OVER (ORDER BY Year, Month)) * 100.0 / 
        LAG(total_sales) OVER (ORDER BY Year, Month), 
        2
    ) AS mom_growth_rate
FROM monthly_sales;

------------------------------------------------------------
-- 4. Seasonal Trends (Quarterly)
------------------------------------------------------------
SELECT 
    Year,
    QUARTER(STR_TO_DATE(CONCAT(Year,'-',Month,'-01'), '%Y-%m-%d')) AS Quarter,
    SUM(total_sales) AS quarterly_sales
FROM monthly_sales
GROUP BY Year, Quarter
ORDER BY Year, Quarter;

------------------------------------------------------------
-- 5. Day-of-Week Effect
------------------------------------------------------------
SELECT 
    Weekday_Name,
    ROUND(AVG(M01AB + M01AE + N02BA + N02BE + N05B + N05C + R03 + R06), 2) AS avg_sales
FROM sales_daily
GROUP BY Weekday_Name
ORDER BY FIELD(Weekday_Name,'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');

------------------------------------------------------------
-- 6. Drug-Wise Trends
------------------------------------------------------------
SELECT 
    Year,
    Month,
    ROUND(SUM(M01AB),2) AS total_M01AB,
    ROUND(SUM(M01AE),2) AS total_M01AE,
    ROUND(SUM(N02BA),2) AS total_N02BA,
    ROUND(SUM(N02BE),2) AS total_N02BE,
    ROUND(SUM(N05B),2) AS total_N05B,
    ROUND(SUM(N05C),2) AS total_N05C,
    ROUND(SUM(R03),2) AS total_R03,
    ROUND(SUM(R06),2) AS total_R06
FROM sales_daily
GROUP BY Year, Month
ORDER BY Year, Month;

------------------------------------------------------------
-- 7. Simple Forecast for Next Month (Naive)
-- Using last available month’s sales as next month’s forecast
------------------------------------------------------------
SELECT 
    MAX(Year) AS last_year,
    MAX(Month) AS last_month,
    SUM(M01AB + M01AE + N02BA + N02BE + N05B + N05C + R03 + R06) AS last_month_sales,
    SUM(M01AB + M01AE + N02BA + N02BE + N05B + N05C + R03 + R06) AS forecast_next_month
FROM sales_daily
WHERE (Year, Month) = (
    SELECT Year, Month FROM sales_daily ORDER BY Year DESC, Month DESC LIMIT 1
);

------------------------------------------------------------
-- 8. Yearly Growth Trend
------------------------------------------------------------
SELECT 
    Year,
    SUM(M01AB + M01AE + N02BA + N02BE + N05B + N05C + R03 + R06) AS yearly_sales,
    ROUND(
        (SUM(M01AB + M01AE + N02BA + N02BE + N05B + N05C + R03 + R06) - 
         LAG(SUM(M01AB + M01AE + N02BA + N02BE + N05B + N05C + R03 + R06)) 
         OVER (ORDER BY Year)) * 100.0 / 
         LAG(SUM(M01AB + M01AE + N02BA + N02BE + N05B + N05C + R03 + R06)) 
         OVER (ORDER BY Year), 
        2
    ) AS yoy_growth_rate
FROM sales_daily
GROUP BY Year
ORDER BY Year;

------------------------------------------------------------
-- 9. Top 3 Best Performing Drug Categories (Revenue Share)
------------------------------------------------------------
SELECT 
    'M01AB' AS drug, ROUND(SUM(M01AB),2) AS total_sales FROM sales_daily
UNION ALL
SELECT 'M01AE', ROUND(SUM(M01AE),2) FROM sales_daily
UNION ALL
SELECT 'N02BA', ROUND(SUM(N02BA),2) FROM sales_daily
UNION ALL
SELECT 'N02BE', ROUND(SUM(N02BE),2) FROM sales_daily
UNION ALL
SELECT 'N05B', ROUND(SUM(N05B),2) FROM sales_daily
UNION ALL
SELECT 'N05C', ROUND(SUM(N05C),2) FROM sales_daily
UNION ALL
SELECT 'R03', ROUND(SUM(R03),2) FROM sales_daily
UNION ALL
SELECT 'R06', ROUND(SUM(R06),2) FROM sales_daily
ORDER BY total_sales DESC
LIMIT 3;
