import csv
import sys
import os
import pymysql
from pymysql import cursors
from dotenv import load_dotenv

load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")
connection = pymysql.connect(
    host,
    user,
    password,
    database
    )
cursor = connection.cursor()
# testing

def load_and_print_product_list():
    cursor.execute('SELECT product_id, product_name, price FROM products')
    rows = cursor.fetchall()
    for row in rows:
        print(f'Product ID: {str(row[0])}, Product Name: {row[1]}, Price: {row[2]}')

def load_and_print_courier_list():
    cursor.execute('SELECT courier_id, courier_name, phone FROM couriers')
    rows = cursor.fetchall()
    for row in rows:
        print(f'ID: {str(row[0])}, Courier Name: {row[1]}, Phone Number: {row[2]}')

def main_menu():
    print("       Main Menu:\n")
    try:
        start = input("What would you like to do?\n"
                        "Press 1 to show Product Menu\n"
                        "Press 2 to show Courier Menu\n"
                        "Press 3 to show Order Menu\n"
                        "Press 0 to close app\n")
        while True:
            if int(start) == 1:
                return product_menu()
            elif int(start) == 2:
                return courier_menu()
            elif int(start) == 3:
                return order_menu()
            elif int(start) == 0:
                print("Okay. Closing the app. Byee")
                break
            else:
                start = input("Uh oh! That's not in the list. Please try again:\n"
                                "Press 1 to show Product Menu\n"
                                "Press 2 to show Courier Menu\n"
                                "Press 3 to show Order Menu\n"
                                "Press 0 to close app\n")
    except ValueError:
        print("Whoops! Please enter a number.")
        main_menu()
    except KeyboardInterrupt:
        print("Keyboard Interrupt :)")
        os._exit(0)
    finally:
        return sys.exit()

######################################################       THE PRODUCT MENU       ######################################################

def product_menu():
    os.system("cls")
    print("       Product Menu:\n")
    try:
        options = input("Press 0 to return to Main Menu\n"
                        "Press 1 to display the list of current products\n"
                        "Press 2 to create a new product\n"
                        "Press 3 to update a product\n"
                        "Press 4 to delete a product\n")
        while True:
            if int(options) == 0:
                return return_to_main_menu()
            elif int(options) == 1:
                return display_list_of_products()
            elif int(options) == 2:
                return create_new_product()
            elif int(options) == 3:
                return update_product()
            elif int(options) == 4:
                return delete_a_product()
            else:
                options = input("Whoops! That number isn't in the list. Please enter again:\n"
                                "Press 0 to return to Main Menu\n"
                                "Press 1 to display the list of current products\n"
                                "Press 2 to create a new product\n"
                                "Press 3 to update a product\n"
                                "Press 4 to delete a product\n")
    except ValueError:
        print("Whoops! Please enter a number.")
        return product_menu()
    except KeyboardInterrupt:
        print("Keyboard Interrupt :)")
        os._exit(0)

def return_to_main_menu():
    print("Returning to Main Menu")
    return main_menu()

def display_list_of_products():
    # os.system("cls")
    print("Here is the list of products:")
    load_and_print_product_list()
    while True:
        finished_looking = input("Press 0 to return to the Product Menu once you're done\n")
        if finished_looking == "0":
            break
        else:
            print("Invalid input. Please enter again.")
    return product_menu()

def append_product_to_db(new_product, new_price):
    sql = "INSERT INTO products (product_name, price) VALUES (%s, %s)"
    val = (new_product, new_price)
    cursor.execute(sql, val)
    connection.commit()

def create_new_product():
    os.system("cls")
    print("Create New Product:")
    return create_new_product2()

def create_new_product2():
    load_and_print_product_list()
    new_product = input("What product would you like to add?\n"
                        "You can press 0 to go back.\n").title()
    if new_product == "0":
        print("Okay! Returning to Product Menu")
        return product_menu()
    else:
        new_price = input("What is the price of this product?\n")
        append_product_to_db(new_product, new_price)
        print("You have successfully added {} to the list!".format(new_product))
        load_and_print_product_list()
        return create_another_product()

