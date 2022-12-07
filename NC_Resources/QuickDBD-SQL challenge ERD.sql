-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/FidsQz
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "NC_Voters" (
    "id" int   NOT NULL,
    "County_Name" varchar(50)   NOT NULL,
    "State" varchar(50)   NOT NULL,
    "Party" varchar(50)   NOT NULL,
    "Race_Code" varchar(50)   NOT NULL,
    "Ethnic_Code" varchar(50)   NOT NULL,
    "Total_Voters" int   NOT NULL,
    "Election_Date" date   NOT NULL,
    CONSTRAINT "pk_NC_Voters" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "GA_Voters" (
    "id" int   NOT NULL,
    "County_Name" varchar(50)   NOT NULL,
    "State" varchar(50)   NOT NULL,
    "Party" varchar(50)   NOT NULL,
    "Race_Code" varchar(50)   NOT NULL,
    "Ethnic_Code" varchar(50)   NOT NULL,
    "Total_Voters" int   NOT NULL,
    "Election_Date" date   NOT NULL,
    CONSTRAINT "pk_GA_Voters" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "FL_Voters" (
    "id" int   NOT NULL,
    "County_Name" varchar(50)   NOT NULL,
    "State" varchar(50)   NOT NULL,
    "Party" varchar(50)   NOT NULL,
    "Race_Code" varchar(50)   NOT NULL,
    "Ethnic_Code" varchar(50)   NOT NULL,
    "Total_Voters" int   NOT NULL,
    "Election_Date" date   NOT NULL,
    CONSTRAINT "pk_FL_Voters" PRIMARY KEY (
        "id"
     )
);

