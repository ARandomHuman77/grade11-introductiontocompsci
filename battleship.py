'''
Name    : Sara Volk
Program : Battleship
Date    : January 10, 2025
Purpose : To create a program, with a friendly user interface, that lets the user play 
          battleship with a computer. This will demonstrate my understanding of all the 
          concepts learned throughout the course, including variables, functions, parameters, 
          return values, strings, importing other modules, loops, if-else statements, lists, 
          classes, and object-oriented programming.

The overall comments on the used functions and classes are on a separate document.
'''
import pygame, sys, random
from pygame.locals import QUIT

# Map class; both user map and computer map possess the attributes, properties, etc. in the class
class Map:
    # Initializes a Map object with the given x, y coordinates
    def __init__(self, x, y):

        # Defines the file path to the water image for the background of the maps
        imagePath = "C:/Users/Sarav/Downloads/eLearning Computer Science/Final Culminating/Images/water.png"
        
        # Loads the water image
        self.image = pygame.image.load(imagePath)

        # Creates a rectangle for the water image (image is put inside of this rectangle 
        # so it can be displayed on the screen and positioned)
        self.rect = self.image.get_rect()
        
        # Sets the image's x, y position on the screen
        self.rect.x = x
        self.rect.y = y

        # Initialized the empty dictionary "squareCoords." This is used to store all the letter, number
        # coordinates as keys. Each key (coordinate) have x, y values that represent its top-left corner.
        # This is ultimately used to display fire/white circle sprites on each square if guessed and to 
        # "snap" a dropped ship to the closest square. Both maps are attributed this dictionary.
        self.squareCoords = {}

        # Initializes lists to track the squares with hits and misses. Used to display the fire/white 
        # circle sprites on these squares.
        self.hitTracker = []
        self.missTracker = []

        # Calls the function that draws grid lines on the map
        self.drawLine(screen, x, y)

        # Calls the function that make each letter, number coordinate key and assigns each key unique x, y 
        # values (the top-left corner). The key-value pairs are added to the squareCoords dictionary
        self.createSquares(x, y)

    # Draws grid lines on the map
    def drawLine(self, screen, x, y):
        # Loop to draw 11 vertical lines
        for i in range(11):
            # Since each square is 40 x 40 pixels, 40 pixels must be added after each iterations
            lineX = x + i * 40    
            pygame.draw.line(screen, BLACK, (lineX, 50), (lineX, 450), 3)

        # Loop to draw 11 horizontal lines
        for j in range(11):
            lineY = y + j * 40
            pygame.draw.line(screen, BLACK, (x, lineY), (x + 400, lineY), 3)
        
    # Make each letter, number coordinate key and assigns each key unique x, y 
    # values (the top-left corner). The key-value pairs are added to the squareCoords dictionary
    def createSquares(self, x, y):
        
        # Keeps track of the horizontal axis (columns). If i increases by 1, it moves to the next 
        # column (the square to the right). The x-coordinate of each square in different columns 
        # is adjusted by adding 40 pixels "i" times. 
        # Ex. If the loop is on column C, i = 2 and the x-value would increase by 80 pixels (40*2). 
        # This x-value is the same for all of the squares in column C
        i = 0
        for letter in letters:

            # Similar to "i," but keeps track of the vertical axis (rows). If j increases by 1, it moves to
            # the next row (the square below). The y-coordinate of each square in different columns is 
            # adjusted by adding 40 pixels "j" times.
            # Gets reset to 0 after each column (for each new letter).
            j = 0
            for number in numbers:

                # Combine the letter and number to make a coordinate like A3, J8
                square = str(letter) + str(number)

                # Calculate the top-left corner of the square using the current column (i) and row (j).
                squareX = x + (i*40)
                squareY = y + (j*40)

                # Stores the x, y values as a tulpe
                coords = squareX, squareY

                # The key-value (the letter, number coord and its top-left x, y value)
                # pair gets added to the squareCoords dictionary
                self.squareCoords[square] = coords
                
                # Move to the next row
                j += 1

            # Move to the next column
            i += 1

        