def continue_adding_product_prompt():
    continue_adding = input("\nWould you like to add anything else?\nPress 1 for Yes\nPress 2 for No\n")
    return continue_adding

def continue_adding_product_result():
    continue_adding = continue_adding_product_prompt()
    if continue_adding == "1":
        return create_new_product2()
    elif continue_adding == "2":
        return product_menu()
    else:
        print("Sorry, that wasn't an option.")
        return continue_adding_product_result()

def create_another_product():
    return continue_adding_product_result()

def update_product_in_db(new_product, new_price, change_product):
    cursor.execute("UPDATE products SET product_name=%s, price=%s WHERE product_id=%s", (new_product, new_price, change_product))
    connection.commit()

def product_id_list():
    cursor.execute("SELECT product_id FROM products")
    result_set = cursor.fetchall()
    result = []
    for x in result_set:
        result.append(x[0])
    return result

def update_product():
    os.system("cls")
    print("Update A Product:")
    return update_product2()
    
def update_product2():
    load_and_print_product_list()
    product_id_list()
    try:
        change_product = int(input("What product would you like to update?\nYou can press 0 to go back\n"))
        while True:
            if change_product == 0:
                break
            elif change_product in product_id_list():
                print("To update a product or price, enter what you would like to change it to. Or leave blank to skip:")
                cursor.execute("SELECT product_name, price FROM products WHERE product_id=(%s)", (change_product))
                selected_product = cursor.fetchall()
                new_product = input("Current product: {}\nReplace with: ".format(selected_product[0][0])).title()
                if new_product == "":
                    new_product = selected_product[0][0]
                else:
                    pass
                new_price = input("Current price: {}\nReplace with: ".format(selected_product[0][1]))
                if new_price == "":
                    new_price = selected_product[0][1]
                else:
                    pass
                print(new_product, new_price)
                update_product_in_db(new_product, new_price, change_product)
                load_and_print_product_list()
                cursor.execute("SELECT product_name, price FROM products WHERE product_id=(%s)", (change_product))
                selected_product = cursor.fetchall()
                print("You have successfully updated number {}:\nProduct name: {}. Price: {}".format(change_product, selected_product[0][0], selected_product[0][1]))
                return update_another_product()
            else:
                change_product = int(input("Sorry, that isn't in the list. Please enter again\n"))
        return product_menu()
    except ValueError:
        print("Oops! Please input a number.")
        return update_product()
    except KeyboardInterrupt:
        print("Keyboard Interrupt :)")
        os._exit(0)

def change_product_prompt():
    change_product = input("\nWould you like to update anything else?\nPress 1 for Yes\nPress 2 for No\n")
    return change_product

def change_product_result():
    change_product = change_product_prompt()
    if change_product == "1":
        return update_product2()
    elif change_product == "2":
        return product_menu()
    else:
        print("Sorry, that wasn't an option.")
        return change_product_result()

def update_another_product():
    return change_product_result()

def delete_product_in_db(delete_product):
    cursor.execute("DELETE FROM products WHERE product_id=%s", (delete_product))
    connection.commit()

def delete_a_product():
    os.system("cls")
    print("Delete A Product:")
    return delete_a_product2()

def delete_a_product2():
    load_and_print_product_list()
    product_id_list()
    try:
        delete_product = int(input("What product would you like to delete?\nYou can press 0 to go back\n"))
        while True:
            if delete_product == 0:
                break
            elif delete_product in product_id_list():
                cursor.execute("SELECT product_name, price FROM products WHERE product_id=(%s)", (delete_product))
                selected_product = cursor.fetchall()
                confirm = int(input("Are you sure you want to delete {}?\nPress 1 for Yes\nPress 2 to cancel\n".format((selected_product[0]))))
                if confirm == 1:
                    print("You've successfully deleted {} from the list!".format(selected_product[0][0]))
                    delete_product_in_db(delete_product)
                    load_and_print_product_list()
                    return delete_another_product()
                else:
                    print("Okay, cancelled!")
                    return delete_a_product()
            else:
                delete_product = int(input("Sorry, that isn't in the list. Please enter again\n"))
        return product_menu()
    except ValueError:
        load_and_print_product_list()
        print("Oops! Please input a number.")
        return delete_a_product()
    except KeyboardInterrupt:
        print("Keyboard Interrupt :)")
        os._exit(0)

