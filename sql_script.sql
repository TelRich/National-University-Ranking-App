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

-- Top 5 schools by undergrad enrollment for midwest states
SELECT md.name, r.undergrad_enrollment
FROM midwest md
INNER JOIN Rank r
ON md.rank_id = r.rank_id
ORDER BY r.undergrad_enrollment DESC
LIMIT 5;

-- Top 5 schools by undergrad enrollment for northeast states
SELECT md.name, r.undergrad_enrollment
FROM northeast md
INNER JOIN Rank r
ON md.rank_id = r.rank_id
ORDER BY r.undergrad_enrollment DESC
LIMIT 5;

