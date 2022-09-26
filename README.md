# jerrys_quick_mart
## Solution to Jerry´s quick mart problem

>Previous configuration
### Program is codified on python so it´s necesary to:
#### (1) Install python version 3.8.1~
#### (2) Run like a console app.
#### (3) Know that all the files in the repository should be in the same folder
#### (4) The inventory is preloaded when the program is executed from a txt file "invetory.txt"

>Solution description
### I decided to solve this on python because I think python has a flexible way to manipulate system files
### The program works like a store cashier, with the principal menu and its corresponding submenus

### Principal Menu
>Sell products    =>Goes to select customer type

>Chech inventory  =>Prints the Inventory

>Exit             =>Finishes the program

### Customer type 
#### Allows to select the type of customer because the price of the products depends on the type of customer.

>Regular customer =>Goes to Sell Menu

>Rewards member   =>Goes to Sell Menu

>Cancel           =>Returns to Principal Menu

### Sell Menu

> Add products to cart             =>Allows to add products to cart by writing the product's name and quantity that the user wants to buy

> Delete products from the cart    =>Allows to delete products from the cart by writing the item´s uuid

> Show products in cart            =>Displays the current products in the cart

> Check in                         =>Goes to Check in Menu

> Cancel transaction               =>Returns to Principal Menu

### Check in Menu

>Enter the customer's name           => Writes the customer's name

#Confirm Transaction

>Yes                               =>Goes to Cash Menu

>No					     =>Cancels transaction and returns to Principal Menu

#Cash Menu

>Shows the cost of the transaction

>Enter the payment       	     =>Displays transaction´s information and create a transaction information file .txt