def delete_product_again_prompt():
    delete_again = input("\nWould you like to delete anything else?\nPress 1 for Yes\nPress 2 for No\n")
    return delete_again

def delete_product_again_result():
    delete_product_again =  delete_product_again_prompt()
    if delete_product_again == "1":
        return delete_a_product2()
    elif delete_product_again == "2":
        return product_menu()
    else:
        print("Sorry, that wasn't an option.")
        return delete_product_again_result()

def delete_another_product():
    return delete_product_again_result()

######################################################       THE COURIER MENU       ######################################################

def courier_menu():
    print("       Courier Menu:\n")
    try:
        options = input("Press 0 to return to Main Menu\n"
                        "Press 1 to display the list of current couriers\n"
                        "Press 2 to add a new courier\n"
                        "Press 3 to update a courier\n"
                        "Press 4 to delete a courier\n")
        while True:
            if int(options) == 0:
                return return_to_main_menu()
            elif int(options) == 1:
                return display_list_of_couriers()
            elif int(options) == 2:
                return create_new_courier()
            elif int(options) == 3:
                return update_courier()
            elif int(options) == 4:
                return delete_a_courier()
            else:
                options = input("Whoops! That number isn't in the list. Please enter again:\n"
                                "Press 0 to return to Main Menu\n"
                                "Press 1 to display the list of current courier\n"
                                "Press 2 to add a new courier\n"
                                "Press 3 to update a courier\n"
                                "Press 4 to delete a courier\n")
    except ValueError:
        print("Oops! Please input a number.")
        return courier_menu()
    except KeyboardInterrupt:
        print("Keyboard Interrupt :)")
        os._exit(0)

def display_list_of_couriers():
    print("Here is the list of couriers:")
    load_and_print_courier_list()
    while True:
        finished_looking = input("Press 0 to return to the Product Menu once you're done\n")
        if finished_looking == "0":
            break
        else:
            print("Invalid input. Please enter again.")
    return courier_menu() 

def append_courier_to_db(new_courier, new_phone):
    sql = "INSERT INTO couriers (courier_name, phone) VALUES (%s, %s)"
    val = (new_courier, new_phone)
    cursor.execute(sql, val)
    connection.commit()

def create_new_courier():
    print("Add New Courier:")
    return create_new_courier2()
    
def create_new_courier2():
    load_and_print_courier_list()
    new_courier = input("What courier would you like to add?\n"
                        "You can press 0 to go back.\n").title()
    if new_courier == "0":
        print("Okay! Returning to Courier Menu")
        return courier_menu()
    else:
        new_phone = input("What is their phone number?\n")
        append_courier_to_db(new_courier, new_phone)
        print("You have successfully added {} to the list!".format(new_courier))
        load_and_print_courier_list()
        return create_another_courier()

def continue_adding_courier_prompt():
    continue_adding = input("Would you like to add anyone else?\nPress 1 for Yes\nPress 2 for No\n")
    return continue_adding

def continue_adding_courier_result():
    continue_adding = continue_adding_courier_prompt()
    if continue_adding == "1":
        return create_new_courier2()
    elif continue_adding == "2":
        return courier_menu()
    else:
        print("Sorry, that wasn't an option.")
        return continue_adding_courier_result()

def create_another_courier():
    return continue_adding_courier_result()

def update_courier_in_db(new_courier, new_phone, change_courier):
    cursor.execute("UPDATE couriers SET courier_name=%s, phone=%s WHERE courier_id=%s", (new_courier, new_phone, change_courier))
    connection.commit()

def courier_id_list():
    cursor.execute("SELECT courier_id FROM couriers")
    result_set = cursor.fetchall()
    result = []
    for x in result_set:
        result.append(x[0])
    return result

