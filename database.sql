CREATE TABLE IF NOT EXISTS urls (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS url_checks (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT REFERENCES urls (id),
    status_code SMALLINT,
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE OR REPLACE VIEW latest_url_checks AS
SELECT
	t1.url_id,
	t1.status_code,
	t1.created_at
FROM url_checks AS t1
WHERE t1.created_at = (
	SELECT
		MAX(t2.created_at)
	FROM url_checks AS t2
	WHERE t1.url_id = t2.url_id
	GROUP BY t2.url_id);
