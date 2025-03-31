/*
  Example transformation model.
  Replace with your actual transformation logic.
*/

WITH source_data AS (
  SELECT 
    id,
    name,
    timestamp,
    value
  FROM {{ source('source_name', 'table_name_1') }}
),

transformed AS (
  SELECT
    id,
    name,
    TIMESTAMP(timestamp) AS timestamp,
    CAST(value AS FLOAT64) AS numeric_value,
    -- Add additional transformations here
    CURRENT_TIMESTAMP() AS model_run_time
  FROM source_data
)

SELECT * FROM transformed