def update_courier(): #if both inputs are empty, say okay, nothing has been updated
    print("Update A Courier:")
    return update_courier2()

def update_courier2():
    load_and_print_courier_list()
    courier_id_list()
    try:
        change_courier = int(input("What courier would you like to update?\nYou can press 0 to go back\n"))
        while True:
            if change_courier == 0:
                break
            elif change_courier in courier_id_list():
                print("To update a courier or phone number, enter what you would like to change it to. Or leave blank to skip:")
                cursor.execute("SELECT courier_name, phone FROM couriers WHERE courier_id=(%s)", (change_courier))
                selected_courier = cursor.fetchall()
                print(selected_courier[0])
                new_courier = input("Current courier: {}\nReplace with: ".format(selected_courier[0][0])).title()
                if new_courier == "":
                    new_courier = selected_courier[0][0]
                else:
                    pass
                new_phone = input("Current phone number: {}\nReplace with: ".format(selected_courier[0][1]))
                if new_phone == "":
                    new_phone = selected_courier[0][1]
                else:
                    pass
                print(new_courier, new_phone)
                update_courier_in_db(new_courier, new_phone, change_courier)
                load_and_print_courier_list()
                cursor.execute("SELECT courier_name, phone FROM couriers WHERE courier_id=(%s)", (change_courier))
                selected_courier = cursor.fetchall()
                print("You have successfully updated number {}:\nCourier name: {}. Phone: {}".format(change_courier, selected_courier[0][0], selected_courier[0][1]))
                return update_another_courier()
            else:
                change_courier = int(input("Sorry, they aren't in the list. Please enter again\n"))
        return courier_menu()
    except ValueError:
        print("Oops! Please input a number.")
        return update_courier()
    except KeyboardInterrupt:
        print("Keyboard Interrupt :)")
        os._exit(0)

def change_courier_prompt():
    change_courier = input("Would you like to update anyone else?\nPress 1 for Yes\nPress 2 for No\n")
    return change_courier

def change_courier_result():
    change_courier = change_courier_prompt()
    if change_courier == "1":
        return update_courier2()
    elif change_courier == "2":
        return courier_menu()
    else:
        print("Sorry, that wasn't an option.")
        return change_courier_result()

def update_another_courier():
    return change_courier_result()

def delete_courier_in_db(delete_courier):
    cursor.execute("DELETE FROM couriers WHERE courier_id=%s", (delete_courier))
    connection.commit()

def delete_a_courier():
    print("Delete A Courier")
    return delete_a_courier2()

def delete_a_courier2():
    load_and_print_courier_list()
    courier_id_list()
    try:
        delete_courier = int(input("Which courier would you like to delete?\nYou can press 0 to go back\n"))
        while True:
            if delete_courier == 0:
                break
            elif delete_courier in courier_id_list():
                cursor.execute("SELECT courier_name, phone FROM couriers WHERE courier_id=(%s)", (delete_courier))
                selected_courier = cursor.fetchall()
                confirm = int(input("Are you sure you want to delete {}?\nPress 1 for Yes\nPress 2 to cancel\n".format(selected_courier[0][0])))
                if confirm == 1:
                    delete_courier_in_db(delete_courier)
                    load_and_print_courier_list()
                    return delete_another_courier()
                else:
                    print("Okay, cancelled!")
                    return delete_a_courier()
            else:
                delete_courier = int(input("Sorry, they aren't in the list. Please enter again\n"))
        return courier_menu()
    except ValueError:
        load_and_print_courier_list()
        print("Oops! Please input a number.")
        return delete_a_courier()
    except KeyboardInterrupt:
        print("Keyboard Interrupt :)")
        os._exit(0)
        
def delete_courier_again_prompt():
    delete_again = input("Would you like to delete anyone else?\nPress 1 for Yes\nPress 2 for No\n")
    return delete_again

def delete_courier_again_result():
    delete_again = delete_courier_again_prompt()
    if delete_again == "1":
        return delete_a_courier2()
    elif delete_again == "2":
        return courier_menu()
    else:
        print("Sorry, that wasn't an option.")
        return delete_courier_again_result()

