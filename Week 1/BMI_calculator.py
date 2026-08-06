## Getting user input for name, age, height, and weight
name = input("Enter your name: ")
age = int(input("Enter your age: "))

while True:
    unit_system = input("Enter the preferred unit system (metric/imperial)\n Metric(Kg,cm), Imperial(lbs,in): ").strip().lower()
    if unit_system in ["metric", "imperial"]:
        break
    print("Invalid unit system. Please enter 'metric' or 'imperial'.")

print("You have selected the " + unit_system + " system.")

height = float(input("Enter your height in centimeters: ")) if unit_system == "metric" else float(input("Enter your height in inches: ")) 
weight = float(input("Enter your weight in kilograms: ")) if unit_system == "metric" else float(input("Enter your weight in pounds: "))



if unit_system.lower() == "imperial":
    height = height * 0.0254  # Convert inches to meters
    weight = weight * 0.453592  # Convert pounds to kilograms

if unit_system.lower() == "metric":
    height = height / 100  # Convert centimeters to meters
    weight = weight  # Weight is already in kilograms

##calculating BMI
bmi = weight / (height ** 2)



def main():
    print("Hello, " + name + "! You are " + str(age) + " years old.")
    print("Your BMI is: " + str(round(bmi, 2)))

    if bmi < 18.5:
        print("You are underweight.")
    elif 18.5 <= bmi < 24.9:
        print("You have a normal weight.")
    elif 25 <= bmi < 29.9:
        print("You are overweight.")
    else:
        print("You are obese.")

if __name__ == "__main__":
    main()