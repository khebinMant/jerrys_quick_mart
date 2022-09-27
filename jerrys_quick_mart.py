
import os
import uuid
from datetime import date

products = []
TAX = 6.5

class Product:
    def __init__(self, item, quantity, regular_price, member_price, tax_status):
        self.item = item
        self.quantity = quantity
        self.regular_price = regular_price
        self.member_price = member_price
        self.tax_status = tax_status
            
class Customer:
    def __init__(self, name, customer_status):
        self.name = name
        self.customer_status = customer_status

class CartItem:
    def __init__(self, uuid, product, quantity, unit_price, sub_total, tax, total):
        self.uuid = uuid
        self.product = product
        self.quantity = quantity
        self.unit_price = unit_price
        self.sub_total = sub_total
        self.tax = tax
        self.total = total

class Transaction:
    def __init__(self, uuid, cart_items, date, customer):
        self.uuid = uuid
        self.cart_items = cart_items
        self.date = date
        self.customer = customer
        self.cash = 0
        self.total = 0
        self.total_items = 0
        self.sub_total = 0
        self.tax = 0
        self.change = 0
    
    def calculate_total_items(self):
        for cart_item in self.cart_items:
            self.total_items += cart_item.quantity
    
    def calculate_total(self):
        for cart_item in self.cart_items:
            self.total += cart_item.total

    def calculate_sub_total(self):
        for cart_item in self.cart_items:
            self.sub_total += cart_item.sub_total
    
    def calculate_tax(self):
        for cart_item in self.cart_items:
            self.tax += cart_item.tax

    def set_cash(self,cash):
        self.cash = cash    

    def calculate_change(self):
        self.change = (self.total - self.cash)*-1
    


def create_products_dictionary(product_line):
    #Convert to objects all the products on each line from the txt inventory file
    product = Product(product_line[0],product_line[1],product_line[2],product_line[3],product_line[4])
    products.append(product)

def update_inventory_file():
    #Update the inventory in the txt file 
    with open("inventory.txt","w") as filestream:
        for product in products:
            filestream.write("%s,%s,%s,%s,%s\n"%(str(product.item),str(product.quantity),str(product.regular_price),str(product.member_price),str(product.tax_status)))

def initialize_data():
    #Initialize the data from txt file
    with open("inventory.txt", "r") as filestream:
        for line in filestream:
            product_line = line.rstrip().split(",")
            create_products_dictionary(product_line)

def clean_console():
    #This function just clean the console
    clear = lambda: os.system('cls')
    clear()

def update_product_stock(product,quantity,action):
    #This function allow to update product stock when the transaction is cancelled
    #or when the transaction has been completed
    for prod in products:
        if prod.item == product.item:
            if action == 'remove':
                prod.quantity = str(int(prod.quantity) - quantity)
            if action == 'add':
                prod.quantity = str(int(prod.quantity) + quantity)

def search_cart_product_by_uuid(cart_items):
    #This function helps to search a product added to the cart by his unique id uuid
    #this is used to delete a product from the cart
    if len(cart_items)>0:
        check_find = False
        while check_find == False:   
            cart_item_uuid = input("Enter product´s UUID you want to remove: ")
            for cart_item in cart_items:
                if cart_item.uuid == cart_item_uuid:
                    check_find = True
                    print(cart_item.product.item)
                    return cart_item
            if check_find == False:
                print("Product does not exist in the cart. Please write an available product")
    else:
        print("There are no products in the cart")
        input("Press any key to continue....")

def search_product_by_name():
    #This function helps to search a product by his name 
    #the process to select a product and add a cart is by the products name 
    check_find = False
    while check_find == False:   
        product_name = input("Enter the name of the product you want to buy: ").strip()
        for product in products:
            if product.item == product_name:
                check_find = True
                return product
        if check_find == False:
            print("Product does not exist in the inventory. Please write an available product")
    
