'''
Name    : Sara Volk
Program : Five Functions Program
Date    : November 13, 2024
Purpose : To create a program that performs a series of tasks. The program 
          will repeatedly perform the wanted task until the user wants to exit 
          the program. This will demonstrate my understanding of using functions, 
          parameters, return values, strings, and loops.

Functions used:

wordCount: Counts the number of words in a given string.
    Parameters:
        text: the user's string.

    Return value: the count of how many words is found in the string.

isPrime: Determines if the given argument (parameter) value is a prime number or not.
    Parameters:
        number: the user's POSITIVE integer.

    Return value: True if the user's number is a prime number or False if user's number 
                  is not a prime number.

midPoint: Calculates the midpoint of the given two points in the form 'x, y'.
    Parameters:
        coordinate1: the x and y values of the first point.
        coordinate2: the x and y values of the seocnd point.

    Return value: the coordinates of the midpoint of the user's two points in the
                  in the form "(x, y)".

slope: Calculates the slope of a line, given the coordinates of two points on the line 
       by the user in the form 'x, y'. Ensure to handle horizontal and vertical lines.
    Parameters:
        coordinate1: the x and y values of the first point.
        coordinate2: the x and y values of the seocnd point.

    Return value: the slope value of the line based on the two points 
                  the user provides.

isValidDate: Determines if the given string is a valid date (i.e. has correct ranges 
             for month and day), taking account of leap years. 
             Required format: "dd/mm/yyyy"
    Parameters:
        date: the user's date

    Return value: True if the user's date is valid or False if the user's date is
                  invalid. Also returns False if the format is invalid.
'''

# Defines the function, wordCount()
# The method of counting the amount of words in a given string is through counting the number of spaces
def wordCount(text):

    # sets the variable, count, to 1 (since the number of spaces is always one less than the amount of words)
    count = 1

    # The code in the for-loop will keep repeating until it's finished iterating each character in the user's text
    for char in text:

        # During the iteration process, if the character is a space, the following code in the if-block will be executed
        if char == " ":
            # A space is a separator of two words. Thus if there's a space, there must be another word.
            count += 1

    # Once the for-loop has stopped, the value of the variable, count, is returned to the section of the program the function was called upon
    return count


# Defines the function, isPrime()
def isPrime(number):

    # If the user's number is 0 or 1, the function will return False (0 and 1 are not prime numbers)
    if (number == 0) or (number == 1):
        return False
    
    # If the user's number is not 0 or 1, the following code in the else-block will be executed
    else:

        # The code in the for-loop will keep repeating until it's finished iterating every value in the range from 2 to user's number - 1
        for i in range(2, number):
            
            # If the remainder is 0 after dividing the user's number by a value in the range from 2 to user's number - 1, the function will return False
            if (number % i == 0):
                return False
            
        # If the user's number was not divisble by any value in the range from 2 to user's number - 1, the function will return True
        return True


# Defines the function, midPoint()
def midPoint(coordinate1, coordinate2):

    # Splits each element in the variable, coordinate1, that's separated by ', ' into a list
    # Converts each element into an integer 
    # Stores each element into the variables, x1 and y1
    x1, y1 = map(int, coordinate1.split(', '))

    # Splits each element in the variable, coordinate2, that's separated by ', ' into a list
    # Converts each element into an integer 
    # Stores each element into the variables, x2 and y2
    x2, y2 = map(int, coordinate2.split(', '))

    # Calculates the x-value of the midpoint
    xMidpoint = (x1 + x2) / 2

    # Calculates the y-value of the midpoint
    yMidpoint = (y1 + y2) / 2

    # Converts the x and y values of the midpoint into a string and combines them in the form (x,y)
    midpoint = "(" + str(xMidpoint) + ", " + str(yMidpoint) + ")"

    # Returns the value of the variable, midpoint
    return midpoint


# Defines the function, slope()
def slope(coordinate1, coordinate2):

    # Splits each element in the variable, coordinate1, that's separated by ', ' into a list
    # Converts each element into an integer 
    # Stores each element into the variables, x1 and y1
    x1, y1 = map(int, coordinate1.split(', '))

    # Splits each element in the variable, coordinate2, that's separated by ', ' into a list
    # Converts each element into an integer 
    # Stores each element into the variables, x2 and y2
    x2, y2 = map(int, coordinate2.split(', '))

    # When x-values are the same, the line is vertical, and there is no slope
    if x1 == x2:
        slope = "Vertical line. No slope"
    
    # When y-values are the same, the line is horizontal, and the slope is 0
    elif y1 == y2:
        slope = 0

    # If the line is neither vertical or horizontal, the slope will be calculated
    else:
        slope = (y2 - y1) / (x2 - x1)

    # Returns the value of the variable, slope
    return slope