# Ship class; all of the user's ships possess the attributes, properties, etc. in the class
class Ship:
    # Initializes a Ship object with the given file image path, x, y coordinates, width, and height
    def __init__(self, imagePath, startX, startY, width, height):

        # Loads the ship image
        self.image = pygame.image.load(imagePath)

        # Rescales the image to the given width and height
        self.image = pygame.transform.scale(self.image, (width, height))

        # Create a rectangle for the image
        self.rect = self.image.get_rect()
        
        # Sets the image's initial x, y position on the screen
        self.rect.x = startX
        self.rect.y = startY

    # Determines the other adjacent squares the dropped ship is occupying and stores them in a list
    def putInList(self, startingSquare):
        
        #Initializes the list that contains its coordinates
        self.posOnMap = []

        # Retrieves the letter and number of the most left square the ship is occupying
        startingLetter = startingSquare[0]
        row = startingSquare[1]

        # Figures out how many squares wide the ship is
        shipSquareWidth = self.rect.width // 40

        # Loops through all items (letters) in the list "letters," but it also takes the index 
        # position of the iterated item and stores it in the variable "pos"
        for pos, letter in enumerate(letters):
            if letter == startingLetter:

                # Will iterate as many times equal to the number of squares wide the ship is, which allows 
                # the proper number of coordinates added to the list
                for i in range(shipSquareWidth):

                    # Since the ships can only be placed horizontally, the row does not change and only the
                    # column (letter) does. To calculate the column, the index position of the inital letter
                    # gets added by "i" where i increases by 1 after each iteration. This new index position is then
                    # used to retrieve an item in the list "letters," which will be the next column. Since "letters" 
                    # is in alphabetical order, the letters retrieved from the list should be consecutive from 
                    # the starting one, allowing it to make coordinates of squares horizontally adjacent 
                    # from each other.
                    occupyingSquare = str(letters[pos + i]) + str(row)

                    self.posOnMap.append(occupyingSquare)
                
                # Breaks the first for-loop
                break
        
        print(self.posOnMap)
    
    # Determines if the dropped ship is within the user's map
    def isWithinBounds(self, mapRect):
        # If the entire ship is within the area of the user's map, then the function returns True
        if mapRect.collidepoint(self.rect.x, self.rect.y) and mapRect.collidepoint(self.rect.x + self.rect.width, self.rect.y + self.rect.height):
            return True

        # If the entire ship is not, the function returns False
        else:
            return False
    
    # Determines if the dropped ship is ontop of another ship
    def isOverlapping(self):
        
        # Loops through all items in the list "ships," which stores all of the user's ships
        for ship in ships:

            # Continues to the next iteration if the iterated ship is the ship that's currently being 
            # checked if for overlapping
            if ship == self:
                continue
            
            try:
                # Loops through all of the squares in the iterated ship's coordinate list (posOnMap)
                for coord in ship.posOnMap:

                    # Retrieves the iterated coordinate's top-left corner x, y values
                    testX = userMap.squareCoords[coord][0]
                    testY = userMap.squareCoords[coord][1]

                    # If the test x, y values match with the x, y value of the dropped ship, the left side 
                    # of the ship is overlapping another. Thus, return True
                    if self.rect.x == testX and self.rect.y == testY:
                        return True
                    
                    # Checks if the right side of the ship is overlapping with another ship
                    if (self.rect.x + self.rect.width - 40) == testX and (self.rect.y) == testY:
                        return True
                    
            # When you place the first ship you'll get this error, and it's because the list, "posOnMap," isn't
            # attributed to any ships yet. Ships have to placed on the map before they get the "posOnMap" list
            except AttributeError:
                continue
                
        return False



# Displays all of the desired text on the game screen
def displayText(text, font, colour, x, y):

    # Renders the text with the given font and colour into an image
    image = font.render(text, True, colour)

    # Displays the image (the rendered text) onto the screen at the given x, y values
    screen.blit(image, (x, y))


# Displays letters (A-J) on the horizontal axis and numbers (0-9) on the vertical axis of a map
def labellingMap(x, y):

    # i is used to move on to the next square to the right
    i = 0
    for j in letters:

        # Calls the function to display the letter
        # Each square is 40 pixels wide, so 40 must be added to the x position after every iteration
        displayText(j, textFont, BLACK, x + (i*40) + 5, 10)

        # Increases by 1 after each iteration to move on to the next square
        i += 1

    # l is used to move on to the square below
    l = 0
    for k in numbers:
        k = str(k)

        # Calls the function to display the number
        # Each square is also 40 pixels tall, so 40 must be added to the y position after every iteration
        displayText(k, textFont, BLACK, x - 30, y + (l*40))

        # Increases by 1 after each iteration to move on to the next square
        l += 1


