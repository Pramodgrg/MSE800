def isfloat(n):
  """ 
  If string can be converted to floating number 
  returns that number, otherwise returns false
  """
  try:
    n=float(n)
    return n;
  except ValueError:
     return False;

def inputfloat(hint):
  """ 
  Prints hint and asks to enter number.
  Repeats until decimal number is entered.
  """
  ret = False
  while ret is False:
    ret = isfloat(input(hint))
    if ret is False:
      print("Please enter number")
  return ret 

class BMIcalculator:
  def getdata(self):
    """
    Get weight in kgs and height in cms.
    Height is entered in cetimetres and stored in metres
    """

    self.weight = inputfloat("Please enter your weight in kilograms:")
    self.height = inputfloat("Please enter your height in centimetres:")/100

  def calculate(self):
    """
    Calculate and return bmi
    """

    return round(self.weight/(self.height ** 2),2)

  def givingadvice(self):
    """
    Gives advice based on bmi
    """

    bmi = self.calculate()
    if bmi < 18.5:
      print("You are underweight.")
    elif 18.5 <= bmi < 24.9:
      print("You have a normal weight.")
    elif 25 <= bmi < 29.9:
      print("You are overweight.")
    else:
      print("You are obese.")


def main():
  print("\n","="*42,"\n")
  print("Hello, let's calculate your BMI.");
  
  calc = BMIcalculator()
  print()
  calc.getdata()
  bmi=calc.calculate()
  print(f"Your BMI is {bmi}")
  calc.givingadvice()
  print("\n","="*42,"\n")

if __name__ == "__main__":
    main()