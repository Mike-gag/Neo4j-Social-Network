---QUERY 1---
MATCH (u:User)
RETURN COUNT(u) AS UserCount

---QUERY 2---
MATCH (t:Target)
RETURN COUNT(t) AS TargetCount

---QUERY 3---
MATCH (u:User)-[a]->(t:Target)
RETURN COUNT(a) AS ActionCount

---QUERY 4---
MATCH (u:User {id: 37})-[a]->(t:Target)
RETURN a.ACTIONID as ActionID, t.id as TargetID

---QUERY 5---
MATCH (u:User)-[a]->(t:Target)
RETURN u.id AS UserID, COUNT(a) AS ActionCount
ORDER BY UserID ASC

---QUERY 6---
MATCH (u:User)-[a]->(t:Target)
WITH t, COUNT(DISTINCT u) AS UserCount
RETURN t.id AS TargetID, UserCount
ORDER BY TargetID ASC

---QUERY 7---
MATCH (u:User)-[a]->(t:Target)
WITH u, COUNT(a) AS ActionCount
RETURN AVG(ActionCount) AS AverageActionsPerUser

---QUERY 8---
MATCH (u:User)-[a]->(t:Target)
WHERE a.FEATURE2 > 0
RETURN u.id AS UserID, t.id AS TargetID
ORDER BY TargetID ASC

---QUERY 9---
MATCH (u:User)-[a]->(t:Target)
WHERE a.LABEL = 1
RETURN t.id AS TargetID, COUNT(a) AS ActionCount