# Finds the closest square the ship was dropped on based on its top-left corner. The coordinates of the ship's
# top-left corner will be corrected to the x, y values of the closest square
def placementCorrection(shipX, shipY):

    # Iterates through all letter, number coordinates on the user's map. Each coordinate will do the following
    for coord in userMap.squareCoords:

        # Takes the x, y value of the top-left corner of the iterated square coordinate
        squareX = userMap.squareCoords[coord][0]
        squareY = userMap.squareCoords[coord][1]

        # Checks for x, y values 25 pixels to the right of the original x posiiton
        # Not perfectly 40 pixels to the right because anything beyond 25 pixels, the user most likely meant 
        # to drop the ship on the square to the right of the current iterated square
        for i in range(26):
            testX = squareX + i

            # For every test x value, it will check for x, y values 30 pixels down from the original y posiiton
            # Not 40 pixels for the same reason, but vertically
            for j in range(31):
                testY = squareY + j

                # If the test x, y values match with the ship's x, y values
                if testX == shipX and testY == shipY:

                    # Returns the x, y values of the iterated square (the closest square)
                    return userMap.squareCoords[coord][0], userMap.squareCoords[coord][1], coord
            
            # For every test x value, it will ALSO check for x, y values 10 pixels up from the original y posiiton
            # (for more flexibility)
            for k in range(11):
                testY = squareY - k
                if testX == shipX and testY == shipY:
                    return userMap.squareCoords[coord][0], userMap.squareCoords[coord][1], coord
        

        # Checks for x, y values 15 pixels to the left of the original x posiiton
        for i in range(16):
            testX = squareX - i

            # For every test x value, it will check for x, y values 30 pixels down from the original y posiiton
            for j in range(31):
                testY = squareY + j
                if testX == shipX and testY == shipY:
                    return userMap.squareCoords[coord][0], userMap.squareCoords[coord][1], coord
            
            # For every test x value, it will ALSO check for x, y values 10 pixels up from the original y posiiton
            for k in range(11):
                testY = squareY - k
                if testX == shipX and testY == shipY:
                    return userMap.squareCoords[coord][0], userMap.squareCoords[coord][1], coord


# Randomizes ship locations for the computer
def compCoords():

    # This list keeps track of which coordinates are already taken on the computer's map
    # Prevents overlapping ships
    coordsOccupied = []

    # Iterates through all of the keys (ships) in the dictionary "compShips"
    for ship in compShips:

        # The 4 of the 5 ships take up a different amount of squares, so shipSquareWidth has to changed
        # accordingly. shipSquareWidth is used to make sure the right amount of coords are appended to the
        # list in each key.
        if ship == "compDes":
            shipSquareWidth = 2

        elif ship == "compSub" or ship == "compCru":
            shipSquareWidth = 3

        elif ship == "compBat":
            shipSquareWidth = 4

        elif ship == "compCar":
            shipSquareWidth = 5


        while True:
            try:
                # Empties the key 
                # (had to implement it because if the starting square was in column J, you would get an index 
                # error during the looping process since there's no letter after J, causing it to pick another 
                # starting position. However, the J coordinate is already appended into the list, so this empties 
                # it, removing that J coordinate.)
                compShips[ship] = []

                # Chooses the coordinate of the most left square that the ship is occupying
                startingLetter = random.choice(letters)
                row = random.choice(numbers)

                # Returns the index position of the starting square's letter in the list "letters"
                startingIndexPos = letters.index(startingLetter)

                # Will loop the number of times equal to how many squares the iterated ship can 
                # horizontally occupy. Ex. the destroyer is 2 squares wide. Therefore, the for-loop will 
                # repeat twice so only 2 coordinates can be appended into the list in the destroyer key
                for i in range(shipSquareWidth):

                    # After each iteration, the starting index position increases by one, and this new index 
                    # position is then used to retrieve the consecutive letter(s) from the starting one. The
                    # new letter and the row are put together to make a new square coordinate that the 
                    # iterated ship is occupying (these squares are adjacent of each other)
                    newCoord = letters[startingIndexPos + i] + str(row)

                    if newCoord in coordsOccupied:
                        raise Exception

                    else: 
                        coordsOccupied.append(newCoord)

                        # The coordinate will be added into the list of the iterated key in the dictionary "compShips"
                        compShips[ship].append(newCoord)

        
                break    
            
            # (IndexError) E.g. when the starting square is in the J column. There's no column beyond J, 
            # so there'll be an index error.
            # (Exception) E.g. if the destroyer is already occupying G6 and H6, but during the making of 
            # the submarine coordinates, its starting square is E6. It will ultimately overlap with G6.
            except (IndexError, Exception):
                continue


# Determines if the user's guess is valid 
# (i.e. in the proper letter, number format and has not already been guessed)
def isGuessValid(guess):
    try:
        if len(guess) == 2:

            # Takes the character at index 0
            letter = guess[0]

            # Takes the character at index 1 and convert it into an integer
            number = int(guess[1])

            if letter in letters:
                if number in numbers:
                    if guess not in guessesMade:

                        # If the letter and number of the guess are possible letters and numbers 
                        # and if the guess has not been entered before
                        guessesMade.append(guess)
                        return True
    
        else:
            return False
    
    # Ex. if I entered "HI", this error will appear because "I" cannot be turned into an integer
    except ValueError:
        return False
    

