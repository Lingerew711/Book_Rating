CREATE TABLE "books" (
	"isbn"	VARCHAR  PRIMARY KEY,
	"title"	VARCHAR NOT NULL,
	"author"	VARCHAR NOT NULL,
	"year"	INTEGER NOT NULL
);
CREATE TABLE "users" (
    "name" VARCHAR(50) NOT NULL.
	"username" VARCHAR(50) PRIMARY KEY,
	"password"	VARCHAR(50) NOT NULL
);
CREATE TABLE "reviews" (
	"id"	SERIAL PRIMARY KEY,
	"username"	VARCHAR(50) NOT NULL,
	"review"	VARCHAR NOT NULL,
	"rating"	INTEGER NOT NULL,
	"book_id"	VARCHAR(150) NOT NULL,
	FOREIGN KEY("username") REFERENCES "users",
	FOREIGN KEY("book_id") REFERENCES "books"
);