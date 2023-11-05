# Installation

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Installation Guide](https://docs.docker.com/compose/install/)

## Getting Started

To get your project up and running, follow these steps:

1. Clone the repository (if you haven't already):

   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```
2. Change the variables in .env if needed
3. Build and start the Docker containers:
    ```bash
    docker-compose up --build
    ```
4. To stop the project, use the following command:
    ```bash
    docker-compose down
    ```

# API Endpoints

## Auth

### User Registration

- **URL:** `/register`
- **HTTP Method:** POST
- **Description:** Allows users to register with the application
- **Request Body:**
    - `username` (string): User's desired username.
    - `password` (string): User's password.
    - `location` (string, optional): User's location.
- **Authentication:** Not required.
- **Response:** New user object with user ID, username, and location.

### User Login

- **URL:** `/login`
- **HTTP Method:** POST
- **Description:** Allows registered users to log in and obtain an authentication token.
- **Request Body:**
    - `username` (string): User's username.
    - `password` (string): User's password.
- **Authentication:** Not required.
- **Response:** Authentication token for the user.

### User Profile Update

- **URL:** `/profile`
- **HTTP Method:** PUT
- **Description:** Allows authenticated users to update their profile information.
- **Request Body:**
    - `location` (string, optional): User's location.
- **Authentication:** Required (user must provide a valid authentication token).
- **Response:** Updated user object with the new location.

## Weather

### Get Current Weather

- **URL**: `/current`
- **Method**: GET
- **Description**: This endpoint retrieves the current weather for the user's location.

- **Response Format**: JSON
- **Response Example**:
  ```json
  {
    "city": "New York",
    "temperature": 23.5,
    "weather_condition": "Clear"
  }
  ```

### Search Current Weather

- **URL**: `/search`
- **Method**: GET
- **Description**: This endpoint is designed to search for the current weather in a specified city or zip code.
- **Parameters**:
    - `city` (optional): The name of the city for which you want to retrieve weather data.
    - `zip` (optional): The zip code of the city for which you want to retrieve weather data.
- **Response Format**: JSON
- **Response Example**:
  ```json
   {
  "city": "Los Angeles",
  "temperature": 28.2,
  "weather_condition": "Partly Cloudy"
   }
  ```

### Forecast Weather

- **URL:** `/forecast`
- **Method:** `GET`
- **Description:** This endpoint retrieves the weather forecast for a specified city or user's location.
- **Parameters**:
    - `city` (optional): The name of the city for which you want to retrieve weather data.
    - `zip` (optional): The zip code of the city for which you want to retrieve weather data.
- **Response Format**: JSON
- **Response Example**:

```json
{
  "city": "Chicago",
  "forecast": [
    {
      "date": "2023-11-05T12:00:00Z",
      "temperature": 15.5,
      "weather_condition": "Rain"
    },
    {
      "date": "2023-11-06T12:00:00Z",
      "temperature": 12.8,
      "weather_condition": "Cloudy"
    }
  ]
}
