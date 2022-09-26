# jerrys_quick_mart
## Solution to jerrys quick mart

>Previous configuration
### Program is writed on python then is necesary
#### (1) Install a python version 3.8.1~
#### (2) Its a console aplication.
#### (3) All the files in the repository should be in the same folder
#### (4) The inventory is preloaded when the program is executed from a txt file "invetory.txt"

>Solution description
### I decided to solve this on python because I think python has a flexible way to manipulate system files
### The program works like a store cashier, with some menu and submenus

### Principal Menu
>Sell products    =>Goes to select customer type

>Chech inventory  =>Print the Inventory

>Exit             =>Finish the program

### Customer type 
#### Allow's to select the type of customer because the price of the products that are gonna be selling depends of that
>Regular customer =>Goes to Sell Menu
>Rewards member   =>Goes to Sell Menu
>Cancel           =>Return to Principal Menu

### Sell Menu
> Add products to cart             =>Allow to add products to cart writing the products name and quantity that user want to buy
> Delete products from the cart    =>Allow to delete products from the cart writing the uuid of the cart item
> Show products in cart            =>Display the current products in the cart
> Check in                         =>Check In Menu
> Cancel transaction               =>Return to Principal Menu

### Check in Menu
>Enter the customer name           => Write the customer name

#Confirm Transaction
>Yes                               =>Cash Menu
>No					     =>Cancel transaction return´s to Principal Menu

#Cash Menu
>Shows the cost of the transaction
>Enter the money			     =>Display transaction´s information and create a transaction information file .txt



