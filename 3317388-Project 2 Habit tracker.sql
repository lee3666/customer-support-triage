CREATE TABLE habits (
    habit_id    INT PRIMARY KEY,
    habit_name  VARCHAR(50) NOT NULL,
    target_days INT NOT NULL,
    start_date  DATE NOT NULL
);

CREATE TABLE habit_log (
    log_id     INT PRIMARY KEY,
    habit_id   INT NOT NULL,
    log_date   DATE NOT NULL,
    completed  TINYINT NOT NULL
);