
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

if(OBJECT_ID(N'create_tests') IS NOT NULL)
    begin
        drop procedure create_tests;
    end
go

create procedure create_tests
    @country int,
    @date date,
    @new_tests int,
    @total_tests int,
    @positive_rate int
as begin
    set nocount on;
    insert into Tests (
        cty_id,
        tes_date,
        tes_new_tests,
        tes_total_tests,
        tes_positive_rate
    ) values (
         @country,
         @date,
         @new_tests,
         @total_tests,
         @positive_rate
     );
end
go

if(OBJECT_ID(N'create_vaccinations') IS NOT NULL)
    begin
        drop procedure create_vaccinations;
    end
go

create procedure create_vaccinations
    @country int,
    @date date,
    @total_vaccinations int,
    @people_vaccinated int,
    @people_fully_vaccinated int,
    @new_vaccinations int
as begin
    set nocount on;
    insert into Vaccinations (
        cty_id,
        vac_date,
        vac_total_vaccinations,
        vac_people_vaccinated,
        vac_people_fully_vaccinated,
        vac_new_vaccinations
    ) values (
         @country,
         @date,
         @total_vaccinations,
         @people_vaccinated,
         @people_fully_vaccinated,
         @new_vaccinations
     );
end
go