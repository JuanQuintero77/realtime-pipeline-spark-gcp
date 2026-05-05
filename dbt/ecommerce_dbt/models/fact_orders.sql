{{ config(materialized='table') }}

select
    o.order_id,
    o.user_id,
    o.event_timestamp as order_time,
    o.total_amount,

    p.payment_method,
    p.amount as paid_amount,

    case 
        when p.order_id is not null then true
        else false
    end as is_paid

from {{ ref('stg_orders') }} o
left join {{ ref('stg_payments') }} p
    on o.order_id = p.order_id