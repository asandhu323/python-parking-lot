import json
import os
import re


def save_cars_list(cars_list, car_file):
    """ Save the cars_list as json in the car_file """
    car_file = open(car_file, "w")
    car_json = json.dumps(cars_list, indent=4)
    car_file.write(car_json)
    car_file.close()


def load_cars_list(car_file):
    """ Returns the list of cars from the file """
    if os.path.isfile(car_file):
        cars_file = open(car_file)
        cars_data = cars_file.read()
        cars_file.close()
        cars_list = json.loads(cars_data)
    else:
        cars_list = []

    return cars_list


def get_new_car():
    """ Gets data for a new car from the user and validates it """

    make = input("Enter make: ")
    if re.search("^[A-Za-z0-9 ]+$", make) is None:
        raise ValueError("The Make is invalid")

    model = input("Enter model: ")
    if re.search("^[A-Za-z0-9 ]+$", model) is None:
        raise ValueError("The Model is invalid")

    year = input("Enter year: ")
    if re.search("^\d{4}$", year) is None:
        raise ValueError("The Year is invalid")
    if int(year) <= 1900:
        raise ValueError("The Year is invalid")

    license = input("Enter License: ")
    if re.search("^[A-Z0-9]+$", license) is None:
        raise ValueError("The License is invalid")

    return make, model, year, license


def does_license_exist(license, cars_list):
    """ Checks if license exists in cars_list, return True if it does and False otherwise"""
    for car in cars_list:
        if car["license"] == license:
            return True
    return False


def main():
    quit = False
    cars_list = load_cars_list("cars.json")

    while not quit:
        user_selection = input("Add Car(a), List Cars(n), Find Car(f), Remove Car(r) or Quit(q)")

        try:
            if user_selection == "a":
                make, model, year, license = get_new_car()
                if not does_license_exist(license, cars_list):
                    car = {"make": make, "model": model, "year": int(year), "license": license}
                    cars_list.append(car)
                    save_cars_list(cars_list, "cars.json")
                else:
                    print("Car already exists in the Parking Lot")

            elif user_selection == "n":
                if len(cars_list) > 0:
                    for car in cars_list:
                        print("%d %s %s with license plate %s." % (car["year"], car["make"], car["model"], car["license"]))
                else:
                    print("No cars yet")

            elif user_selection == "f":
                license = input("Enter license: ")
                if re.search("^[A-Z0-9]+$", license) is None:
                    raise ValueError("Invalid License Search Term")

                found_match = False
                for car in cars_list:
                    if license.lower() in car["license"].lower():
                        print("%d %s %s with license plate %s." % (car["year"], car["make"], car["model"], car["license"]))
                        found_match = True
                if not found_match:
                    print("No car found.")

            elif user_selection == "r":
                license = input("Enter License: ")
                if re.search("^[A-Z0-9]+$", license) is None:
                    raise ValueError("Invalid License")

                is_found = False
                for car in cars_list:
                    if car["license"] == license:
                        cars_list.remove(car)
                        save_cars_list(cars_list, "cars.json")
                        print("Car with license %s remove from the parking lot." % license)
                        is_found = True
                        break
                if not is_found:
                    print("No car found.")

            elif user_selection == "q":
                print("Quitting Program")
                quit = True

            else:
                print("Invalid Selection. Try Again.")

        except ValueError as e:
            print("Value Error: %s" % e)


if __name__ == "__main__":
    main()