def check_stock(product):
    #This function helps to check the stock availability 
    quantity = 0
    while True:
        try:
            quantity = int(input("Please enter the quantity to be purchased: "))
        except ValueError:
            clean_console()
            print("Invalid input. Please try again")
        if quantity == 0:
            clean_console()
            print("Not a valid number")
        else:
            break  # <-- if the user inputs a valid score, this will break the input loop

    for prod in products:
        if prod.item == product.item:
            if int(prod.quantity) == 0:
                clean_console()
                print("Sorry, there is not more stock available")
                input("Press any key to continue....")
                return 'no_stock'
            if int(prod.quantity) < int(quantity):
                clean_console()
                print("Sorry, there is not enough stock to complete your order. There are only: ",prod.quantity, "available")
                input("Press any key to continue....")
                return 'not_enough'
            if int(prod.quantity) >= int(quantity):
                return quantity


def show_cart_products(cart_items):
    #This function display all the products selected to be bought
    print("****************************** PRODUCTS IN CART ******************************")
    print("______________________________________________________________________________")
    print("|   UUID   | Product  | Quantity | Unit Price | Subtotal |   Tax   |  Total  |")
    print("______________________________________________________________________________")
    for cart_item in cart_items:
        print(str(cart_item.uuid).rjust(10), str(cart_item.product.item).rjust(10) , str(cart_item.quantity).rjust(7), str(cart_item.unit_price).rjust(10), str(format(cart_item.sub_total,'.2f')).rjust(13) , str(format(cart_item.tax,'.2f')).rjust(11), str(format(cart_item.total,'.2f')).rjust(10))

def show_available_products():
    #This function display all the avaliable products
    #this helps to the user to choice the products more easily
    print("***************************** PRODUCTS ****************************")
    print("___________________________________________________________________")
    print("|   Item   | Quantity | Regular price | Member price | Tax status |")
    print("___________________________________________________________________")
    for product in products:
        print(str(product.item).rjust(10), str(product.quantity).rjust(5), str(product.regular_price).rjust(15), str(product.member_price).rjust(12), str(product.tax_status).rjust(20))


def add_product_to_cart(cart_items,customer_status):
    #Allow to add products in the cart
    #First check the customer status normal or VIP to calculate 
    #prices and taxes 
    show_available_products()
    product = search_product_by_name()
    quantity = check_stock(product)

    if quantity!='no_stock' and quantity!='not_enough':
        unit_price = product.regular_price
        if customer_status == 'vip':
            unit_price = product.member_price
        sub_total = float(unit_price) * int(quantity)
        tax = 0
        total = sub_total
        if product.tax_status == 'taxable':
            tax =  (sub_total * TAX)/100
            total = sub_total + tax
        cart_item = CartItem(str(uuid.uuid4())[:5], product, quantity, unit_price, sub_total, tax, total)
        cart_items.append(cart_item)
        #At this point is necesary to update the product stock on products
        update_product_stock(product,int(quantity),'remove')

def remove_product_from_cart(cart_items):
    #Remove products from the cart and 
    #update the stock in this case if we remove products from the cart
    #then is necesary to add to the products the canceled quantity
    show_cart_products(cart_items)
    cart_item = search_cart_product_by_uuid(cart_items)
    if cart_item:
        cart_items.remove(cart_item)
        update_product_stock(cart_item.product,int(cart_item.quantity),'add')


def check_customer_status():
    #Menu to select customer status
    option = 0
    print("**************** SELECT CUSTOMER TYPE ********************")
    while True:
        print("(1) Regular customer")
        print("(2) Rewards member")
        print("(3) Cancel")
        option = input("Select customer status: ")
        clean_console()
        if(option == '1'):
            #Returns regular  when its a regular customer
            return 'regular'
        if(option == '2'):
            #Returns vip when its a premium member
            return 'vip'
        if(option == '3'):
            return 'cancel'
        elif(option != '1' and option != '2' and option != '3'):
            print("That option is not in the menú")

