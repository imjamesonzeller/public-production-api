import math
import random
import string

class PlacementInformation():
    def __init__(self, word, coords, direction):
        self.word = word
        self.coords = coords
        self.direction = direction

class WordSearch():
    def __init__(self, words) -> None:
        self.words = words
        self.words_copy = words.copy()
        self.size = self.__computeGridSize()
        self.grid = [ [ "_" for i in range(self.size) ] for i in range(self.size) ]
        self.directions = [{"x_step": 0, "y_step": 1}, {"x_step": 1, "y_step": 0}, {"x_step": 1, "y_step": 1}, {"x_step": 1, "y_step": -1},
                           {"x_step": 0, "y_step": -1}, {"x_step": -1, "y_step": 0}, {"x_step": -1, "y_step": -1}, {"x_step": -1, "y_step": 1}]

    def __computeGridSize(self) -> int:
        total_characters = sum(len(word) for word in self.words)
        average_word_length = total_characters // len(self.words)
        max_word_length = max(len(word) for word in self.words)
        
        # Calculate initial grid size based on number of words and average word length
        grid_size = math.ceil(math.sqrt(len(self.words) * average_word_length))
        
        grid_size = max(grid_size, max_word_length)
        
        grid_size *= 2
        return grid_size

    def __getRandomCoords(self) -> tuple[int, int]:
        return (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
    
    def __getValidDirection(self, word, coords) -> dict | None:
        # Okay this function is cooked as fuck... The point of this function is to take a word and coordinates and find a valid direction for the word to be place into the grid
        # This function becomes fucked when you realize there may not be a valid direction. If there is not a valid direction it returns None, but if there is, it returns the direction
        # I handle the return of None in the generate_word_search function by continuing which gets new random starting coords for the word
        # The reason I don't initially check if there is a valid direction in a different function is because doing it this way allows for only one iteration through self.directions
        # If I for say had a does_valid_direction_exist function, I would iterate through and return true or false and if true I would iterate through again in this function to return it
        # It is more likely a valid direction exists than doesn't so it is a little better time complexity wise (Well not time complexity but real world run time lol...)
        # If you read this and you know how I could possibly refractor this so that the return isn't sometimes None, please reach out (jz@jamesonzeller.com)

        x_pos, y_pos = coords
        random.shuffle(self.directions)
        valid_direction = True
        for direction in self.directions:
            for i in range(len(word)):
                y_offset = i * direction["y_step"]
                x_offset = i * direction["x_step"]
                
                curr_y = y_pos + y_offset
                curr_x = x_pos + x_offset

                try: 
                    if (curr_x) < 0 or (curr_y) < 0:
                        valid_direction = False
                        break
                    # Checks if current location for word is blank or matches current character, if neither of those apply then direction is invalid.
                    if self.grid[curr_y][curr_x] != "_" and self.grid[curr_y][curr_x] != word[i]:
                        valid_direction = False
                        break
                except IndexError:
                    valid_direction = False
                    break

            if valid_direction:
                return direction
        return None

    def __placeWord(self, placement_info) -> None:
        x_pos, y_pos = placement_info.coords
        direction = placement_info.direction
        word = placement_info.word

        for i in range(len(word)):
            y_offset = i * direction["y_step"]
            x_offset = i * direction["x_step"]
            
            curr_y = y_pos + y_offset
            curr_x = x_pos + x_offset

            self.grid[curr_y][curr_x] = word[i]

    def __fillBlanksIn(self) -> None:
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == "_":
                    self.grid[row][col] = random.choice(string.ascii_uppercase)
    
    def generateWordSearch(self) -> list[list[chr]]:
        while len(self.words) != 0:
            # Get random coords, current word, and random direction
            coords = self.__getRandomCoords()
            word = self.words[0].upper()

            # getValidDirection returns None if there is not a valid direction for that word at that coordinate
            # So, on the next line, if not direction then we continue and we get new random coordinates and try again to get a valid direction for it
            # This will continue until the word has a valid direciton and coordinate combo when it will then pass on and be placed in the grid
            # I really wish that this 'looping' till we find a valid direction was not handled in the generateWordSearch function but changing this would require full logic rework.
            direction = self.__getValidDirection(word, coords)
            if not direction:
                continue

            # Place word on board and remove from working words list
            placement_info = PlacementInformation(word, coords, direction)
            self.__placeWord(placement_info)

            self.words.pop(0)

        # After all words are inserted, fill in blanks with random characters
        self.__fillBlanksIn()
        return self.grid