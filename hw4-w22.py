
import unittest

## Name : Renee Du
## Student ID: 97626101
## People you worked with :


# The Customer class
# The Customer class represents a customer who will order from the restaurants.
class Customer: 
    # Constructor
    def __init__(self, name, card = 120):
        self.name = name
        self.card = card

    # Load some deposit onto the customer's card.
    def load_card(self, deposit):
        self.card += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, waiter, restaurant, item_name, quantity):
        if not(waiter.has_restaurant(restaurant)):
            print("Sorry, we don't have that restaurant. Please try a different one.")
        elif not(restaurant.has_item(item_name, quantity)):  
            print("Our restaurant has run out of " + item_name + " :( Please try a different restaurant!")
        elif self.card < waiter.estimated_cost(restaurant, quantity): 
            print("Don't have enough money for that :( Please load more money!")
        else:
            bill = waiter.place_order(restaurant, item_name, quantity) 
            self.submit_order(waiter, restaurant, bill) 
    
    # Submit_order takes a waiter, a restaurant and an amount as parameters, 
    # it deducts the amount from the customer’s card and calls the receive_payment method on the waiter object
    def submit_order(self, waiter, restaurant, amount): 
        self.card -= amount
        waiter.receive_payment(restaurant, amount)


    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.card) + " on my card."


# The Waiter class
# The Waiter class represents a waiter at the market. 
class Waiter:

    # Constructor
    def __init__(self, name, directory =[], service_fee = 10, wallet = 0):
        self.name = name
        self.directory = directory[:] # make a copy of the directory
        self.service_fee = service_fee
        self.wallet = wallet

    # Whether the restaurant is in the waiter's directory
    def has_restaurant(self, restaurant):
        return restaurant in self.directory

    # Adds a restaurant to the directory of the waiter.
    def add_restaurant(self, new_restaurant):
        self.directory.append(new_restaurant)

    # Returns the estimated cost of an order, namely the cost of the foods (quantity times cost)
	# plus the server's own service fee .
    def estimated_cost(self, restaurant, quantity):
        return ((restaurant.cost * quantity) + self.service_fee)

    # Receives payment from customer, and adds service fee to wallet 
    # then adds the money minus the service fee to the restaurant's earnings.
    def receive_payment(self, restaurant, money):
        #add service fee to the waiter's wallet
        self.wallet += self.service_fee
        restaurant.earnings += (money - self.service_fee)

    # Places an order at the restaurant.
	# The waiter pays the restaurant the cost.
	# The restaurant processes the order
	# Function returns cost of the order, using estimated_cost method
    def place_order(self, restaurant, item, quantity):
        restaurant.process_order(item, quantity)
        return self.estimated_cost(restaurant, quantity)  
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " waiter. We take debit cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the food market."

## Complete the restaurant class here following the instructions in HW_4_instructions_rubric
class Restaurant:
    
    def __init__(self, name, inventory, cost = 5, earnings=0):
        self.name = name
        self.inventory = {}
        self.inventory.update(inventory)
        self.cost = cost
        self.earnings = earnings
    
    
    def has_item(self, item, quantity): 
        if item in self.inventory.keys():
            if self.inventory[item] >= quantity:
                return True
            
        return False



    def process_order(self, item, quantity):
        if self.has_item(item, quantity):
            self.inventory[item] = self.inventory.get(item) - quantity
   
    def stock_up(self, item, number):
        if item in self.inventory:
            self.inventory[item] += number
        else:
            self.inventory[item] = number

    def __str__ (self): 
        return "Hello, we are" + self.name + "This is current menu" + str(self.inventory.keys()) + "We charge" + self.cost + "per item. We have" + self.earnings + "in total."




