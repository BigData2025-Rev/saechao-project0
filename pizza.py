import json


class Pizza:
    def __init__(self, pizza_type, size, toppings):
        self.pizza_type = pizza_type
        self.size = size
        self.toppings = toppings
        self.cost = 0

    def calculate_cost(self, pizza_types, sizes, toppings):
        if self.pizza_type in pizza_types:
            self.cost += pizza_types[self.pizza_type][1]

        if self.size in sizes:
            self.cost += sizes[self.size][1]

        for topping in self.toppings:
            if topping in toppings:
                self.cost += toppings[topping][1]

    def get_pizza_type_name(self, pizza_types):
        return pizza_types.get(self.pizza_type)[0]

    def get_size_name(self, sizes):
        return sizes.get(self.size)[0]

    def get_toppings_names(self, toppings):
        return [toppings[topping][0] for topping in self.toppings if topping in toppings]


class Order:
    def __init__(self):
        self.name = ""
        self.pizzas = []
        self.total_cost = 0

    def get_name(self):
        self.name = input('Can we get a name for the order?\n')
        return self.name

    def add_pizza(self, pizza):
        self.pizzas.append(pizza)
        self.total_cost += pizza.cost

    def import_order(self, file_path, pizza_types, sizes, toppings):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.name = data.get("name")

                for pizza_data in data.get("pizzas", []):
                    pizza_type = pizza_data.get("pizza_type")
                    size = pizza_data.get("size")
                    pizza_toppings = pizza_data.get("toppings", [])

                    pizza = Pizza(pizza_type, size, pizza_toppings)
                    pizza.calculate_cost(pizza_types, sizes, toppings)
                    self.add_pizza(pizza)
        except Exception as e:
            print(f"Error importing order: {e}")

    def export_order(self, file_path):
        try:
            data = {
                "name": self.name,
                "pizzas": [
                    {
                        "pizza_type": pizza.pizza_type,
                        "size": pizza.size,
                        "toppings": pizza.toppings,
                        "cost": pizza.cost
                    } for pizza in self.pizzas
                ],
                "total_cost": self.total_cost
            }
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
                print(f"Order successfully exported to {file_path}")
        except Exception as e:
            print(f"Error exporting order: {e}")

    def show_order_summary(self, pizza_types, sizes, toppings):
        print(f"\nOrder Summary for {self.name}")
        cost = 0
        for idx, pizza in enumerate(self.pizzas, start=1):
            pizza_type_name = pizza.get_pizza_type_name(pizza_types)
            size_name = pizza.get_size_name(sizes)
            toppings_names = ", ".join(pizza.get_toppings_names(toppings))
            print(f"Pizza {idx}: {pizza_type_name}\nSize: {size_name}\nToppings: {toppings_names}\nCost: ${pizza.cost:.2f}\n")
            cost += pizza.cost
        print(f"\nTotal Cost {cost}")


class PizzaOrder:
    def __init__(self):
        self.pizza_types = {
            '1': ('Pepperoni', 11.00),
            '2': ('Cheese', 7.00),
            '3': ('Create Your Own', 5.00)
        }
        self.sizes = {
            '1': ('Small', 0),
            '2': ('Medium', 2.00),
            '3': ('Large', 4.00)
        }
        self.toppings = {
            '1': ('Mushrooms', 1.50),
            '2': ('Olives', 1.50),
            '3': ('Cheese', 2.00),
            '4': ('Bell Peppers', 1.00),
            '5': ('Bacon', 4.00),
            '6': ('Onions', 2.50),
            '7': ('Jalapeno', 2.50),
            '8': ('Pepperoni', 4.00),
            '9': ('Chicken', 4.00),
        }

    def show_pizza_types(self):
        print("\nPizza Types:")
        for key, (pizza, price) in self.pizza_types.items():
            print(f"{key}: {pizza} - ${price}")

    def show_sizes(self):
        print("\nSizes:")
        for key, (size, price) in self.sizes.items():
            print(f"{key}: {size} - ${price}")

    def show_toppings(self):
        print("\nToppings:")
        for key, (topping, price) in self.toppings.items():
            print(f"{key}: {topping} - ${price}")


if __name__ == "__main__":
    pizza_order_system = PizzaOrder()
    print("\nPizza Ordering System")
    
    while True:
        print("\nMain Menu:")
        choice = input("[1] Order Pizza\n[2] Import Order\n[3] Export Order\n[4] Exit\n")
        
        if choice == "1":
            order = Order()
            order.get_name()
            
            while True:
                print("\nChoose a pizza type:")
                pizza_order_system.show_pizza_types()
                pizza_type = input("Enter the pizza type number: ")

                if pizza_type not in pizza_order_system.pizza_types:
                    print("Invalid pizza type. Try again.")
                    continue

                print("\nChoose a size:")
                pizza_order_system.show_sizes()
                size = input("Enter the size number: ")

                if size not in pizza_order_system.sizes:
                    print("Invalid size. Try again.")
                    continue

                print("\nChoose toppings (enter numbers separated by commas):")
                pizza_order_system.show_toppings()
                topping_choices = input("Enter topping numbers: ").split(',')

                pizza = Pizza(pizza_type, size, topping_choices)
                pizza.calculate_cost(pizza_order_system.pizza_types, pizza_order_system.sizes, pizza_order_system.toppings)
                order.add_pizza(pizza)
                print(f"Pizza added! Cost: ${pizza.cost:.2f}")

                another = input("Would you like to add another pizza? (y/n): ")
                if another.lower() != 'y':
                    break
            
            order.show_order_summary(pizza_order_system.pizza_types, pizza_order_system.sizes, pizza_order_system.toppings)

        elif choice == "2":
            file_path = input("Enter the file path to import order: ")
            order = Order()
            order.import_order(file_path, pizza_order_system.pizza_types, pizza_order_system.sizes, pizza_order_system.toppings)
            order.show_order_summary(pizza_order_system.pizza_types, pizza_order_system.sizes, pizza_order_system.toppings)

        elif choice == "3":
            file_path = input("Enter the file path to export order: ")
            order.export_order(file_path)

        elif choice == "4":
            break

        else:
            print("Invalid choice. Please try again.")
