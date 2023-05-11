CREATE TABLE companies (
    name TEXT PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE postings (
    id INTEGER PRIMARY KEY,
    company TEXT NOT NULL REFERENCES companies(name),
    job TEXT NOT NULL,
    place TEXT NOT NULL
);