CREATE TABLE predictions (
    userid VARCHAR(50) PRIMARY KEY,
    prediction INT NOT NULL
);

CREATE TABLE actuals (
    userid VARCHAR(50) PRIMARY KEY,
    actual INT NOT NULL
);



-- ADD Example data

insert into predictions (userid, prediction) values ('user1', 0);

insert into predictions (userid, prediction) values ('user2', 1);

insert into predictions (userid, prediction) values ('user3', 1);

insert into predictions (userid, prediction) values ('user4', 0);

-- ADD ACTUALS

insert into actuals (userid, actual) values ('user1', 0);

insert into actuals (userid, actual) values ('user2', 1);

insert into actuals (userid, actual) values ('user3', 1);

insert into actuals (userid, actual) values ('user4', 1);


-- CALCULATE THE ACCURACY
SELECT
    ROUND( CAST( SUM(correct_prediction) AS DECIMAL)  / COUNT(*)  , 4) as accuracy
FROM (
    SELECT 
        a.userid,
        CASE WHEN a.actual = p.prediction THEN 1 ELSE 0 END AS correct_prediction
    FROM 
        actuals a
    JOIN 
        predictions p ON a.userid = p.userid
);