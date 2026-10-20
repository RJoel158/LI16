CREATE TABLE IF NOT EXISTS db_ronald.fb_ronald (
userid BIGINT, age INT, dob_day INT, dob_year INT, dob_month INT,
gender STRING, tenure INT, friend_count INT, friendships_initiated INT,
likes BIGINT, likes_received BIGINT, mobile_likes BIGINT,
mobile_likes_received BIGINT, www_likes BIGINT, www_likes_received BIGINT
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE TBLPROPERTIES ('serialization.null.format'='NA');
DESCRIBE db_ronald.fb_ronald;
