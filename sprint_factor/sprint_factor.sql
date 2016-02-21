alter session set `store.json.all_text_mode` = true;
alter session set `planner.enable_decimal_data_type` = true;

SELECT averageSpeedSprint, maxSpeed, sprintCount, displayName, positionGroup, gameId, snapCount FROM
(
(SELECT nflId, AVG(CAST(t1.flattracking.s as DECIMAL(28, 2))) AS averageSpeedSprint, MAX(CAST(t1.flattracking.s as DECIMAL(28, 2))) AS maxSpeed, COUNT(CAST(t1.flattracking.s as DECIMAL(28, 2))) AS sprintCount FROM (SELECT FLATTEN(t.flatdata.playerTrackingData) AS flattracking, t.flatdata.nflId as nflId FROM (SELECT FLATTEN(homeTrackingData) AS flatdata FROM dfs.`/Users/silvia/Desktop/NFL_Hackathon/data3/allgames.json`) t) t1 WHERE t1.flattracking.s > 5.0 GROUP BY nflId ORDER BY sprintCount
)
UNION
(SELECT nflId, AVG(CAST(t1.flattracking.s as DECIMAL(28, 2))) AS averageSpeedSprint, MAX(CAST(t1.flattracking.s as DECIMAL(28, 2))) AS maxSpeed, COUNT(CAST(t1.flattracking.s as DECIMAL(28, 2))) AS sprintCount FROM (SELECT FLATTEN(t.flatdata.playerTrackingData) AS flattracking, t.flatdata.nflId as nflId FROM (SELECT FLATTEN(awayTrackingData) AS flatdata FROM dfs.`/Users/silvia/Desktop/NFL_Hackathon/data3/allgames.json`) t) t1 WHERE t1.flattracking.s > 5.0 GROUP BY nflId ORDER BY sprintCount
)
) AS t3,
(SELECT t2.flatdata.displayName AS displayName, t2.flatdata.nflId AS nflId, t2.flatdata.positionGroup AS positionGroup FROM (SELECT FLATTEN(teamPlayers) AS flatdata FROM dfs.`/Users/silvia/Desktop/NFL_Hackathon/data3/allteams.json`) t2
) AS t4,

(
(SELECT COUNT(t1.flattracking.event) AS snapCount , nflId, gameId FROM (SELECT FLATTEN(t.flatdata.playerTrackingData) AS flattracking, t.flatdata.nflId AS nflId, t.gameId AS gameId FROM (SELECT FLATTEN(homeTrackingData) AS flatdata, gameId FROM dfs.`/Users/silvia/Desktop/NFL_Hackathon/data3/allgames.json`) t) t1 WHERE t1.flattracking.event='snap' GROUP BY nflId, gameId)
UNION
(SELECT COUNT(t1.flattracking.event) AS snapCount , nflId, gameId FROM (SELECT FLATTEN(t.flatdata.playerTrackingData) AS flattracking, t.flatdata.nflId AS nflId, t.gameId AS gameId FROM (SELECT FLATTEN(awayTrackingData) AS flatdata, gameId FROM dfs.`/Users/silvia/Desktop/NFL_Hackathon/data3/allgames.json`) t) t1 WHERE t1.flattracking.event='snap' GROUP BY nflId, gameId)

) AS t5

WHERE t3.nflId=t4.nflId AND t4.nflId=t5.nflId
ORDER BY sprintCount
;