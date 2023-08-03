----Top 5 schools by rank for northeast states

Select a.name, b.rank,
From northeast a
Join Rank b 
Where rank_id = rank_id
Order by rank DESC
LIMIT 5
  
  


  -------Top 5 schools by tuition fees for southeast state
Select a.name, b.tuiton fee,
From South a
Join Rank b
Where rank_id = rank_id
Order by  tuition fee DESC
LIMIT 5


-- kennedy
-- show the top 5 schools by rank for west states. 
select w.name, r.rank_num
from nur_app.west as w
inner join nur_app.rank as r
on w.rank_id = r.id
order by r.rank_num asc limit 5


-- show the top 5 schools by instate fees for midwest states
select m.name, r.in_state
from nur_app.midwest as m
inner join nur_app.rank as r
on m.rank_id = r.id
order by r.in_state Desc limit 5

