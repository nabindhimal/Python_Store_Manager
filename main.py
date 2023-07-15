import termcolor
import datetime

# The termcolor module is not installed by default . You can install it using the following commands.
# For linux users : pip3 install termcolor
# For windows users : pip install termcolor
# For mac users : pip3 install termcolor

headers = ['Model Name', 'Brand', 'Price', 'Quantity', 'Processor', 'Graphics']
laptops = []

# Function for reading the inventory file
def read_inventory(): 
    with open('inventory.txt', 'r') as inventory:
        for line in inventory:
            line = line.strip()
            items = line.split(",")
            modelName,brand,price,quantity,processor,graphics_card = items
            laptop = {
                'modelName' : modelName.lower(),
                'brand' : brand.lower().strip(),
                'price' : price.strip(),
                'quantity' : int(quantity),
                'processor' : processor,
                'graphics_card' : graphics_card  
            }
            laptops.append(laptop)
    return laptops

inventory = read_inventory()

# Function for managing orders
def order():
    # Taking input for orders  
    print(termcolor.colored(('Enter details of laptop to order.'),'green'))

    while True:
        manufacter = input('Manufacturer name: ') 
        if manufacter=='':
            print(termcolor.colored((f"Please enter manufacturer's name."),'magenta',attrs=["bold"]))
        else:
            break

    while True:
        name = input("Laptop's model name: ") 
        if name=='':
            print(termcolor.colored((f"Please enter laptop's model name."),'magenta',attrs=["bold"]))
        else:
            break
    
    while True:
        brand = input('Brand: ') 
        if brand=='':
            print(termcolor.colored((f"Please enter laptop's brand name."),'magenta',attrs=["bold"]))
        else:
            break   

    while True:
        try:
            price =float(input("Price: "))   
            break
        except ValueError:
            print(termcolor.colored((f"Please enter valid price."),'magenta',attrs=["bold"]))

    while True:
        try:
            quantity = int(input("Quantity: "))   
            break
        except ValueError:
            print(termcolor.colored((f"Please enter valid quantity."),'magenta',attrs=["bold"]))

    while True:
        processor = input("Processor: ") 
        if processor=='':
            print(termcolor.colored((f"Please enter laptop's processor name."),'magenta',attrs=["bold"]))
        else:
            break

    while True:
        graphics_card = input("Graphics card: ") 
        if graphics_card=='':
            print(termcolor.colored((f"Please enter laptop's graphics name."),'magenta',attrs=["bold"]))
        else:
            break   

    # Updating the inventory file
    exists = False
    with open("inventory.txt", "r") as file1:
        lines = file1.readlines()
        for i, line in enumerate(lines):
            if line.startswith(name + ','):
                exists = True
                parts = line.strip().split(',')
                old_quantity = int(parts[3])
                new_quantity = old_quantity + quantity
                lines[i] = f"{name},{brand},{price},{new_quantity},{processor},{graphics_card}\n"
                break
    if not exists:
        lines.append(f'{name},{brand},{price},{quantity},{processor},{graphics_card}\n')
    
    with open("inventory.txt", "w") as file1:
        file1.writelines(lines)

    # Generating  and saving an invoice as a txt file for the order
    net_amount = price * quantity
    vat_amount = 0.13 * net_amount
    gross_amount = net_amount + vat_amount

    invoice = f"""Invoice for the order:
    Manufacturer:{manufacter}
    Laptop: {name}
    Brand: {brand}
    Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    Net Amount: {net_amount:.2f}
    VAT: {vat_amount:.2f}
    Gross Amount: {gross_amount:.2f}
    """

    filename = f"{manufacter}.txt"
    with open(filename, "w") as file2:
        file2.write(invoice)
    print(termcolor.colored((f"Invoice saved to {filename}"))),


    print(invoice)

