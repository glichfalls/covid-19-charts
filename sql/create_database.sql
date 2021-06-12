-- create database

use master;
go

if(DB_ID(N'Covid19') IS NOT NULL)
    begin
        alter database Covid19 set offline with rollback immediate
        drop database Covid19;
    end
go

create database Covid19;
go

use Covid19;
go

if(OBJECT_ID(N'Continent') IS NOT NULL)
    begin
        drop table Continent;
    end
go

create table Continent (
                           con_id		int				identity(1,1)	not null,
                           con_name	varchar(100)	not null,
                           constraint PK_Continent primary key (con_id),
                           constraint U_name unique(con_name)
)

if(OBJECT_ID(N'Country') IS NOT NULL)
    begin
        drop table Country;
    end
go

create table Country
(
    cty_id			int				identity(1,1)	not null,
    con_id			int				not null,
    cty_iso_code	varchar(10)		not null,
    cty_location	varchar(50)		not null,
    constraint PK_Country primary key (cty_id),
    constraint FK_Country_Contintent foreign key (con_id) references Continent(con_id),
    constraint U_iso_code unique (cty_iso_code)
)

if(OBJECT_ID(N'Cases') IS NOT NULL)
    begin
        drop table Cases;
    end
go

create table Cases
(
    cas_id					int		identity(1,1)	not null,
    cty_id					int		not null,
    cas_date				date	not null,
    cas_total_cases			int		not null,
    cas_new_cases			int		not null,
    cas_total_deaths		int		not null,
    cas_new_deaths			int		not null,
    cas_reproduction_rate	float	not null,
    constraint PK_Cases primary key (cas_id),
    constraint FK_Cases_Country foreign  key (cty_id) references Country(cty_id),
)

if(OBJECT_ID(N'Tests') IS NOT NULL)
    begin
        drop table Tests;
    end
go

create table Tests
(
    tes_id				int		identity(1,1)	not null,
    cty_id				int		not null,
    tes_new_tests		int		not null,
    tes_total_tests		int		not null,
    tes_positive_rate	float	not null,
    constraint PK_Tests primary key (tes_id),
    constraint FK_Tests_Country foreign key (cty_id) references Country(cty_id)
)

if(OBJECT_ID(N'Vaccinations') IS NOT NULL)
    begin
        drop table Vaccinations;
    end
go

create table Vaccinations
(
    vac_id									int		identity(1,1)	not null,
    cty_id									int		not null,
    vac_date								date	not null,
    vac_total_vaccinations					int,
    vac_people_vaccinated					int,
    vac_people_fully_vaccinated				int,
    vac_new_vaccinations					int,
    constraint PK_Vaccinations primary key (vac_id),
    constraint FK_Vaccinations_Country foreign key (cty_id) references Country(cty_id),
);