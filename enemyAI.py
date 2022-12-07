import itertools
from ship import Ship
from constants import *
from grid import Grid
import random


class EnemyAi:
    """class EnemyAI includes basic target selection logic
       if it hits a ship it will fire at the correct cells until the ship is sunk"""
    def __init__(self):
        self.grid = Grid(720, 120)
        self.ships = [Ship(ship, SHIPS[ship][0], SHIPS[ship][1]) for ship in SHIPS]
        self.ship_hit = None
        self.second_hit = None
        self.tested_no_hit = None
        self.tested_no_hit_2 = None
        self.available_cells = self.populate_available_cells()

    @staticmethod
    def populate_available_cells():
        """produces a list of tuples of coordinate pairs"""
        rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        grid = itertools.product(rows, columns)
        return [cell for cell in grid]

    def reset_hit_logs(self):
        """After sinking the ship sets the attributes that remember hits are set to None"""
        self.ship_hit = None
        self.second_hit = None
        self.tested_no_hit = None
        self.tested_no_hit_2 = None


    def randomize_ships(self):
        """Creates a list of coordinates reflecting the coordinates of a 10x10 grid,
         then adds ships to "self.grid", removing the used coordinates so they can't be reused"""
        rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ship_coord_mapping = {}
        grid = itertools.product(rows, columns)
        available_cells = [cell for cell in grid]
        for ship in self.ships:
            ship_coordinates = self.randomize_ship_coordinates(columns, rows, ship, available_cells)
            cells_minus_ship = [cell for cell in available_cells if cell not in ship_coordinates]
            ship_coord_mapping[ship.name] = ship_coordinates
            available_cells = cells_minus_ship
            self.grid.update_cells_with_ship(starting_x=ship.column,
                                             starting_y=ship.row,
                                             ship_name=ship.name,
                                             length=ship.length,
                                             horizontal=ship.horizontal)

    def randomize_ship_coordinates(self, columns, rows, ship, available_cells):
        """Creates a list of random ship coordinates for the "randomize_ships()" function,
           checks if all coordinate pairs are in "available_cells",
           if not then calls itself recursively until a valid coordinate list is created"""
        ship.horizontal = random.choice([True, False])
        ship_coordinates = []
        if ship.horizontal:
            ship.row = random.choice(rows)  # choose any y-coordinate
            available_columns = columns[:-ship.length]  # chooses only those x-coordinates that can include the ship
            ship.column = random.choice(available_columns)
            x = ship.column
            for _ in range(ship.length):
                ship_coordinates.append((x, ship.row))
                x += 1
        else:
            ship.column = random.choice(columns)
            available_rows = rows[:-ship.length]
            ship.row = random.choice(available_rows)
            y = ship.row
            for _ in range(ship.length):
                ship_coordinates.append((ship.column, y))
                y += 1
        if all(coord in available_cells for coord in ship_coordinates):
            return ship_coordinates
        else:
            # If any ship is in a cell already occupied call the function again
            return self.randomize_ship_coordinates(columns, rows, ship, available_cells)

    def random_pick(self):
        return random.choice(self.available_cells)

    def enemy_turn(self):
        # if no hits were recorded
        if not self.ship_hit:
            pick = self.random_pick()
        # After two misses where two hits were previously recorded
        elif self.tested_no_hit_2:
            self.second_hit = None
            self.tested_no_hit = None
            self.tested_no_hit_2 = None
            return self.pick_target_after_first_hit()
        # After the first hit, check the neighboring cells
        elif self.ship_hit and not self.second_hit:
            pick = self.pick_target_after_first_hit()
        # After second hit, shoot in line
        elif self.ship_hit and self.second_hit:
            pick = self.pick_target_after_second_hit(1)
        # If none of the above conditions are met, again select a random cell from the available cells
        else:
            pick = self.random_pick()
        self.available_cells.remove(pick)
        return pick

    def pick_target_after_first_hit(self):
        # Selects a random neighboring cell
        next_targets = [(self.ship_hit[0] + 1, self.ship_hit[1]),
                        (self.ship_hit[0] - 1, self.ship_hit[1]),
                        (self.ship_hit[0], self.ship_hit[1] + 1),
                        (self.ship_hit[0], self.ship_hit[1] - 1)]
        # compares the list of 4 targets to the available cells to ensure valid target returned
        next_targets_verified = [cell for cell in next_targets if cell in self.available_cells]
        pick = random.choice(next_targets_verified)
        return pick

    def pick_target_after_second_hit(self, check_distance):
        """If the opponent hits twice, it will check along the same axis as these hits,
           the checking distance is increased, and the method is called recursively in order to expand the search area"""
        if self.ship_hit[0] == self.second_hit[0]:  # Checking the same X axis coordinate
            next_targets = [(self.ship_hit[0], (max(self.ship_hit[1], self.second_hit[1]) + check_distance)),
                            (self.ship_hit[0], (min(self.ship_hit[1], self.second_hit[1]) - check_distance))]
            next_targets_verified = [cell for cell in next_targets if cell in self.available_cells]
            if next_targets_verified:
                return random.choice(next_targets_verified)
            else:
                # If there are no available targets set the "second_hit" attribute to None
                # and call the method responsible for the opponent's move again
                if self.tested_no_hit_2:
                    self.second_hit = None
                    return self.enemy_turn()
                # If it hits a second time it increases the checking distance by the next cell and calls the method again
                else:
                    check_distance += 1
                    return self.pick_target_after_second_hit(check_distance)
        else:  # Checking the same but for Y axis
            next_targets = [(max(self.ship_hit[0], self.second_hit[0] + check_distance), self.ship_hit[1]),
                            (min(self.ship_hit[0], self.second_hit[0] - check_distance), self.ship_hit[1])]
            next_targets_verified = [cell for cell in next_targets if cell in self.available_cells]
            if next_targets_verified:
                return random.choice(next_targets_verified)
            else:
                if self.tested_no_hit_2:
                    self.second_hit = None
                    return self.enemy_turn()
                else:
                    check_distance += 1
                    return self.pick_target_after_second_hit(check_distance)
