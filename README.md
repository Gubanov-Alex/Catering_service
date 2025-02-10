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