class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        self.inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Restaurant("The Grill Queen", self.inventory, cost = 10)
        self.s2 = Restaurant("Tamale Train", self.inventory, cost = 9)
        self.s3 = Restaurant("The Streatery", self.inventory)
        self.c1 = Waiter("West")
        self.c2 = Waiter("East")
        self.c3 = Waiter("Ann")
        #the following codes show that the two waiters have the same directory
        for c in [self.c1, self.c2, self.c3]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_restaurant(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.card, 120)
        self.assertEqual(self.f2.card, 150)

	## Check to see whether constructors work
    def test_waiter_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #waiter holds the directory - within the directory there are three restaurants
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_restaurant_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the restaurant can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Restaurant("Misc restaurant", inventory)

		# Testing whether restaurant can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_card = self.f2.card
        previous_earnings_restaurant = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.card, previous_custormer_card - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_restaurant + 20)


	# Check to see that the server can serve from the different restaurants
    def test_adding_and_serving_restaurant(self):
        c3 = Waiter("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_restaurant(self.s1))
        self.assertFalse(c3.has_restaurant(self.s3)) 
        c3.add_restaurant(self.s3)
        self.assertTrue(c3.has_restaurant(self.s3))
        self.assertEqual(len(c3.directory), 3)

   ## Check to see if receive_payment works
    def test_receive_payment(self):
        f4 = Customer("Megan", 150)
        s4 = Restaurant("Fleetwood", self.inventory, cost = 10) 
        c4 = Waiter("Mel", directory = [s4])
        self.assertEqual(c4.wallet, 0)  
        f4.validate_order(c4,s4,"Taco",4) 
        self.assertEqual(c4.wallet, 10) 

	# Check that the restaurant can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases
        # Test to see if has_item returns True when a restaurant has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the restaurant does not have this food item: 
        self.assertEqual(self.s1.has_item("Fish", 20), False) 
        # Test case 2: the restaurant does not have enough food item: 
        self.assertEqual(self.s2.has_item("Burger", 90), False) 
        # Test case 3: the restaurant has the food item of the certain quantity: 
        self.assertEqual(self.s3.has_item("Taco", 10), True) 

	# Test validate order
    def test_validate_order(self):
    
		# case 1: test if a customer doesn't have enough money on their card to order
        # The below test is incorrect since it doesn't test validate_order correctly. Please fix the test below. 
        # Think about how to test a method when the method doesn't return anything 
        # (hint: think about what values change or don't change)
        self.f1.validate_order(self.c1, self.s1, 'Burger', 100)
        self.assertTrue(self.s1.has_item('Burger', 30))
        self.assertEqual(self.f1.card, 120)

		# case 2: test if the restaurant doesn't have enough food left in stock
        self.f1.validate_order(self.c1, self.s1, 'Burger', 90)
        self.assertFalse(self.s1.has_item('Burger', 90))

		# case 3: check if the waiter can order item from that restaurant
        self.f1.validate_order(self.c3, self.s1, 'Burger', 3)    
        self.assertEqual(self.c3.wallet, 10)
        

    # Test if a customer can add money to their card
    def test_load_card(self):
        self.f1.load_card(15)
        self.assertEqual(self.f1.card, 135) 
        self.f2.load_card(40)
        self.assertEqual(self.f2.card, 190)
        self.f2.load_card(10)
        self.assertEqual(self.f2.card, 200)

    
### Write main function
def main():
    # Create at least 3 inventory dictionaries with at least 3 different types of food.
    # The dictionary keys are the food items and the values are the quantity for each item.
    # Create at least 2 Customer objects. Each should have a unique name and unique amount of money on their card.
    # Create at least 3 Restaurant objects. Each should have a unique name, 
    # inventory (use the inventory that you just created), and cost.
    # Create at least 2 Waiter objects. Each should have a unique name and directory (a list of restaurants).
    inventory1 = {"Sushi":40, "Rice":50, "Soup":20}
    inventory2 = {"Kongfu Chicken":20, "Bobba Tea":60, "Hot Pot": 30}
    inventory3 = {"Peach":40, "Mango":90, "Banana": 10}
    f1 = Customer("Amy", 100)
    f2 = Customer("Kevin", 150)
    s1 = Restaurant("Sushi Shop", inventory1, cost = 15)
    s2 = Restaurant("Hot Pot Lee", inventory2, cost = 20)
    s3 = Restaurant("Frutas de la Abuela", inventory3, cost = 5)
    c1 = Waiter("Jack")
    c2 = Waiter("Ben") 
    c3 = Waiter("Ann")
    c1.add_restaurant(s1)
    c1.add_restaurant(s3)
    c2.add_restaurant(s2)
    c3.add_restaurant(s1)
    c3.add_restaurant(s2)
    c3.add_restaurant(s3)

    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases
    #case 1: the waiter does not have the restaurant 
    print("Test validate_order(c1, 'Fashi', 'Rice', 14), return 'Sorry, we don't have that restaurant. Please try a different one.'")
    f1.validate_order(c1, 'Fashi', 'Rice', 14)
    print("Test validate_order(c1, 'Ben Bakery', 'Bobba Tea', 4), return 'Sorry, we don't have that restaurant. Please try a different one.'")
    f2.validate_order(c2, 'Ben Bakery', "Bobba Tea", 4)

    #case 2: the casher has the restaurant, but not enough ordered food or the ordered food item
    print("Test validate_order(c1, s2, 'Banana', 20), return 'Our restaurant has run out of Banana :( Please try a different restaurant!'")
    f1.validate_order(c2, s3, "Banana", 20)
    print("Test validate_order(c1, s2, 'Bobba Tea', 800), return 'Our restaurant has run out of Bobba Tea :( Please try a different restaurant!'")
    f2.validate_order(c2, s2, "Bobba Tea", 800)

    #case 3: the customer does not have enough money to pay for the order: 
    print("Test validate_order(c1, s2, 'Hot Pot', 25), return 'Don't have enough money for that :( Please load more money!'")
    f1.validate_order(c2, s2, "Hot Pot", 25)
    print("Test validate_order(c1, s2, 'Sushi', 30), return 'Don't have enough money for that :( Please load more money!'")
    f2.validate_order(c1, s1, "Sushi", 30)

    #case 4: the customer successfully places an order
    print("Test validate_order(c1, s2, 'Peach', 5), return nothing as the order can be placed")
    f1.validate_order(c1, s3, "Peach", 5)
    print("Test validate_order(c1, s2, 'Mango', 4), return nothing as the order can be placed")
    f2.validate_order(c1, s3, "Mango", 4)




if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
