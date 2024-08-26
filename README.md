E-Commerce Website Project

This project is an E-Commerce website developed using Django, where users can register, browse products, add them to their cart, and place orders. Admins have CRUD capabilities for managing categories and products. The website also features user authentication and order tracking.

To access the data for 
Adnin - username : admin, password : admin
To access the data for 
User - username : radha@gmail.com, password : radha12345

Task 1: Developed APIS
1. Signup
   Validations:
   - Email must be Unique,
   - Password's length must be greater than 6
   - Password must contains both letters and digits
   - Mobile Number's length must be 10 digits
2. Login
3. Place Order
4. Get Order by Admin
5. Add to cart
6. Checkout
7. logout

For this requirements, developed models are:
1. Category Model Fields: name
2. Product Model: category(FK), name, image, description, price
3. UserData: user, mobile, address, image
4. Cart Model: user,product,created
5. Booking Model: user, product, total, status, created
   
Task 2: Queries's output

Query 1 : Find user-wise, product-wise ordering quantity with total item value.
Query 2 : weekly order analysis for the first quarter
Query 3 : Retrieve product name and no of orders. exclude products with fewer than 5 orders.
Query 4 : Find the products thar are sold more than 7 times or have not sold yet in the first quarter.





