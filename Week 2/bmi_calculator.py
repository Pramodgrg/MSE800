class BMICalculator:
    def calculate_bmi(weight, height):
        bmi = weight / (height ** 2)
        return bmi 
    

def main():
    weight = float(input("Enter your weight in kg: "))
    height = float(input("Enter your height in centimeters: "))
    # converting height from centimeters to meters
    height = height / 100  
    bmi = BMICalculator.calculate_bmi(weight, height)
    print(f"Your BMI is: {bmi:.2f}")
if __name__ == "__main__":
    main()