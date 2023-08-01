# Laptop-DB

Laptop-DB is a web application for managing laptops and their associated parts. It allows users to search for laptop information down to the model/serial number and find associated parts. Users can also search for specific parts and see all the laptops that use that part. The data is user-generated, and the application includes badges to denote verified values. Users can upvote or downvote laptop and part information, and there is a reporting feature for suggesting different values.

## Features

- Laptop information lookup by model/serial number
- Part information lookup by part ID
- Upvoting and downvoting of laptop and part data
- Reporting feature for suggesting data changes/bugs/general comments
- User-generated data with badges for verified values

## Tech Stack

- Django: The web framework used for the backend
- HTML, CSS (Bootstrap), JavaScript: Frontend development
- SQLite: Database for storing data
- AWS S3: Storage for static files and media files
- Apache: Web server for deploying the application

## Deployment

This application is deployed on [laptop-db.com](https://www.laptop-db.com).
