# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Product vision statement

"Grocery Quest" is a fun and practical web app that helps users improve their grocery budgeting skills through an interactive price guessing game while also discovering, reviewing, and comparing local grocery stores to make smarter shopping decisions."

## User stories

Price Guessing Game
- As a user, I want to guess the prices of grocery items so that I can test my knowledge and improve my budgeting skills.
- As a user, I want to see the actual price of an item after guessing so that I can compare my estimate to the real cost.
- As a user, I want to see average price estimates from other users so that I can compare my guesses with the community.

Grocery Store Listings & Reviews
- As a user, I want to browse a list of grocery stores in my area so that I can find places to shop.
- As a user, I want to filter stores by distance, price range, product variety, and customer service rating so that I can find the best option for my needs.
- As a user, I want to read reviews from other shoppers so that I can make informed decisions before visiting a store.
- As a user, I want to submit reviews for stores I’ve visited so that I can share my experiences with others.
- As a user, I want to upload photos of grocery stores so that others can get a visual idea of the store’s layout and product selection.

User Interaction & Personalization
- As a user, I want to add new grocery stores that are not listed so that I can contribute to the community.
- As a user, I want to edit or delete my reviews so that I can update my opinions if my experience changes.
- As a user, I want to save my favorite stores so that I can quickly access their details in the future.
- As a user, I want to create a profile to track my price guessing scores, submitted reviews, and favorite stores so that I can personalize my experience.

## Steps necessary to run the software

#### Prerequisites

- Python 3.11 or higher (if not using Docker for local development)
- MongoDB Atlas account
- Docker and Docker Compose installed

#### Clone the repository:

Clone the repository to your local machine:
```bash
git clone <https://github.com/software-students-spring2025/2-web-app-segfaultsquad.git>
```


#### Set up the virtual environment

1. Copy the example .env file:
```bash
cp .env.example .env
```

2. Or create a .env file in the root directory with the following content:
```bash
    MONGO_URI=your_mongodb_connection_string
    SECRET_KEY=your_secret_key
    DEBUG=True
    UPLOAD_FOLDER=./uploads
    MAX_CONTENT_LENGTH=16777216
```

#### Set up Docker
1. Build and start the containers using Docker Compose
```bash
docker-compose up --build
```
#### Access the application
Once the containers are up and running, you can access the application at: http://localhost:5050

#### Stopping the application
```bash
docker-compose down
```



## Task boards

[Link to Task Board](https://github.com/orgs/software-students-spring2025/projects/80/views/2)
