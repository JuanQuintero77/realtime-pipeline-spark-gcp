{{ config(materialized='view') }}

select * 
from read_parquet('/home/juan/projects/proyecto-ecommerce/data/silver/orders/**/*.parquet')