DROP TABLE if EXISTS voters;
--Creating a blank table of what our final values will be after parsing the data
CREATE TABLE voters (
	county_number VARCHAR(50),
	registration_number VARCHAR(50),
	election_date VARCHAR(50),
	election_type VARCHAR(50),
	party VARCHAR(30),
	absentee VARCHAR(30),
	provisional VARCHAR(30),
	supplemental VARCHAR(30)
	)
;
drop table if exists georgia;

-- Creating a blank table to store the txt file of georgia voter data
CREATE TABLE georgia (data VARCHAR(255));

-- Inserting data into Georgia table using substrings annotated in the codebook on the original voter data site
insert INTO voters(county_number, registration_number, election_date, election_type, party, absentee, provisional, supplemental)
select CAST(SUBSTRING(data, 1, 3) AS VARCHAR(50)) as county_number,
	CAST(SUBSTRING(data, 4, 8) AS VARCHAR(50)) as registration_number,
	CAST(SUBSTRING(data, 12, 8) AS VARCHAR(50)) as election_date,
	CAST(SUBSTRING(data, 20, 3) AS VARCHAR(50)) as election_type,
	CAST(SUBSTRING(data, 23, 2) AS VARCHAR(50)) as party,
	CAST(SUBSTRING(data, 25,1) as VARCHAR(50)) as absentee,
	CAST(SUBSTRING(data, 26,1) as VARCHAR(50)) as provisional,
	CAST(SUBSTRING(data, 27,1) as VARCHAR(50)) as supplemental
FROM georgia;

-- Data Cleansing steps: Turning the election_date field from a string (VarChar) into a datetime field
ALTER TABLE voters Alter column election_date type date
using to_date(election_date, 'YYYYMMDD');

-- Adding a state field and coding each row as GA 
Alter table voters
add State varchar(30);

update voters set state='GA';

-- Standardizing the Party data into three different categories (Rep=Republican identifier, DEM= Democrat Identifier, UNA= all other parties listed)
update voters
set party='REP'
where party='R ';

update voters set party='DEM'
where party='D ';

update voters set party='UNA'
where party not in ('DEM','REP');

-- Creating a table to import codebook for each of Georgia's over 150 county codes and their associated name
create table counties (
	county_number varchar(30),
	county_name varchar(30)
);


--adding a blank field into the voters table called county name and effectively joining the data together using the County codes
alter table voters add county_name varchar(30);

update voters set county_name= c.county_name
from counties as c
where voters.county_number=c.county_number;

-- adding a table with voter_count for later aggregation
alter table voters add voter_count INT;

UPDATE voters set voter_count= 1;

-- testing using the sum function to see number of voters per county
select sum(voter_count) from voters group by county_number;