# Determines if the user's guess is a hit or miss
def isUserGuessHit(guess):

    # Loops through all keys (ships) in the dictionary "compShips". Each key will do the following
    for ship in compShips:

        # Loops through all the elements (letter, number coordinates) in the list (the value of the key) 
        # in the iterated key
        for coord in compShips[ship]:

            # If the iterated coordinate matches with the guessed coordinate
            if guess == coord:
                
                # Removes that coordinate from the iterated key's list.
                # This is ultimately for checking sunken ships. If the list is empty, it will indicate that 
                # the ship has sunken.
                compShips[ship].remove(coord)
                
                return True
    
    return False


# Determines if the computer's guess is a hit or miss
def isCompGuessHit(guess):

    # Loops through all items (ships) in the list "ships" (user's ships). Each item will do the following
    for ship in ships:

        # Loops through all items (letter, number coordinates) in the iterated ship's list (contains 
        # the square coordinates its occupying)
        for coord in ship.posOnMap:

            # If the iterated coordinate matches with the guessed coordinate
            if guess == coord:

                # Removes that coordinate from the iterated ship's coordinate list.
                # This is ultimately for checking sunken ships. If the list is empty, it will indicate that 
                # the ship has sunken.
                ship.posOnMap.remove(coord)

                return True
            
    return False


# Randomizes a guess for the computer
def compTurn():
    
    # After 24 rounds, the computer's guesses will become more "intelligent"
    if len(guessesMade) >= 24:

        while True:

            # Chooses a random item in the list "ships" (user ships)
            ship = random.choice(ships)
            
            # If the ship has sunk, a new ship will be chosen (if a ship has sunken, "sunk" is appended 
            # to the ship's list)
            if "sunk" in ship.posOnMap:   
                continue
            
            # If the ship hasn't sunk, the while-loop will break
            else:
                break
                
        # Generates a random number between 1 and 100
        num = random.randint(1, 100)
                
        # If the randomized number is less or equal to 70, the following will happen
        # This means the computer will have a 70% to guess correctly
        if num <= 70:

            # Chooses one of the correct coordinates of the chosen ship as the computer's guess
            compGuess = random.choice(ship.posOnMap)

            # Adds the choosen coordinate into the guessesMadeComp list
            guessesMadeComp.append(compGuess)

            # Determines if the guess is a hit
            if isCompGuessHit(compGuess) == True:
                
                # The guess is saved into the user's hitTracker list
                # This allows a fire sprite to appear on the guessed coordinate
                userMap.hitTracker.append(compGuess)
                        
                # Return back to the startGame() function
                return

            # If the guess was a miss
            else:
                # The guess is saved into the computer's hitTracker list
                # This allows a white circle sprite to appear on the guessed coordinate
                userMap.missTracker.append(compGuess)
                    
                # Return back to the startGame() function
                return

    # The computer will guess random a coordinate if 24 rounds hasn't happened or the number was greater than 70
    while True:
        letter = random.choice(letters)
        number = random.choice(numbers)

        compGuess = letter + str(number)

        if compGuess not in guessesMadeComp:
            # If the guess hasn't been made, it will added to the guessesMadeComp list
            guessesMadeComp.append(compGuess)

            # If the computer's guess was a hit
            if isCompGuessHit(compGuess) == True:
                userMap.hitTracker.append(compGuess)
            
            # If the computer's guess was a miss
            else:
                userMap.missTracker.append(compGuess)

            # Return back to the startGame() function
            return


# Displays fire and white circle sprites on both maps to represent hits and misses, respectively
def displayHitAndMiss(map):
        
        # File paths of the hit and miss images
        imagePathHit = "C:/Users/Sarav/Downloads/eLearning Computer Science/Final Culminating/Images/fire.png"
        imagePathMiss = "C:/Users/Sarav/Downloads/eLearning Computer Science/Final Culminating/Images/white_circle.png"
        
        # Loops through all item in the user's or computer's hitTracker list. Each item will do the following:
        for square in map.hitTracker:

            # Loads the fire image
            image = pygame.image.load(imagePathHit)

            # Rescales the fire image so it's 40 x 40 pixels
            image = pygame.transform.scale(image, (40, 40))

            # Creates a rectangle for the fire image
            rect = image.get_rect()

            # Sets the x, y coordinate of the rectangle (fire image) to the x, y coordinate (top-left corner)
            # of the iterated item (letter, number coordinate).
            # squareCoords is a dictionary that holds every letter, number coordinate as keys. The value
            # associated with each key is its top-left x, y coordinate. squareCoords is attributed to both 
            # maps.
            rect.x = map.squareCoords[square][0]
            rect.y = map.squareCoords[square][1]

            # Displays the fire image at the specified position of the rectangle
            screen.blit(image, rect)
        
        # Loops through all item in the user's or computer's missTracker list. Each item will do the following:
        for square in map.missTracker:

            # Loads the white circle image
            image = pygame.image.load(imagePathMiss)

            # Rescales the white circle image to 40 x 40 pixels
            image = pygame.transform.scale(image, (40, 40))
            rect = image.get_rect()
            
            # Sets the x, y coordinate of the rectangle (white circle image) to the x, y coordinate 
            # (top-left corner) of the iterated square (letter, number coordinate).
            rect.x = map.squareCoords[square][0]
            rect.y = map.squareCoords[square][1]
        
            screen.blit(image, rect)


