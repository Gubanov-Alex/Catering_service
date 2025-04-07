# Catering Service Project
## Project Description
Catering Service is a web application designed for managing restaurant operations and food orders. Built with Django and Django REST Framework (DRF), it enables seamless interaction between restaurants, their menus, and users. This project provides functionality for managing restaurants, dishes, and orders efficiently.
## Key Features
- **Restaurant Management**: Full CRUD operations for restaurants.
- **Dish Management**: Creation and association of dishes with restaurants.
- **Order Management**: Supports order creation and order details management.
- **Admin Panel Integration**:
    - Manage restaurants and their associated dishes.
    - Handle orders and external order IDs.

- **Potential External System Integration**: Supported through the `RestaurantOrderID` model.

## Technologies Used
### Core Libraries
- **Django**: The primary framework used to build the backend.
- **Django Rest Framework (DRF)**: To expose RESTful APIs.
- **Celery and Redis**: For background task processing (if used).
- **pytest**: For testing and quality assurance.
- **MyPy, pylint, and pyflakes**: For code linting and type checking.

### Database
A relational database (e.g., PostgreSQL, MySQL, or SQLite) is used to store information about restaurants, dishes, and orders.
## Installed Applications
### Local Apps
- **food**: Handles restaurants, dishes, and orders functionality.
- **logistic**: (Presumed) module for logistics-related features.
- **users**: Manages the custom user model and user functionality.
- **shared**: (Presumed) shared components and utilities for the project.

### Third-Party Applications
- **Django Admin**: Provides an integrated admin interface.
- **Django Rest Framework**: Adds capabilities for building REST APIs.
- **Pytz**: To manage time zones.
- **Redis**: Supports caching and task queues.
- **Celery**: For asynchronous request processing.
- **Pytest**: For unit testing.

## Installation and Setup with Docker Compose, Uvicorn, and Pipfile
### 1. Clone the Repository
``` bash
git clone <REPOSITORY_URL>
cd Catering_service
```
### 2. Configure Environment Variables
1. Create a `.env` file by copying the example file:
``` bash
   cp .env.default .env
# configure environment
# run application
```
1. Edit the `.env` file to set up the environment variables, such as the database credentials. For example:
``` 
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=db
   DB_PORT=5432
```
### 3. Build Docker Containers
Build the Docker containers using the following command:
``` bash
docker-compose build
```
### 4. Start Containers
Start the application stack:
``` bash
docker-compose up
```
The application will spin up using **Uvicorn** as the server, and the database will be automatically initialized.
### 5. Apply Database Migrations
Run the following commands to apply migrations inside the Docker container:
``` bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
### 6. Create a Superuser
Create a superuser to manage the application through the Django Admin interface:
``` bash
docker-compose exec web python manage.py createsuperuser
```
### 7. Access the Application
The application will be accessible at:
``` 
http://localhost:8000
```




## API Documentation
### Available Endpoints
#### Examples of Key Endpoints:
- `/food/restaurants/` — Manage restaurants.
- `/food/dishes/` — CRUD operations for dishes.
- `/food/orders/` — Handle orders.

#### Example Request (POST: Create an Order):
``` json
POST /food/orders/
{
    "user_id": 1,
    "dishes": [{"dish_id": 10, "quantity": 2}],
    "total_price": 1000
}
```
## Admin Management
The Django admin interface provides tools to manage the application's key entities:
- **Restaurants**:
    - CRUD operations for restaurants.
    - Managing associated dishes.

- **Dishes**:
    - Includes attributes like name, price, and reference to the restaurant.

- **Orders**:
    - Manages orders with information about users and external integrations.

## Testing
This project includes unit tests. You can run the tests with the following command:
``` bash
pytest
```
## Example Workflow:
1. Register a restaurant via the Django admin panel.
2. Add dishes to the corresponding restaurant.
3. Create an order via the API.
4. Associate external order IDs for integration with third-party systems (optional).

### Screenshots
(Add screenshots of the application here, if available.)
## Future Development Plans
- Integration with payment systems.
- Extended logistics support.
- Customer notifications about order statuses.
- Advanced reporting and analytics for administrators.



### DEPLOYMENT
Set CI/CD
code quality tools
tests
Select Cloud Provider
Digital Ocean
Rent instance (machine)
Clone Project
Infra:
Native (bare metal)
Machine with application
Machine with worker (or same?)
Database
...
Docker Infra
Machine with Docker
Select HTTP-serverssh Hillyl Catering Gubanov Alex
security
SSL Certificates
Access to staticfiles
Reverse Proxy


### Loading Test Data (Fixtures)

To load mock data for the models: 
`DishOrderItem` 
`DishesOrder` 
`User` 
`DeliveryDishesOrder` 


1. Ensure the fixture file is located at `products/fixtures/.....`.
2. Run the following command to load the data:

   ```bash
   python manage.py loaddata fixtures/logistic_fixture.json
   python manage.py loaddata fixtures/dish_order_fixture.json
   python manage.py loaddata fixtures/user_fixtures.json
   python manage.py loaddata fixtures/dish_order_item_fixture.json
   ```

3. After the data is loaded, the model will be populated with test data.

**Note:** Ensure that restaurants `Melange` and `Bueno` are present and have been populated, 
along with the dishes `Пицца`, `Суши` and `Салат`.

You can use JSON fixtures like this in your project to easily update and manage test data.