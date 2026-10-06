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


INSERT INTO habits (habit_id, habit_name, target_days, start_date) VALUES
(1, 'Exercise',    20, '2025-01-01'),
(2, 'Read',        25, '2025-01-01'),
(3, 'Meditate',    15, '2025-01-01');;

INSERT INTO habit_log (log_id, habit_id, log_date, completed) VALUES
-- Exercise (habitI 1) — done most days, a few misses
(1,  1, '2025-01-01', 1), (2,  1, '2025-01-02', 1), (3,  1, '2025-01-03', 0),
(4,  1, '2025-01-04', 1), (5,  1, '2025-01-05', 1), (6,  1, '2025-01-06', 1),
(7,  1, '2025-01-07', 0), (8,  1, '2025-01-08', 1), (9,  1, '2025-01-09', 1),
(10, 1, '2025-01-10', 1), (11, 1, '2025-01-11', 0), (12, 1, '2025-01-12', 1),
(13, 1, '2025-01-13', 1), (14, 1, '2025-01-14', 1), (15, 1, '2025-01-15', 1),
(16, 1, '2025-01-16', 0), (17, 1, '2025-01-17', 1), (18, 1, '2025-01-18', 1),
(19, 1, '2025-01-19', 1), (20, 1, '2025-01-20', 1), (21, 1, '2025-01-21', 1),
(22, 1, '2025-01-22', 1), (23, 1, '2025-01-23', 0), (24, 1, '2025-01-24', 1),
(25, 1, '2025-01-25', 1), (26, 1, '2025-01-26', 1), (27, 1, '2025-01-27', 1),
(28, 1, '2025-01-28', 1),

-- Read (habit 2) — very consistent
(29, 2, '2025-01-01', 1), (30, 2, '2025-01-02', 1), (31, 2, '2025-01-03', 1),
(32, 2, '2025-01-04', 1), (33, 2, '2025-01-05', 1), (34, 2, '2025-01-06', 1),
(35, 2, '2025-01-07', 1), (36, 2, '2025-01-08', 1), (37, 2, '2025-01-09', 1),
(38, 2, '2025-01-10', 1), (39, 2, '2025-01-11', 1), (40, 2, '2025-01-12', 0),
(41, 2, '2025-01-13', 1), (42, 2, '2025-01-14', 1), (43, 2, '2025-01-15', 1),
(44, 2, '2025-01-16', 1), (45, 2, '2025-01-17', 1), (46, 2, '2025-01-18', 1),
(47, 2, '2025-01-19', 1), (48, 2, '2025-01-20', 1), (49, 2, '2025-01-21', 1),
(50, 2, '2025-01-22', 1), (51, 2, '2025-01-23', 1), (52, 2, '2025-01-24', 1),
(53, 2, '2025-01-25', 0), (54, 2, '2025-01-26', 1), (55, 2, '2025-01-27', 1),
(56, 2, '2025-01-28', 1),

-- Meditate (habit 3) — patchy, several misses
(57, 3, '2025-01-01', 1), (58, 3, '2025-01-02', 0), (59, 3, '2025-01-03', 1),
(60, 3, '2025-01-04', 0), (61, 3, '2025-01-05', 1), (62, 3, '2025-01-06', 1),
(63, 3, '2025-01-07', 1), (64, 3, '2025-01-08', 0), (65, 3, '2025-01-09', 1),
(66, 3, '2025-01-10', 0), (67, 3, '2025-01-11', 1), (68, 3, '2025-01-12', 0),
(69, 3, '2025-01-13', 1), (70, 3, '2025-01-14', 1), (71, 3, '2025-01-15', 0),
(72, 3, '2025-01-16', 1), (73, 3, '2025-01-17', 1), (74, 3, '2025-01-18', 0),
(75, 3, '2025-01-19', 1), (76, 3, '2025-01-20', 1), (77, 3, '2025-01-21', 1),
(78, 3, '2025-01-22', 0), (79, 3, '2025-01-23', 0), (80, 3, '2025-01-24', 1),
(81, 3, '2025-01-25', 1), (82, 3, '2025-01-26', 0), (83, 3, '2025-01-27', 1),
(84, 3, '2025-01-28', 1);

SELECT * FROM habits;

SELECT
    h.habit_name,
    COUNT(*) AS days_completed
FROM habits h
JOIN habit_log l ON h.habit_id = l.habit_id
WHERE l.completed = 1
GROUP BY h.habit_name
ORDER BY days_completed DESC;

SELECT
    h.habit_name,
    COUNT(*) AS days_completed,
    ROUND(100.0 * COUNT(*) / 28, 1) AS pct_completed
FROM habits h
JOIN habit_log l ON h.habit_id = l.habit_id
WHERE l.completed = 1
GROUP BY h.habit_name
ORDER BY pct_completed DESC;

SELECT
    h.habit_name,
    COUNT(*) AS days_completed
FROM habits h
JOIN habit_log l ON h.habit_id = l.habit_id
WHERE l.completed = 1
GROUP BY h.habit_name
ORDER BY days_completed DESC
LIMIT 1;

SELECT
    h.habit_name,
    COUNT(*) AS days_missed
FROM habits h
JOIN habit_log l ON h.habit_id = l.habit_id
WHERE l.completed = 0
GROUP BY h.habit_name
ORDER BY days_missed DESC;

SELECT
    h.habit_name,
    h.target_days,
    COUNT(*) AS days_completed
FROM habits h
JOIN habit_log l ON h.habit_id = l.habit_id
WHERE l.completed = 1
GROUP BY h.habit_id, h.habit_name, h.target_days
HAVING COUNT(*) >= h.target_days;

SELECT
    h.habit_name,
    MIN(l.log_date) AS first_completed
FROM habits h
JOIN habit_log l ON h.habit_id = l.habit_id
WHERE l.completed = 1
GROUP BY h.habit_name
ORDER BY first_completed;

SELECT
    h.habit_name,
    COUNT(*) AS week1_completions
FROM habits h
JOIN habit_log l ON h.habit_id = l.habit_id
WHERE l.completed = 1
  AND l.log_date >= '2025-01-01'
  AND l.log_date <  '2025-01-08'
GROUP BY h.habit_name
ORDER BY week1_completions DESC;