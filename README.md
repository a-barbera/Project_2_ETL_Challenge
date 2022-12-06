# Project_2_ETL_Challenge
Group repository for Project 2, Data Analytics &amp; Visualization

# Project Contributors:
1. Anna Barbera
2. Daniel King-Allen
3. Peter Warren

<b>Our project code and resources can be found here:  https://github.com/a-barbera/Project_2_ETL_Challenge </b>

<h1>Voter Aggregation</h1>

# Project Overview and Resources:

State level documentation of voter registration information from Florida, Georgia and North Carolina will be cleaned and standardized across the states. “Baseline” information will be identified across all three states as well as data that is better documented per state. This information will be cleaned, normalized, and then entered into a SQL database. 

1. Florida Voter Registration
https://dos.myflorida.com/elections/data-statistics/voter-registration-statistics/voter-registration-reports/


2. North Carolina: https://www.ncsbe.gov/results-data/voter-history-data
ncsbe.govncsbe.gov
Voter History Data | NCSBE
Access weekly-updated voter history data for every voter in North Carolina, or see group-level voter demographic counts. 

3. Georgia: https://sos.ga.gov/voter-history-files
sos.ga.govsos.ga.gov
Voter History Files | Georgia Secretary of State
The information and materials available on this website are provided by local elections officials as a service to the public and intended to be as accurate as possible. If the generated list appears to be missing any information regarding qualified candidates, please visit http://elections.sos.ga.gov/Elections/countyelectionoffices.do to locate the contact information for the appropriate elections office to report the issue. This list will not include anyone who has qualified to run in a municipal general or special election unless the city contracts with a county to conduct qualifying of candidates on the city's behalf.


# Our Process:
1. Extraction:
    First, we gathered the voter data from the 3 states we chose and discussed the similarities and differences observed in the keys and values of those datasets, including forming a strategy around how to transform them for the smoothest possible joining further along in the process.  Based on these findings, we chose common values for our datasets to focus on, including: 

<b>County Name, State, Party, Race_Code, Ethnic_Code, Total_Voters, Election_Date</b>
