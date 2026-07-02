-- GridPulse 
-- Catalog: AwsDataCatalog | Database: gridpulse_db | Table: energy_curated


SHOW TABLES IN gridpulse_db;


SELECT *
FROM gridpulse_db.energy_curated
LIMIT 10;

-- Sanity check: row count and year range
SELECT
    MIN(year) AS earliest_year,
    MAX(year) AS latest_year,
    COUNT(*) AS total_rows
FROM gridpulse_db.energy_curated;

-- Current U.S. renewable share and carbon intensity (most recent year)
SELECT
    country,
    year,
    renewables_share_elec,
    carbon_intensity_elec,
    renewables_share_yoy_change
FROM gridpulse_db.energy_curated
WHERE country = 'United States'
ORDER BY year DESC
LIMIT 1;

-- Top 10 countries by renewable share in the most recent year
SELECT
    country,
    renewables_share_elec
FROM gridpulse_db.energy_curated
WHERE year = (SELECT MAX(year) FROM gridpulse_db.energy_curated)
ORDER BY renewables_share_elec DESC
LIMIT 10;

-- U.S. generation mix over time (feeds the Tableau stacked area chart)
SELECT
    year,
    coal_electricity,
    gas_electricity,
    oil_electricity,
    nuclear_electricity,
    hydro_electricity,
    wind_electricity,
    solar_electricity,
    other_renewable_electricity
FROM gridpulse_db.energy_curated
WHERE country = 'United States'
ORDER BY year;