# Checks if any ships have sunken, updates "userShipsLeft" and "compShipsLeft" accordingly
def checkSunkenShip(userShipsLeft, compShipsLeft):
    userRemaining = userShipsLeft
    compRemaining = compShipsLeft 

    # Iterates through all items in the list "ships" (user's ships)
    for ship in ships:

        # If the list of the iterated ship contain no coordinates 
        if len(ship.posOnMap) == 0:

            # The string "sunk" gets added to the list. This prevents the sunken ship to go through 
            # this if-block again since it will have 1 item in its list.
            ship.posOnMap.append("sunk")

            userRemaining -= 1

    # Iterates through all keys in the dictionary "compShips"
    for ship in compShips:

        # If the list in iterated key in compShips is empty
        if len(compShips[ship]) == 0:
            compShips[ship].append("sunk")
            compRemaining -= 1

    # Returns the values of userRemaining and compRemaining
    return userRemaining, compRemaining


# Main game function, handling turns
def startGame():

    # Allows modifications of the following variables within this function
    global turn, isFirstTurnOver, userShipsLeft, compShipsLeft
    
        
    if turn == "user":

        # If the user clicked the text box (typing is True), the text box border will turn green.
        if typing == True:
            pygame.draw.rect(screen, (126, 217, 87), textBox, 4)
        
        # Otherwise, the text box border will remain red.
        else: 
            pygame.draw.rect(screen, (255, 70, 70), textBox, 4)


        # Displays the current text entered by the user in the text box
        displayText(userGuess, textFont, BLACK, 400, 505)

        # Displays general text
        displayText("Coordinate:", textFont, BLACK, 140, 505)


        # If it's the first turn, display general instructions
        if isFirstTurnOver == False:
            displayText("Your turn! Please enter a coordinate before pressing attack! e.g A4, B7", textFontSmall, BLACK, 5, 575)
        
        # After the first turn, the program will display the status of the previous attack (i.e. hit or miss)
        else:
            displayText(f"Last attack was a {status}! Try attacking again!", textFontSmall, BLACK, 5, 575)
        

        # If the user's input is invalid, display an error message
        if validGuess == False:
            displayText("Invalid coordinate! Please try again!", textFontSmall, BLACK, 700, 515)
        

        # If the mouse is hovering over the attack button, the button "lights" up
        if (attackButton.x <= mouseX <= attackButton.x + 180) and (attackButton.y <= mouseY <= attackButton.y + 50):
           pygame.draw.rect(screen, (174, 242, 145), attackButton)
        else:
            pygame.draw.rect(screen, (126, 217, 87), attackButton)
        
        # The label for the attack button
        displayText("ATTACK", textFontBold, BLACK, 517, 500)     


    elif turn == "computer":
        
        # Initiates the computer's turn
        compTurn()

        # Checks if any ships have sunken, updates the variables "userShipsLeft" and "compShipsLeft" accordingly
        userShipsLeft, compShipsLeft = checkSunkenShip(userShipsLeft, compShipsLeft)
        
        turn = "user"

        isFirstTurnOver = True
    

# Displays the appropriate ending screen (win, tie, or lose)
def endingScreen(imagePath, text, x, y):
    
    # Loads the image corresponding to the ending (images are pre-cropped to be 800 x 600 pixels)
    image = pygame.image.load(imagePath)
    
    # Creates a rectangle for the image
    rect = image.get_rect()

    # Sets the x, y coordinate (top-left corner) of the rectangle (image)
    rect.x = 0
    rect.y = 0
    
    # Displays the image at the specified position of the rectangle
    screen.blit(image, rect)

    # Draws a dark blue background next to the image
    pygame.draw.rect(screen, (19, 49, 84), (800, 0, 400, 600))

    # Displays general ending text (e.g. "YOU WON!", "YOU LOST!", etc.)
    displayText(text, textFontBigBold, WHITE, x, y)
    displayText("Rerun the progam", textFont, WHITE, 855, 250)
    displayText("to play again!", textFont, WHITE, 890, 290)




