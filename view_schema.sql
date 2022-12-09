--Example of ways we can use data to assist with analysis
create VIEW party_by_state as 
select sum("Total_Voters") as Vote_Count,"Party" as party,"State" as state from floridavoter group by "Party","State"
UNION
select count(voter_count)as vote_count,party,state from voters group by party, state
union
select sum("Total_Voters") as vote_count,"Party" as party,"State" as state from nc_voter_data group by "Party","State";;

select * from party_by_state;