{{ config(materialized='table') }}

select
    date_trunc('day', order_time) as date,
    count(*) as total_orders,
    sum(total_amount) as total_revenue,
    sum(case when is_paid then total_amount else 0 end) as paid_revenue
from {{ ref('fact_orders') }}
group by 1