# Colours
WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

BACKGROUND = (241, 235, 228)

# Possible letters and numbers to guess from
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


# Pygame set up
pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('Battleship')
clock = pygame.time.Clock()

# Fonts
textFontBigBold = pygame.font.SysFont("Times New Roman", 60, bold = True)
textFont = pygame.font.SysFont("Times New Roman", 40)
textFontMid = pygame.font.SysFont("Times New Roman", 30)
textFontSmall = pygame.font.SysFont("Times New Roman", 20)
textFontBold = pygame.font.SysFont("Times New Roman", 40, bold = True)

# Create Ship objects for different types of ships with their image paths, starting position, and dimensions
# The destroyer (2 squares wide; each square is 40 pixels)
shipDes = Ship("C:/Users/SaraV/Downloads/eLearning Computer Science/Final Culminating/Images/destroyer.png", 240, 550, 80, 40)

# The submarine (3 squares wide)
shipSub = Ship("C:/Users/Sarav/Downloads/eLearning Computer Science/Final Culminating/Images/submarine.png", 330, 550, 120, 40)

# The crusier (3 squares wide)
shipCru = Ship("C:/Users/SaraV/Downloads/eLearning Computer Science/Final Culminating/Images/cruiser.png", 110, 550, 120, 40)

# The battleship (4 squares wide)
shipBat = Ship("C:/Users/SaraV/Downloads/eLearning Computer Science/Final Culminating/Images/battleship.png", 100, 500, 160, 40)

# The carrier (5 squares wide)
shipCar = Ship("C:/Users/Sarav/Downloads/eLearning Computer Science/Final Culminating/Images/cruiser.png", 270, 500, 200, 40)

# List of all the Ship objects
ships = [shipDes, shipSub, shipCru, shipBat, shipCar]

# Create Map objects for the user and computer with specified screen positions (x, y)
userMap = Map(100, 50)
compMap = Map(700, 50)

# Not the exact correct measurements of the map, but the extra margin is for flexibility when 
# placing the ships on the map
userMapCoor = pygame.Rect(100, 50, 410, 410)

# Initialized button dimensions
quitButton = pygame.Rect(1080, 550, 120, 50)
startButton = pygame.Rect(535, 500, 140, 50)
attackButton = pygame.Rect(510, 500, 180, 50)

# Variable that keeps track if a ship is being dragged
activeShip = None

# Variable that keeps track if all ships are placed within the user's map
allShipsPlaced = True


# Game status variables
gameOn = False
isFirstTurnOver = False # This variable allows a different text to be displayed after the first turn
ending = False


# This variable allows an error message to be displayed if an invalid coordinate was guessed
validGuess = True


# User input gets stored in this variable
userGuess = ""

# Keeps track if the user is typing (i.e if the user clicked on the text box)
typing = False

# Initializes the text box dimensions
textBox = pygame.Rect(340, 500, 160, 50)


# Lists that store the coordinates guessed. Prevents repeated coordinates
guessesMade = []
guessesMadeComp = []

# Variables that keep track of how many ships are left for the user and computer
userShipsLeft = 5
compShipsLeft = 5

# Keeps track of whose turn it is
turn = "user"