def delete_another_courier():
    return delete_courier_again_result()

######################################################       THE ORDER MENU       ######################################################
def load_and_print_order_list():
    cursor.execute('SELECT * FROM orders')
    rows = cursor.fetchall()
    for row in rows:
        print(f'Order ID: {row[0]}, Customer Name: {row[1]}, Customer Address: {row[2]}, Customer Phone: {row[3]}, Courier: {row[4]}, Status: {row[5]}, Items: {row[6]}')

def order_menu():
    print("       Order Menu:\n")
    try:
        options = input("Press 0 to return to Main Menu\n"
                        "Press 1 to display the list of current orders\n"
                        "Press 2 to create a new order\n"
                        "Press 3 to update the status of an order\n"
                        "Press 4 to update an order\n"
                        "Press 5 to delete an order\n")
        while True:
            if int(options) == 0:
                return return_to_main_menu()
            elif int(options) == 1:
                return display_list_of_orders()
            elif int(options) == 2:
                return create_new_order()
            elif int(options) == 3:
                return update_order_status()
            elif int(options) == 4:
                return update_order()
            elif int(options) == 5:
                return delete_an_order()
            else:
                options = input("Whoops! That number isn't in the list. Please enter again:\n"
                                "Press 0 to return to Main Menu\n"
                                "Press 1 to display the list of current orders\n"
                                "Press 2 to create a new order\n"
                                "Press 3 to update the status of an order\n"
                                "Press 4 to update an order\n"
                                "Press 5 to delete an order\n")
    except ValueError:
        print("Oops! Please enter a number.")
        return order_menu()
    except KeyboardInterrupt:
        print("Keyboard Interrupt :)")
        os._exit(0)

def display_list_of_orders():
    print("Here is the list of orders:")
    load_and_print_order_list()
    
    while True:
        finished_looking = input("Press 0 to return to the Order Menu once you're done\n")
        if finished_looking == "0":
            break
        else:
            print("Invalid input. Please enter again.")
    return order_menu()

def append_order_to_db(new_name, new_address, new_phone, order_courier, order_status, order_products):
    sql = "INSERT INTO orders (customer_name, customer_address, customer_phone, courier, order_status, items) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (new_name, new_address, new_phone, order_courier, order_status, order_products)
    cursor.execute(sql, val)
    connection.commit()

def create_new_order():
    print("Create A New Order:")
    return create_new_order2()

def create_new_order2():
    load_and_print_order_list()
    
    new_name = input("What is the name of the customer would you like to add?\nYou can press 0 to go back.\n").title()
    if new_name == "0":
        print("Okay! Returning to Order Menu")
        return order_menu()
    
    else:
        new_address = input("What is their address?\n").title()
        
        new_phone = input("What is their number?\n")
        
        load_and_print_product_list()
        print("Please select the customer's chosen products from the list. Press 0 when done.")
        
        order_products_list = []
        choose_products = input("Product number: ")
        while choose_products != "0":
            order_products_list.append(choose_products)
            print(order_products_list)
            choose_products = input("Product number: ")
        
        print(order_products_list)
        order_products = ', '.join(order_products_list)
        
        load_and_print_courier_list()
        order_courier = int(input("Please select a courier\n"))
        
        order_status = "Preparing"
        
        append_order_to_db(new_name, new_address, new_phone, order_courier, order_status, order_products)
        
        print("Successfully created the order for {}!".format(new_name))
        
        load_and_print_order_list()
        return create_another_order()

def continue_adding_order_prompt():
    continue_adding = input("Would you like to add anything else?\nPress 1 for Yes\nPress 2 for No\n")
    return continue_adding

def continue_adding_order_result():
    continue_adding = continue_adding_order_prompt()
    if continue_adding == "1":
        return create_new_order2()
    elif continue_adding == "2":
        return order_menu()
    else:
        print("Sorry, that wasn't an option.")
        return continue_adding_order_result()

def create_another_order():
    return continue_adding_order_result()

