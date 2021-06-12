
use Covid19;

if(OBJECT_ID(N'create_continent') IS NOT NULL)
    begin
        drop procedure create_continent;
    end
go

create procedure create_continent
    @name varchar(50),
    @new_identity int = null output
as begin
    set nocount on;
    insert into Continent (con_name) values (@name);
    set @new_identity = SCOPE_IDENTITY();
end
go

if(OBJECT_ID(N'create_country') IS NOT NULL)
    begin
        drop procedure create_country;
    end
go

create procedure create_country
    @continent int,
    @iso_code varchar(20),
    @name varchar(50),
    @new_identity int = null output
as begin
    set nocount on;
    insert into Country (con_id, cty_iso_code, cty_location) values (@continent, @iso_code, @name);
    set @new_identity = SCOPE_IDENTITY();
end
go

if(OBJECT_ID(N'create_cases') IS NOT NULL)
    begin
        drop procedure create_cases;
    end
go

create procedure create_cases
    @country int,
    @date date,
    @total_cases int,
    @new_cases int,
    @total_deaths int,
    @new_deaths int,
    @reproduction_rate float
as begin
    set nocount on;
    insert into Cases (
        cty_id,
        cas_date,
        cas_total_cases,
        cas_new_cases,
        cas_total_deaths,
        cas_new_deaths,
        cas_reproduction_rate
    ) values (
         @country,
         @date,
         @total_cases,
         @new_cases,
         @total_deaths,
         @new_deaths,
         @reproduction_rate
     );
end
go