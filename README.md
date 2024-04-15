---
date: 2024-04-15T21:05:11.013421
author: AutoGPT <info@agpt.co>
---

# test

The project involves creating an API endpoint that accepts various forms of data, notably URLs, text, and contact information, for the purpose of QR code generation. The user prefers the encoded data to be in the form of a URL to facilitate directing users to specific webpages, aiming for efficient and user-friendly interactions. A significant requirement is the ability to customize the generated QR codes. Customization options include adjustments to the QR code's size, making it larger for enhanced readability, color modifications for improved contrast, and a higher error correction level to maintain scannability even when partially obscured or damaged. The output format for the generated QR code is specified as SVG, aligning with the user's needs for quality and scalability. The technical stack selected for this task consists of Python as the programming language, with FastAPI as the API framework, PostgreSQL for the database, and Prisma as the Object-Relational Mapping (ORM) system. This stack supports the development of efficient, scalable, and maintainable applications, fitting the project's requirements for a robust and responsive QR code generation service.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'test'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
