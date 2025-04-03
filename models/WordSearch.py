import random
import math
import string
from models import PlacementInformation

class WordSearch():
    def __init__(self, _words: list[str]) -> None:
        self._words: list[str] = _words
        self._words_copy: list[str] = _words.copy()
        self._size: int = self._compute_grid_size()
        self._grid: list[list[str]] = [ [ "_" for i in range(self._size) ] for i in range(self._size) ]
        self._kDirections: list[dict[str, int]] = [{"x_step": 0, "y_step": 1}, {"x_step": 1, "y_step": 0}, {"x_step": 1, "y_step": 1}, {"x_step": 1, "y_step": -1},
                           {"x_step": 0, "y_step": -1}, {"x_step": -1, "y_step": 0}, {"x_step": -1, "y_step": -1}, {"x_step": -1, "y_step": 1}]

    @property
    def words(self) -> list[str]:
        return self._words_copy

    def _compute_grid_size(self) -> int:
        total_characters = sum(len(word) for word in self._words)
        average_word_length = total_characters // len(self._words)
        max_word_length = max(len(word) for word in self._words)
        
        # Calculate initial _grid _size based on number of _words and average word length
        grid_size = math.ceil(math.sqrt(len(self._words) * average_word_length))
        
        grid_size = max(grid_size, max_word_length)
        
        grid_size *= 2
        return grid_size

    def _get_random_coords(self) -> tuple[int, int]:
        return (random.randint(0, self._size - 1), random.randint(0, self._size - 1))
    
    def _get_valid_direction(self, word, coords) -> dict[str, int] | None:
        # Okay this function is cooked as fuck... The point of this function is to take a word and coordinates and find a valid direction for the word to be place into the _grid
        # This function becomes fucked when you realize there may not be a valid direction. If there is not a valid direction it returns None, but if there is, it returns the direction
        # I handle the return of None in the generate_word_search function by continuing which gets new random starting coords for the word
        # The reason I don't initially check if there is a valid direction in a different function is because doing it this way allows for only one iteration through self._kDirections
        # If I for say had a does_valid_direction_exist function, I would iterate through and return true or false and if true I would iterate through again in this function to return it
        # It is more likely a valid direction exists than doesn't so it is a little better time complexity wise (Well not time complexity but real world run time lol...)
        # If you read this and you know how I could possibly refractor this so that the return isn't sometimes None, please reach out (jz@jamesonzeller.com)

        x_pos, y_pos = coords
        random.shuffle(self._kDirections)
        valid_direction = True
        for direction in self._kDirections:
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
                    if self._grid[curr_y][curr_x] != "_" and self._grid[curr_y][curr_x] != word[i]:
                        valid_direction = False
                        break
                except IndexError:
                    valid_direction = False
                    break

            if valid_direction:
                return direction
        return None

    def _place_word(self, placement_info) -> None:
        x_pos, y_pos = placement_info.coords
        direction = placement_info.direction
        word = placement_info.word

        for i in range(len(word)):
            y_offset = i * direction["y_step"]
            x_offset = i * direction["x_step"]
            
            curr_y = y_pos + y_offset
            curr_x = x_pos + x_offset

            self._grid[curr_y][curr_x] = word[i]

    def _fill_blanks_in(self) -> None:
        for row in range(len(self._grid)):
            for col in range(len(self._grid[row])):
                if self._grid[row][col] == "_":
                    self._grid[row][col] = random.choice(string.ascii_uppercase)
    
    def generate_word_search(self) -> list[list[chr]]:
        while len(self._words) != 0:
            # Get random coords, current word, and random direction
            coords = self._get_random_coords()
            word = self._words[0].upper()

            # getValidDirection returns None if there is not a valid direction for that word at that coordinate
            # So, on the next line, if not direction then we continue and we get new random coordinates and try again to get a valid direction for it
            # This will continue until the word has a valid direciton and coordinate combo when it will then pass on and be placed in the _grid
            # I really wish that this 'looping' till we find a valid direction was not handled in the generate_word_search function but changing this would require full logic rework.
            direction = self._get_valid_direction(word, coords)
            if not direction:
                continue

            # Place word on board and remove from working _words list
            placement_info = PlacementInformation(word, coords, direction)
            self._place_word(placement_info)

            self._words.pop(0)

        # After all _words are inserted, fill in blanks with random characters
        self._fill_blanks_in()
        return self._grid