while True:
    clock.tick(30)

    # Event handling
    for event in pygame.event.get():

        # If the user clicks the top right exit button, program will end
        if event.type == QUIT:
            pygame.quit() # Exits the program gracefully without freezing
            sys.exit()

        # If the user mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            # Checks if it's a left mouse button click
            if event.button == 1:

                # Loops through all items in the list "ships", but it also takes the index 
                # position of the iterated item and stores it in the variable "num"
                for num, ship in enumerate(ships):
                    
                    # If the user mouse left clicked ontop of a ship and the game has not started
                    if ship.rect.collidepoint(pygame.mouse.get_pos()) and gameOn == False:
                        
                        # "activeShip" becomes the index position number of the iterated item
                        activeShip = num

                        # Saves the current position (x, y) of the clicked ship
                        initialPosX = ship.rect.x
                        initialPosY = ship.rect.y

                
                if gameOn == False:

                    #If the user mouse left clicked ontop of the start button
                    if startButton.collidepoint(pygame.mouse.get_pos()):
                    
                        # Reinitalizes the variable as True
                        allShipsPlaced = True

                        # Loops through all of the items in the list "ships" (user ships)
                        for ship in ships:

                            # If the iterated ship is not within the user's map
                            if ship.isWithinBounds(userMapCoor) == False:
                                allShipsPlaced = False

                                break

                        if allShipsPlaced == True:
                            # If all ships are within the grid, the game will start
                            gameOn = True

                            # Initalizes the dictionary that stores all of the computer's ship locations 
                            # in a list (the value of the key) in the according key 
                            compShips = {
                                "compDes": [], 
                                "compSub": [],
                                "compCru": [],
                                "compBat": [],
                                "compCar": [],
                            }

                            # Generates random ship locations for the computer
                            compCoords()

                            # Outputs all of the computer ship's coordinates if the user wants an easy win
                            print(compShips)
                

                if gameOn == True and ending == False:

                    # If the user mouse left clicked on the text box
                    if textBox.collidepoint(pygame.mouse.get_pos()):
                        typing = True # Becomes True

                
                    if typing == True:

                        # If the user left clicked on the attack button
                        if attackButton.collidepoint(pygame.mouse.get_pos()):
                            validGuess = True

                            # If the user's guess is valid
                            if isGuessValid(userGuess) == True:

                                # After figuring out the guess is valid, checks if it's a hit or miss
                                if isUserGuessHit(userGuess) == True:
                                    
                                    # The guess is saved into the computer's hitTracker list
                                    # This allows a fire sprite to appear on the guessed coordinate
                                    compMap.hitTracker.append(userGuess)
                                    
                                    # This variable keeps track whether the user's last attack was a hit or miss
                                    # It ultimately gets displayed on screen
                                    status = "hit"
                                
                                # If isUserGuessHit(userGuess) == False (the user's guess is a miss)
                                else:

                                    # The guess is saved into the computer's missTracker list
                                    # This allows a white circle sprite to appear on the guessed coordinate
                                    compMap.missTracker.append(userGuess)
                                    
                                    status = "miss"

                                # Resets the text in the input box
                                userGuess = ""

                                # Switches to the computer's turn
                                turn = "computer"
                            

                            # If isGuessValid(userGuess) == False:
                            else:
                                validGuess = False
                                
                                # Resets the text in the input box
                                userGuess = ""
                            
                            # Resets typing to False so that the user has to click on the text box again to type
                            typing = False
                

                # If the game has not ended 
                if ending == False:

                    # If the user left clicked on the quit button
                    if quitButton.collidepoint(pygame.mouse.get_pos()):
                        print("Boooooo...")
                        pygame.quit()
                        sys.exit()

                # If the game has ended; somebody won
                if ending == True:

                    # If the user left clicked on the quit button
                    if quitButton.collidepoint(pygame.mouse.get_pos()):
                        print("Thank you for playing :)")
                        pygame.quit()
                        sys.exit()
                    
        # If the mouse moved
        elif event.type == pygame.MOUSEMOTION:

            # If there is an active ship (as a result of left clicking on a ship)
            # and the game has not started
            if activeShip != None and gameOn == False:

                # The ship at index "activeShip" will get moved relative to the mouse's movement.
                # The "event.rel" contains the relative movement of the mouse (the change of x and y 
                # since the last event). The move_ip() function takes these changes of x and y 
                # to update the position of ship's rectangle. In turn, the "activeShip" moves correspondingly 
                # to the mouse's movements
                ships[activeShip].rect.move_ip(event.rel)
        
        # If the user releases their mouse click
        elif event.type == pygame.MOUSEBUTTONUP:

            # Checks if the action was from the left mouse button
            if event.button == 1:

                # If there is an active ship (as a result of left clicking on a ship)
                # and the game has not started
                if activeShip != None and gameOn == False:

                    # If the "activeShip" is placed outside of the user's map
                    if ships[activeShip].isWithinBounds(userMapCoor) == False:
                        
                        # The activeShip's x, y coordinates will be reset to its initial position values 
                        # before the move
                        ships[activeShip].rect.x = initialPosX
                        ships[activeShip].rect.y = initialPosY
                    
                    # If the "activeShip" is within the user's map
                    else:
                        # Calls on placementCorrection(), passing the ship's current x, y values (top left coords)
                        # This ultimately "snaps" the ship onto the map to the closest square. 
                        newPosX, newPosY, startingSquare = placementCorrection(ships[activeShip].rect.x, ships[activeShip].rect.y)
                       
                        # The newPosX and newPosY would be the closest square's top left x, y values, which become
                        # the ship's new top left x, y values
                        ships[activeShip].rect.x = newPosX
                        ships[activeShip].rect.y = newPosY

                        # If the "activeShip" is overlapping with another ship
                        if ships[activeShip].isOverlapping() == True:

                            # The activeShip's x, y coordinates will be reset to its initial position values 
                            # before the move
                            ships[activeShip].rect.x = initialPosX
                            ships[activeShip].rect.y = initialPosY    

                        # If the "activeShip" is not overlapping with another ship
                        else:
                            # Passing the most left square that the ship is occupying, putInList()
                            # will ultimatley store the letter, number coordinates of the ship.
                            ships[activeShip].putInList(startingSquare)

                    # Setting activeShip back to none allows the current active ship to be dropped 
                    # and user to move a different ship
                    activeShip = None

        # If a keyboard key was pressed
        elif event.type == pygame.KEYDOWN:
            if typing == True:

                # If the keystroke was from the backspace key
                if event.key == pygame.K_BACKSPACE:

                    # Removes the last character. 
                    # The slicing causes userGuess to equal the characters from index 0 to index -1 
                    # (the last character), but excludes the character at index -1
                    userGuess = userGuess[:-1]

                else:
                    # Updates the string with the characters from the keystrokes. Capitalizes any lowercase letters
                    userGuess += event.unicode.upper()


    screen.fill(BACKGROUND)

    # Displays general labels and text for the game
    displayText("Your Map", textFontMid, BLACK, 100, 450)
    displayText("Ships Left:", textFontMid, BLACK, 340, 450)
    displayText("Enemy Map", textFontMid, BLACK, 700, 450)
    displayText("Ships Left:", textFontMid, BLACK, 940, 450) 
    labellingMap(userMap.rect.x, userMap.rect.y)
    labellingMap(compMap.rect.x, compMap.rect.y)

    # Displays map backgrounds and grid lines on the game screen
    screen.blit(userMap.image, userMap.rect)
    screen.blit(compMap.image, compMap.rect)
    userMap.drawLine(screen, userMap.rect.x, userMap.rect.y)
    compMap.drawLine(screen, compMap.rect.x, compMap.rect.y)

    # Displays ship sprites
    for ship in ships:
        screen.blit(ship.image, ship.rect)

    # Gets mouse x, y coords
    mouseX, mouseY = pygame.mouse.get_pos()

    # If the mouse is hovering over the quit button, the button "lights" up
    if (quitButton.x <= mouseX <= quitButton.x + 120) and (quitButton.y <= mouseY <= quitButton.y + 50):
        pygame.draw.rect(screen, (252, 130, 130), quitButton)
    else:
        # (255, 70, 70) is a darker shade of red
        pygame.draw.rect(screen, (255, 70, 70), quitButton)

    displayText("QUIT", textFontBold, BLACK, 1090, 555)    


    if gameOn == False:
        # If the mouse is hovering over the start button, the button "lights" up
        if (startButton.x <= mouseX <= startButton.x + 140) and (startButton.y <= mouseY <= startButton.y + 50):
            pygame.draw.rect(screen, (174, 242, 145), startButton)
        else:
            # (126, 217, 87) is a darker shade of green
            pygame.draw.rect(screen, (126, 217, 87), startButton)
            
        displayText("START", textFontBold, BLACK, 540, 500)

        # If all five ships aren't placed on user's map, a friendly message will be displayed
        if allShipsPlaced == False:
            displayText("ERROR! Please place all five ships within your map before pressing start!", textFontSmall, BLACK, 460, 570)
        

    # If gameOn == True
    else:
        if userShipsLeft > 0 and compShipsLeft > 0:
            # Displays the current scores
            displayText(str(userShipsLeft), textFontMid, BLACK, 480, 450)
            displayText(str(compShipsLeft), textFontMid, BLACK, 1080, 450)
            
            startGame()
            
            # Displays the white circle and fire sprites
            displayHitAndMiss(compMap)
            displayHitAndMiss(userMap)

        else:
            ending = True

            # If the user and computer tie. 
            # Since the user goes first, it's only fair to let the computer have one more turn, which can lead to a tie
            if userShipsLeft == 0 and compShipsLeft == 0:
                endingScreen("C:/Users/SaraV/Downloads/eLearning Computer Science/Final Culminating/Images/tie.png", "YOU TIED!", 840, 180)

            # If the computer wins
            elif userShipsLeft == 0:
                endingScreen("C:/Users/SaraV/Downloads/eLearning Computer Science/Final Culminating/Images/lose.jpg", "YOU LOST!", 835, 180)

            # If the user wins
            elif compShipsLeft == 0:
                endingScreen("C:/Users/SaraV/Downloads/eLearning Computer Science/Final Culminating/Images/win.jpg", "YOU WON!", 840, 180)
            
            # Reinitalizes the quit button dimensions
            quitButton = pygame.Rect(925, 360, 150, 60)

            # If the mouse is hovering over the quit button, the button "lights" up
            if (quitButton.x <= mouseX <= quitButton.x + 120) and (quitButton.y <= mouseY <= quitButton.y + 50):
                pygame.draw.rect(screen, (252, 130, 130), quitButton)
            else:
                pygame.draw.rect(screen, (255, 70, 70), quitButton)
            
            displayText("QUIT", textFontBold, BLACK, 950, 365)

    pygame.display.flip()