def update_order_status_in_db(new_status, change_status):
    cursor.execute("UPDATE orders SET order_status=%s WHERE order_id=%s", (new_status, change_status))
    connection.commit()

def order_id_list():
    cursor.execute("SELECT order_id FROM orders")
    result_set = cursor.fetchall()
    result = []
    for x in result_set:
        result.append(x[0])
    return result

def update_order_status():
    print("Update Order Status:")
    return update_order_status2()

def update_order_status2():
    load_and_print_order_list()
    order_id_list()
    try:
        while True:
            change_status = int(input("Which order would you like to update the status of?\nYou can press 0 to go back\n"))
            if change_status == 0:
                break
            
            elif change_status in order_id_list():
                print("To update an order status, please enter one of the following options:\n"
                        "Press 1 for Preparing\nPress 2 for Out-For-Delivery\nPress 3 for Delivered\n")
                
                cursor.execute("SELECT order_status FROM orders WHERE order_id=(%s)", (change_status))
                selected_order_status = cursor.fetchall()
                
                new_status = int(input("Current status: {}\nEnter option here: ".format(selected_order_status[0][0])))
                if new_status == 1:
                    new_status = "Preparing"
                elif new_status == 2:
                    new_status = "Out-For-Delivery"
                elif new_status == 3:
                    new_status = "Delivered"
                else:
                    print("Sorry, that wasn't an option")
                    return update_order_status()
                
                print("You have successfully updated the order status from {} to {}!".format(selected_order_status[0][0], new_status))
                
                update_order_status_in_db(new_status, change_status)
                
                load_and_print_order_list()
                return update_another_order_status()
            else:
                print("Sorry, that isn't in the list.")
        return order_menu()
    except ValueError:
        print("Oops! Please input a number.")
        return update_order_status()
    except KeyboardInterrupt:
        print("Keyboard Interrupt :)")
        os._exit(0)

def change_order_status_prompt():
    change_order_status = input("Would you like to update another status?\nPress 1 for Yes\nPress 2 for No\n")
    return change_order_status

def change_order_status_result():
    change_order_status = change_order_status_prompt()
    if change_order_status == "1":
        return update_order_status2()
    elif change_order_status == "2":
        return order_menu()
    else:
        print("Sorry, that wasn't an option.")
        return change_order_status_result()

def update_another_order_status():
    return change_order_status_result()

def update_order_in_db(replace_name, replace_address, replace_phone, replace_courier, replace_status, replacement_products, choose_update_order):
    cursor.execute("UPDATE orders SET customer_name=%s, customer_address=%s, customer_phone=%s, courier=%s, order_status=%s, items=%s WHERE order_id=%s",
                (replace_name, replace_address, replace_phone, replace_courier, replace_status, replacement_products, choose_update_order))
    connection.commit()

def update_order():
    print("Update An Order:")
    return update_order2()