# Defines the function, isValidDate()
def isValidDate(date):
    
    # Splits each element in the variable, date, that's separated by '/' into a list
    # Converts each element into an integer 
    # Stores each element into the variables, day, month, and year
    try:
        day, month, year = map(int, date.split('/'))

    # If the format of the user's date is invalid (causes a ValueError), the return value is False
    except ValueError:
        return False

    # List of all months with 31 days
    monthsThirtyOne = [1, 3, 5, 7, 8, 10, 12]

    # List of all months with 30 days
    monthsThirty = [4, 6, 9, 11]
    
    # If month is in the list monthsThirtyOne, the following code in the if-block will be executed
    if month in monthsThirtyOne:

        # If the user day is greater than 31 or is less/equal to 0, the return value is False
        if (day > 31) or (day <=0):
            return False

        # If day > 0 or day <= 31, the return value is True
        else: 
            return True
    

    # If month is in the list monthsThirty, the following code in the elif-block will be executed
    elif month in monthsThirty:

        # If day is greater than 30 or is less/equal to 0, the return value is False
        if (day > 30) or (day <= 0):
            return False

        # If day > 0 or day <= 30, the return value is True
        else: 
            return True


    # If month is equal to 2, the following code in the else-block will be executed
    elif month == 2:

        # If year is a century and divisible by 400 or is not a century and is divisible by 4, then it's a leap year
        if (year % 100 == 0 and year % 400 == 0) or (year % 100 != 0 and year % 4 == 0):    

            # If day is greater than 29 or is less/equal to 0, the return value is False
            if (day > 29) or (day <= 0):
                return False
            
            # If day > 0 or day <= 29, the return value is True
            else:
                return True
        
        # Not a leap year
        else:

            # If day is greater than 28 or is less/equal to 0, the return value is False
            if (day > 28) or (day <= 0):
                return False
            
            # If day > 0 or day <= 28, the return value is True
            else:
                return True
            

    # If month is not in the lists monthsThirtyOne or monthsThirty, or is not equal to 2, the return value is False
    else: 
        return False



# Main Program
print("Hello! Welcome to the Five Functions Program!")

# Sets the variable, programOn, empty
programOn = ""

# The code in the while-loop will keep repeating until the variable, programOn, equals to "exit".
while programOn != "exit":

    # Instructions
    print("\nPlease choose one of the five tasks below.\nIf you would like to exit the program, please enter 'exit'.\n")
    
    # Tasks the program can perform
    print("A. Determine the amount of words in a text")
    print("B. Determine if a given number is a prime number")
    print("C. Calculate Midpoint")
    print("D. Calculate Slope")
    print("E. Determine if the given date is valid")

    # Asks user what they would like to do
    programOn = input("\nEnter the corresponding letter to the task you wish to do: ").lower()


    # If user inputs "exit" as the "task" they would like to do, the program will end.
    if programOn == "exit":

        # Displays friendly message before ending the program
        print("\nThank you for using the Five Functions Program. The program has now ended.")


    # If user inputs "a" (determine the amount of words in a text) as the "task" they would like to do, the following code in the elif-block will be executed
    elif programOn == "a":

        # Asks the user for text; no word limit
        userText = input("\nPlease enter text you want the program to calculate: ")

        # Calls on the function, wordCount(text), and stores the returned value into the variable, userTextWordCnt
        userTextWordCnt = wordCount(userText)

        # Displays the number of word in the user's text
        print(f"\nYour text has {userTextWordCnt} words!")

        input("\nPlease press enter to continue!")


    # If user inputs "b" (determine if a given number is a prime number)
    elif programOn == "b":

        # Will keep asking for a number through the while-loop until user inputs valid input (userNumber >= 0)
        while True:

            # Asks user for a number (specifically, a positive integer)
            userNumber = int(input("\nPlease enter a number you want the program to determine: "))

            # If input number is less than 0, it is invalid and will ask for user input again
            if userNumber < 0:
                print("\nPlease enter a positive integer.\n")

            # If userNumber >= 0, while-loop will break and will move onto next portion of the program
            else:
                break
        
        # Calls on the function, isPrime(number), and stores the returned value into the variable, result
        result = isPrime(userNumber)

        # Displays True or False, depending whether or not the user's number is a prime number
        print(f"\n{result}")

        input("\nPlease press enter to continue!")


    # If user inputs "c" (calculate Midpoint)
    elif programOn == "c":
        
        # Asks user for x and y values for the first point
        firstCoordinateMid = input("\nPlease enter the coordinates of one point in the format 'x, y'     : ")

        # Asks user for x and y values for the second point
        secondCoordinateMid = input("Please enter the coordinates of another point in the format 'x, y' : ")

        # Calls on the function, midPoint(coordinate1, coordinate2), and stores the returned value into the variable, midpointResult
        midpointResult = midPoint(firstCoordinateMid, secondCoordinateMid)

        print(f"\nThe midpoint of your two points is {midpointResult}")

        input("\nPlease press enter to continue!")


    # If user inputs "d" (calculate Slope)
    elif programOn == "d":

        # Asks user for x and y values for the first point
        firstCoordinateSlope = input("\nPlease enter the coordinates of one point in the format 'x, y'     : ")

        # Asks user for x and y values for the second point
        secondCoordinateSlope = input("Please enter the coordinates of another point in the format 'x, y' : ")

        # Calls on the function, slope(coordinate1, coordinate2), and stores the returned value into the variable, slopeResult
        slopeResult = slope(firstCoordinateSlope, secondCoordinateSlope)

        print(f"\nSlope: {slopeResult}")

        input("\nPlease press enter to continue!")


    # If user inputs "e" (determine if the given date is valid) 
    elif programOn == "e":

        # Asks user for a date
        userDate = input("\nPlease enter a date in the format 'dd/mm/yyyy': ")

        # Calls on the function, isValidDate(date), and stores the returned value into the variable, dateResult
        dateResult = isValidDate(userDate)

        print(f"\n{dateResult}")

        input("\nPlease press enter to continue!")


    # If user input anything but "a", "b", "c", "d", "e", or "exit"
    else:
        print("\nInvalid answer. Please try again.")