def cash_validation(total):
    #Function to check validation of cash
    #Need to be more than the total price, can not be 0 and just can be a number
    cash = 0
    print("***** THE TOTAL AMOUNT OF THE TRANSACTION IS: $%s *******"% total)
    while True:
        try:
            cash = int(input("Enter the cash given by the customer: "))
        except ValueError:
            clean_console()
            print("This was not a valid input please try again")
        if cash == 0 or cash < total:
            clean_console()
            print("No valid cash its not enough the total is $",total)
        else:
            break 
    return cash

def show_transaction_on_console(transaction):
    # When  transaction is completed the 
    # program prints the transaction
    clean_console()
    print("****************************** Jerry´s Quick Mart ******************************")
    print("Date: " + str(transaction.date))
    print("TRANSACTION: "+transaction.uuid)
    print("________________________________________________________________________________")
    print("|   UUID   |  Product  | Quantity | Unit Price |  Subtotal |   Tax   |  Total  |")
    print("________________________________________________________________________________")
    for cart_item in transaction.cart_items:
        print(str(cart_item.uuid).rjust(10), str(cart_item.product.item).rjust(10), str(cart_item.quantity).rjust(10), str(cart_item.unit_price).rjust(12), str(format(cart_item.sub_total,'.2f')).rjust(12) , str(format(cart_item.tax,'.2f')).rjust(10), str(format(cart_item.total,'.2f')).rjust(9))
    
    print("TOTAL NUMBER OF ITEMS SOLD: $" + str(transaction.total_items))
    print("SUB-TOTAL: $"+str(format(transaction.sub_total,'.2f')))
    print("TAX(6.5%): $"+ str(format(transaction.tax,'.2f')))
    print("TOTAL: $"+ str(format(transaction.total,'.2f')))
    print("CASH: $"+ str(format(transaction.cash,'.2f')))
    print("CHANGE: $"+str(format(transaction.change,'.2f')))
    print("________________________________________________________________________________")
    print("Your transaction has been created successfully!")
    print("The txt file has been created successfully!")
    input("Press any key to continue....")

def create_transaction_file(transaction):
    #This function helps to create a file with the transaction information
    #The name of file is transaction plus the unique uuid created to the object transaction
    transaction_name = 'transaction_'+transaction.uuid+'.txt'
    with open(transaction_name, 'w') as f:
        f.write(
            '''
            ************************* Jerry´s Quick Mart *****************************
            Date: %s
            TRANSACTION: %s
            **************************************************************************
                  |UUID|   |ITEM|      |QUANTITY| |UNIT PRICE|  |SUBTOTAL|  |  TAX  |  | TOTAL |
            ''' 
            %(transaction.date, transaction.uuid)
        )
        for cart_item in transaction.cart_items:
            f.write(
            '''
            %s %s %s %s %s %s %s
            '''
            %(str(cart_item.uuid).rjust(10), str(cart_item.product.item).rjust(10), str(cart_item.quantity).rjust(10), str(cart_item.unit_price).rjust(12), str(format(cart_item.sub_total,'.2f')).rjust(13) , str(format(cart_item.tax,'.2f')).rjust(11), str(format(cart_item.total,'.2f')).rjust(10)))
        
        f.write(
            '''
            **************************************************************************
            TOTAL NUMBER OF ITEMS SOLD: %s
            SUB-TOTAL: $%s
            TAX(6.5%%): $%s
            TOTAL: $%s
            CASH: $%s
            CHANGE: $%s
            ''' 
            %(str(transaction.total_items), str(format(transaction.sub_total,'.2f')), str(format(transaction.tax,'.2f')), str(format(transaction.total,'.2f')), str(format(transaction.cash,'.2f')), str(format(transaction.change,'.2f'))))

def return_to_stock(cart_items):
    # When the transaction is cancelled is necesary 
    # to return the products to the stock
    if len(cart_items)>0:
        for cart_item in cart_items:
            for product in products:
                if cart_item.product.item == product.item:
                    product.quantity = int(product.quantity) + int(cart_item.quantity)