def update_order2():
    load_and_print_order_list()
    order_id_list()
    try:
        while True:
            choose_update_order = int(input("Which order would you like to update?\nYou can press 0 to go back\n"))
            
            if choose_update_order == 0:
                return order_menu()
            
            elif choose_update_order in order_id_list():
                print("Please update the property, or leave blank to skip:")
                
                cursor.execute("SELECT * FROM orders WHERE order_id=(%s)", (choose_update_order))
                selected_order = cursor.fetchall()
                
                replace_name = input("Current customer name: {}\nReplace with: ".format(selected_order[0][1])).title()
                if replace_name == "":
                    replace_name = selected_order[0][1]
                else:
                    pass
                
                replace_address = input("Current customer address: {}\nReplace with: ".format(selected_order[0][2]))
                if replace_address == "":
                    replace_address = selected_order[0][2]
                else:
                    pass
                
                replace_phone = input("Current phone number: {}\nReplace with: ".format(selected_order[0][3]))
                if replace_phone == "":
                    replace_phone = selected_order[0][3]
                else:
                    pass
                
                load_and_print_courier_list()
                replace_courier = input("Current courier: {}\nReplace with: ".format(selected_order[0][4]))
                if replace_courier == "":
                    replace_courier = selected_order[0][4]
                else:
                    pass
                
                while True:
                    replace_status = input("What would you like to change the status to?\n"
                                        "Press 1 for Preparing\nPress 2 for Out-For-Delivery\nPress 3 for Delivered\n"
                                        "Current status: {}\nEnter here: ".format(selected_order[0][5]))
                    if replace_status == "":
                        replace_status = selected_order[0][5]
                        break
                    elif replace_status == "1":
                        replace_status = "Preparing"
                        break
                    elif replace_status == "2":
                        replace_status = "Out-For-Delivery"
                        break
                    elif replace_status == "3":
                        replace_status = "Delivered"
                        break
                    else:
                        print("Sorry, that wasn't an option")
                        
                load_and_print_product_list()
                replacement_products_list = []
                replace_items = input("Current products: {}\nNew product: ".format(selected_order[0][6]))
                if replace_items == "":
                    items_string_to_list = list(selected_order[0][6].split(", "))
                    replacement_products_list = items_string_to_list
                    print(replacement_products_list)
                    
                else:
                    while replace_items != "0":
                        replacement_products_list.append(replace_items)
                        print("Current list: {}".format(replacement_products_list))
                        replace_items = input("New product: ")
                    print(replacement_products_list)
                    
                replacement_products = ', '.join(replacement_products_list)
                
                update_order_in_db(replace_name, replace_address, replace_phone, replace_courier, replace_status, replacement_products, choose_update_order)
                
                load_and_print_order_list()
                return update_another_order()
            else:
                print("Sorry, that isn't in the list. Please enter again")
                return update_order()
    except ValueError:
        print("Oops! Please input a number.")
        return update_order()
    except KeyboardInterrupt:
        print("Keyboard Interrupt :)")
        os._exit(0)

def change_order_prompt():
    change_order = input("Would you like to update another order?\nPress 1 for Yes\nPress 2 for No\n")
    return change_order

def change_order_result():
    change_order = change_order_prompt()
    if change_order == "1":
        return update_order2()
    elif change_order == "2":
        return order_menu()
    else:
        print("Sorry, that wasn't an option.")
        return change_order_result()

def update_another_order():
    return change_order_result()

def delete_order_in_db(delete_order):
    cursor.execute("DELETE FROM orders WHERE order_id=%s", (delete_order))
    connection.commit()

def delete_an_order():
    print("Delete An Order:")
    return delete_an_order2()

def delete_an_order2():
    load_and_print_order_list()
    order_id_list()
    try:
        delete_order = int(input("Which order would you like to delete?\nYou can press 0 to go back\n"))
        
        if delete_order == 0:
            return order_menu()
        
        elif delete_order in order_id_list():
            cursor.execute("SELECT customer_name, customer_address, customer_phone, courier, order_status, items FROM orders WHERE order_id=(%s)", (delete_order))
            selected_product = cursor.fetchall()
            
            confirm = int(input("Are you sure you want to delete {}?\nPress 1 for Yes\nPress 2 to cancel\n".format(selected_product[0])))
            if confirm == 1:
                print("You've successfully deleted {}'s order from the list!".format(selected_product[0][0]))
                delete_order_in_db(delete_order)
                load_and_print_order_list()
                return delete_another_order()
            
            else:
                print("Okay, cancelled!")
                return delete_an_order()
            
        else:
            print("Sorry, that isn't an option")
            return delete_an_order2()
    except ValueError:
        print("Oops! Please input a number.")
        return delete_an_order()
    except KeyboardInterrupt:
        print("Keyboard Interrupt :)")
        os._exit(0)

def delete_order_again_prompt():
    delete_again = input("Would you like to delete another order?\nPress 1 for Yes\nPress 2 for No\n")
    return delete_again

def delete_order_again_result():
    delete_again = delete_order_again_prompt()
    if delete_again == "1":
        return delete_an_order2()
    elif delete_again == "2":
        return order_menu()
    else:
        print("Sorry, that wasn't an option.")
        return delete_order_again_result()

def delete_another_order():
    return delete_order_again_result()

print("Welcome to the app!!\n")
main_menu()
