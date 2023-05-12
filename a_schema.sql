CREATE TABLE postings (
    id INTEGER PRIMARY KEY,
    company TEXT NOT NULL,
    job TEXT NOT NULL,
    place TEXT NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);