# Function for managing sales
def sale():

    while True:
        customer = input(termcolor.colored(("What is your customer's name?: "),'white',attrs=["bold"]))
        if customer=='':
            print(termcolor.colored((f"Please enter customer's name."),'magenta',attrs=["bold"]))
        else:
            break
    
    # print(termcolor.colored(('Nice to meet you '+ customer+ '!'),'green',attrs=["bold"]))

    while True:
        name = input('Choose a brand of laptop?: ').lower()
        if name=='':
            print(termcolor.colored((f"Please enter your desired laptop's name."),'magenta',attrs=["bold"]))
        else:
            break
    

    # Finding the available laptops from inventory

    try:
        laptop_index = None
        for i, laptop in enumerate(inventory):
                if laptop['brand'].lower()==name:
                    laptop_index = i
                    print('These laptops are available in this brand.')
                    print(laptop['modelName'], ': ',laptop['quantity'],' in stock\n')
                    name1 = input('Choose a laptop to buy?: ').lower()
                    qun = int(input('Choose laptop quantity to buy?: '))
                    if qun > int(laptop['quantity']):
                        print('Not enough laptops available!')
                    else:
                        print('This is the price of the laptop: ','$',laptop['price'])
                        confirm = input(termcolor.colored(('Type y to place an order (q or n for exit): '),'red',attrs=["bold"])).lower()
                        if confirm in ['n','no','q']:
                            print('Goodbye!, Contact us when needed..')
                        else:
                            print(termcolor.colored(('Order Succesful! Thank You!'),'blue',attrs=["bold"]))
                            total_price = qun *float(laptop['price']) + 10
                            invoice = f"""Invoice for the sale:
            Customer name:{customer}
            Laptop: {name1}
            Brand: {name}
            Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            Shipping: {10}
            Total price: {total_price}
                                        """
                            filename = f"{customer}.txt"
                            with open(filename, "w") as file3:
                                file3.write(invoice)
                            print(termcolor.colored((f"Invoice saved to {filename}"),'magenta',attrs=["bold"]))

                            print(invoice)


                            # Updating the inventory
                            inventory[laptop_index]['quantity'] -= qun

                            # Saving the updated inventory
                            with open('inventory.txt', 'w') as file:
                                for laptop in inventory:
                                    file.write(f"{laptop['modelName']}, {laptop['brand']}, {laptop['price']}, {laptop['quantity']}, {laptop['processor']}, {laptop['graphics_card']}\n")
                            
                            print(termcolor.colored((f"Stock Updated!"),'magenta',attrs=["bold"]))
                            break
        else:
                    print(termcolor.colored((f"No laptops of this brand are available!"),'red',attrs=["bold"]))
                    print(termcolor.colored((f"Do you want to buy another laptop?"),'blue',attrs=["bold"]))
                    choice = input('Type "y" to buy again or press any key to quit: ').lower()
                    if choice in ['y','yes','ok']:
                            sale()
                    else:
                            print(termcolor.colored((f"Thanks for Visiting!"),'blue',attrs=["bold"]))
                            quit()
    except:
        print(termcolor.colored((f"Please enter valid inputs!"),'magenta',attrs=["bold"]))
        sale()

# Main function for the program

def main():
    # Printing available laptops
    try:
        print(termcolor.colored(("----------------------------------------------Available laptops-----------------------------------------------------------"),'cyan',attrs=["bold"]))
        print(termcolor.colored(("--------------------------------------------------------------------------------------------------------------------------"),'cyan',attrs=["bold"]))
        for laptop in inventory:
            print(termcolor.colored((laptop['modelName'],'  Brand:', laptop['brand'],' :',laptop['quantity'],'in stock'),'light_green',attrs =["bold"]))
            print(termcolor.colored(("--------------------------------------------------------------------------------------------------------------------------"),'cyan',attrs=["bold"]))

        # Main program
        print("Welcome to our laptop store!")
        mode = input(termcolor.colored(('Do you like to (o)rder inventory or (s)ell to a customer?(q for quit): '),'yellow',attrs=["bold"])).lower()

        if mode == 'o':
            order()
        elif mode == 's':
            sale()
        elif mode == 'q':
            print('Goodbye!')
            exit()
        else:
            print('Enter a valid input.')
            main()
    except Exception as e:
        print(f"Error: {e}")



	
main()



