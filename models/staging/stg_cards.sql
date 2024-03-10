

with source as (
    
    {#-
    Normally we would select from the table here, but we are using seeds to load
    our data in this project
    #}
    select * from {{ source('api', 'raw_cards') }}

),

renamed as (

    select
       *
    from source

)

select * from renamed
