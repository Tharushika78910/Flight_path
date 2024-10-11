import random
import mysql.connector

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='12345',
            database='flight_path',
            autocommit=True

        )
        if conn.is_connected():
            print(" ")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None



def get_airport_codes():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Query to get the airport_code column from your table
    query = "SELECT airport_code FROM new_airports"
    cursor.execute(query)

    # Fetch all results and store in the airports list
    airports = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return airports

airports = get_airport_codes()

# Select 3 random airports that will have unfavourable weather conditions
fuel_leak_airports = random.sample(airports, 3)


class Airplane:
    def __init__(self, start_airport, destination_airport, initial_fuel=1000, money=2000):
        self.current_airport = start_airport
        self.destination_airport = destination_airport
        self.fuel = initial_fuel
        self.money = money
        self.cargo_collected = 0
        self.fuel_leak = False

    def fly_to(self, next_airport):
        distance = random.randint(100, 500)       # Random distance in km
        fuel_needed = distance * 2.0                      # Fuel consumption per km

        # Check if next airport has an unfavourable weather condition.

        if next_airport in fuel_leak_airports:
            self.fuel_leak = True
            fuel_needed *= 3.0                      # Increase fuel consumption by 50%
            print(f"Warning: Unfavourable weather condition at {next_airport}! Fuel consumption is higher.")
        else:
            self.fuel_leak = False

        if self.fuel >= fuel_needed:
            self.fuel -= fuel_needed
            self.current_airport = next_airport
            print(f"Flew to {next_airport}. Fuel remaining: {self.fuel:.2f}")
        else:
            print("Not enough fuel to fly to the next airport!")
            return False

        def check_game_over(fuel, money):
            if fuel < (fuel_needed) and money <= 0:
                print("\nYou're out of fuel and money. You can't continue your journey.")
                print("Game Over! Better luck next time, captain.")
                return True
            return False

        return True

    def buy_fuel(self, amount):
        fuel_cost = 2                   # Assume 2 money units per unit of fuel
        cost = amount * fuel_cost
        if self.money >= cost:
            self.money -= cost
            self.fuel += amount
            print(f"Bought {amount} fuel for {cost} money units. Fuel now: {self.fuel}, Money left: {self.money}")
        else:
            print("Not enough money to buy fuel!")

    def collect_cargo(self):
        self.cargo_collected += 1
        print(f"Cargo collected. Total cargo: {self.cargo_collected}")

    def status(self):
        print(f"Current airport: {self.current_airport}, Destination: {self.destination_airport}")
        print(f"Fuel: {self.fuel}, Money: {self.money}, Cargo: {self.cargo_collected}")



def start_flight(username, airplane):
    while True:
        print("\nChoose an action:")
        print("1) Fly to next airport")
        print("2) Buy fuel")
        print("3) Collect cargo")
        print("4) Check status")
        print("5) Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Choose next airport
            next_airport = random.choice([airport for airport in airports if airport != airplane.current_airport])
            if airplane.fly_to(next_airport):
                if airplane.current_airport == airplane.destination_airport:
                    print(f"Congratulations! You've reached {airplane.destination_airport} and completed the flight!")
                    break
        elif choice == "2":
            amount = int(input("Enter amount of fuel to buy: "))
            airplane.buy_fuel(amount)
        elif choice == "3":
            airplane.collect_cargo()
        elif choice == "4":
            airplane.status()
        elif choice == "5":
            print("Game over!!! Better luck next time!")
            break
        else:
            print("Invalid choice!")


def load_player_data(username):
    print(f"Welcome, {username}! Starting a new flight.")
    start_airport = random.choice(airports)
    destination_airport = random.choice([airport for airport in airports if airport != start_airport])
    airplane = Airplane(start_airport, destination_airport)

    return airplane

#Giving game instructions to the user
print("Welcome to Flight Path!")
print("\n")
print("** You must successfully reach the designated destination by collecting cargoes to achieve victory.")
print("** You must manage fuel until you reach the destination, if fuel is insufficient you can buy additional fuel using available funds.")
print("\n")
print("Prepare for takeoff and chart your course through 10 airports, managing fuel and cargo wisely. \nGood luck, captain!")
print("\n")
username = input("Enter your username: ")

airplane = load_player_data(username)
start_flight(username, airplane)