def check_in(cart_items,customer_status):
    #This function ask to the user all necesary information 
    # to create the transaction and give the option to cancell or not
    if len(cart_items)>0:
        customer_name =  input("Enter customer´s name: ")
        customer = Customer(customer_name, customer_status)
        transaction = Transaction(str(uuid.uuid4())[:5], cart_items, date.today(),customer) 
        transaction.calculate_total_items()
        transaction.calculate_sub_total()
        transaction.calculate_tax()
        transaction.calculate_total()
        #Ask if want to continue with the transaction
        option = ''
        while option != 'YES' and option != 'NO':
            clean_console()
            print("***** ARE YOU SURE TO CONTINUE WITH THE TRANSACTION? *******")
            print("( YES ) Continue")
            print("( NO  ) Cancel transaction")
            option = input("Text your answer: ").upper()
            #If the answer is yes then overrride txt inventory file and Create a new txt file with the transaction information
            if option == 'YES':
                cash =  cash_validation(transaction.total)
                transaction.set_cash(cash)
                transaction.calculate_change()
                create_transaction_file(transaction)
                show_transaction_on_console(transaction)
                update_inventory_file()
                return 'completed'
            #If the answer is not then return to stock all the products 'canceled'
            if option == 'NO':
                return 'canceled'

        input("Press any key to continue....")
    else:
        print("There are no products in the cart. Please first add some products")
        input("Press any key to continue....")

def sell_menu():
    #This function just display the sell menu
    option = 0
    cart_items = []
    customer_status = check_customer_status()
    if customer_status == 'cancel':
        return
    else:
        print("__________________________________________________________________________")
        print("************************* Jerry´s Quick Mart *****************************")
        print("__________________________________________________________________________")
        while True:
            print("(1) Add products to cart")
            print("(2) Delete products from the cart")
            print("(3) Show products in cart")
            print("(4) Check in")
            print("(5) Cancel transaction")
            option = input("Select a menu option: ")
            clean_console()
            if(option == '1'):
                print("***************** ADD PRODUCTS TO CART *******************")
                add_product_to_cart(cart_items,customer_status)
                clean_console()
                print("**********************************************************")
            if(option == '2'):
                print("************ DELETE PRODUCTS FROM THE CART ***************")
                remove_product_from_cart(cart_items)
                clean_console()
                print("**********************************************************")
            if(option == '3'):
                print("*************** CHECK PRODUCTS IN CART *******************")
                show_cart_products(cart_items)
                input("Press any key to continue....")
                clean_console()
                print("**********************************************************")
            if(option == '4'):
                print("********************** CHECK IN **************************")
                status = check_in(cart_items,customer_status)
                #If the transaction is cancelled then the products stock dont should be changed 
                if status == 'canceled':
                    cart_items = []
                    return_to_stock(cart_items)
                    clean_console()
                    break
                if status == 'completed':
                    clean_console()
                    break
                print("**********************************************************")
            if(option == '5'):
                #If the transaction is cancelled then the products stock dont should be changed 
                return_to_stock(cart_items)
                break
            elif(option != '1' and option != '2' and option != '3' and option != '4' and option != '5'):
                print("That option is not in the menú")

def main():
    #This function just display the main menu
    option = 0
    initialize_data()
    print("__________________________________________________________________________")
    print("************************* Jerry´s Quick Mart *****************************")
    print("*************************      WELCOME       *****************************")
    print("__________________________________________________________________________")
    while True:
        print("(1) Sell products")
        print("(2) Check inventory")
        print("(3) Exit")
        option = input("Select a menu option: ")
        clean_console()
        if(option == '1'):
            print("******************** SELL PRODUCTS ***********************")
            sell_menu()
            print("**********************************************************")
        if(option == '2'):
            print("******************* CHECK INVENTORY **********************")
            show_available_products()
            #Print all current inventory
            print("**********************************************************")
        if(option == '3'):
            break
        elif(option != '1' and option != '2' and option != '3'):
            print("That option is not in the menú")

main()
