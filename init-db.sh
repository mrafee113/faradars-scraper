psql postgres -c "create database faradars-scraper;"
psql postgres -c "grant connect on database faradars-scraper to public;"

psql faradars-scraper -c "create role faradars-scraper;"
psql faradars-scraper -c "alter role faradars-scraper with login;"
psql faradars-scraper -c "alter role faradars-scraper with password 'faradars-scraper';"
psql faradars-scraper -c "grant all privileges on database faradars-scraper to faradars-scraper;"
psql faradars-scraper -c "alter role faradars-scraper superuser;"

psql faradars-scraper -c "alter role faradars-scraper set client_encoding to 'utf8'"
psql faradars-scraper -c "alter role faradars-scraper set timezone to 'UTC'"
