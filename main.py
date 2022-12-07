# assets
# https://opengameart.org/content/sea-warfare-set-ships-and-more

import pygame, os, sys
from button import Button
from grid import Grid
from pathlib import Path
from ship import Ship
from shoot import Shoot
from text import Text
from constants import *
from pygame.locals import *
from enemyAI import EnemyAi

SIZESCREEN = WIDTH, HEIGHT
os.environ["SDL_VIDEO_CENTERED"] = '1'

pygame.init()
pygame.display.set_caption("Battleship")


screen = pygame.display.set_mode(SIZESCREEN)


class Game:
    def __init__(self):
        self.player_grid = Grid(80, 120)
        self.player_grid.create_cells()
        self.enemyAI = EnemyAi()
        self.enemyAI.grid.create_cells()
        self.ship_list = pygame.sprite.Group()
        self.create_ships()
        self.button_list = pygame.sprite.Group()
        self.button_list.add(Button("rotate", Path(r"./images/Rotate_button.png"), 520, 380))
        self.button_list.add(Button("lock-in", Path(r"./images/lock-in_button.png"), 520, 470))
        self.shoot_list = pygame.sprite.Group()

    def refresh_screen(self):
        screen.fill((60,70,80))
        screen.blit(self.player_grid.surface, self.player_grid.rect)
        screen.blit(self.enemyAI.grid.surface, self.enemyAI.grid.rect)
        self.display_info()
        self.button_list.update()
        self.button_list.draw(screen)
        self.ship_list.update()
        self.ship_list.draw(screen)
        self.shoot_list.update()
        self.shoot_list.draw(screen)

        pygame.display.update()

    @staticmethod
    def display_info():
        title_text = Text("STATKI",WHITE,screen.get_rect().centerx,35)
        player_text = Text("Plansza Gracza", WHITE, 240, 80, size=50)
        enemy_text = Text("Plansza przeciwnika", WHITE, 920, 80, size=50 )

        title_text.draw(screen)
        player_text.draw(screen)
        enemy_text.draw(screen)

    def create_ships(self):
        # Creates ships and sets them between grids one below the other
        ship_y = 120
        ship_x = 500
        for ship in SHIPS:
            path = Path(SHIPS[ship][1])
            name = ship
            length = SHIPS[ship][0]
            self.ship_list.add(Ship(name, length, path, ship_x, ship_y))
            ship_y += 40
        self.ship_list.draw(screen)

    def set_up_player_ships(self):
        """Loop in which the player places ships on the grid"""
        setting_up = True
        selected = None
        while setting_up:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if selected is None:  # The first click selects the ship and starts dragging
                        for i, ship in enumerate(self.ship_list):
                            if ship.rect.collidepoint(event.pos):
                                selected = i
                                shipmove_x = ship.rect.x - event.pos[0]
                                shipmove_y = ship.rect.y - event.pos[1]
                        for button in self.button_list.sprites():
                            if button.rect.collidepoint(event.pos):
                                if button.name == "lock-in":
                                    setting_up = self.lock_in_ships(setting_up)
                                    # print(setting_up)
                    else:
                        for button in self.button_list.sprites():
                            if button.rect.collidepoint(event.pos):
                                if button.name == "rotate":
                                    ships = self.ship_list.sprites()
                                    ships[selected].rotate(event.pos[0], event.pos[1])
                                    break # otherwise "selected" will set to None
                            else:
                                selected = None  # Pressing the mouse button a second time lets go of the ship
                elif event.type == pygame.MOUSEMOTION:
                    if selected is not None:
                        ships = self.ship_list.sprites()
                        ships[selected].rect.x = event.pos[0] + shipmove_x
                        ships[selected].rect.y = event.pos[1] + shipmove_y

            self.refresh_screen()

    def lock_in_ships(self, setting_up):
        """Locks the ships on the grid, centering them in the cell.
        Calls the "update_cells_with_ship" method from the grid class to update the cells"""
        for ship in self.ship_list.sprites():
            if ship.horizontal:
                cell_details = self.player_grid.check_ship(ship.rect.midleft, True)
                # print(self.player_grid.check_ship(ship.rect.midleft, True))
                if cell_details:
                    ship.rect.midleft = cell_details[0]
                    # Update all cells in which the ship is located
                    self.player_grid.update_cells_with_ship(starting_x=cell_details[1],
                                                    starting_y=cell_details[2],
                                                    ship_name=ship.name,
                                                    length=ship.length,
                                                    horizontal=True)
            else:
                cell_details = self.player_grid.check_ship(ship.rect.midtop, False)
                if cell_details:
                    ship.rect.midtop = cell_details[0]
                    # print(cell_details[2])
                    self.player_grid.update_cells_with_ship(starting_x=cell_details[1],
                                                    starting_y=cell_details[2],
                                                    ship_name=ship.name,
                                                    length=ship.length,
                                                    horizontal=False)

        # Count the number of cells in which the ships are located and compare with the value of how many cells should be occupied
        # This will ensure that the ships will not be able to continue the game if the stakti overlap
        ship_cell_total = len([cell.ship for cell in self.player_grid.cells if cell.ship is not None])
        ship_dict_total = sum([ship[0] for ship in SHIPS.values()])
        print(f"{ship_dict_total}====={ship_cell_total}")

        # End of ship placement if ships do not overlap and are on the grid
        if ship_cell_total == ship_dict_total:
            setting_up = False
        else:
            # Remove the "ship" attribute from all cells
            for cell in self.player_grid.cells:
                cell.ship = None
        return setting_up

    def check_for_win(self, grid):
        for cell in grid.cells:
            if cell.ship is not None:
                return False
        return True

    def game_over(self, win):
        screen.fill((60,70,80))
        if win:
            game_over_text = Text("Wygarna!", WHITE,screen.get_rect().centerx,200)
        else:
            game_over_text = Text("Porażka!", WHITE,screen.get_rect().centerx,200)

        play_again_text = Text("Jeszcze raz?", WHITE, screen.get_rect().centerx,300)
        yes_text = Text("Tak",WHITE,320,400)
        no_text = Text("Nie",WHITE,930,400)
        game_over_text.draw(screen)
        play_again_text.draw(screen)
        yes_text.draw(screen)
        no_text.draw(screen)
        pygame.display.update()
        pygame.time.wait(1000)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.pos[0] > screen.get_width()/2:
                        pygame.quit()
                        sys.exit()
                    else:
                        return True

    def enemy_cell_clicked(self):
        # marking a cell to attack on an enemy board
        x,y = pygame.mouse.get_pos()
        cell = self.enemyAI.grid.get_cell(x,y) # select cell
        # checking if the cell has been clicked before
        if not cell.is_clicked:
            cell_rect_center, cell_ship = cell.cell_clicked()
            if cell_ship:
                self.shoot_list.add(Shoot(Path(r"./images/hit.png"), cell_rect_center))
                for ship in self.enemyAI.ships:
                    if ship.name == cell.ship:
                        cell.ship = None
                        ship.length -= 1
                        if ship.length == 0: # ship destroyed
                            if self.check_for_win(self.enemyAI.grid): # check if win
                                self.refresh_screen()
                                pygame.time.wait(500)
                                if self.game_over(True): # player won
                                    self.ship_list.empty()
                                    self.shoot_list.empty()
                                    run()
            else:
                self.shoot_list.add(Shoot(Path(r"./images/miss.png"), cell_rect_center))
            self.refresh_screen()
            pygame.time.wait(200)

            enemy_hit = self.enemyAI.enemy_turn()
            cell = self.player_grid.return_cell(enemy_hit)
            cell_rect_center, cell_ship = cell.cell_clicked()
            if cell_ship:  # The name of the ship will be returned if it is hit
                self.shoot_list.add(Shoot(Path(r"./images/hit.png"), cell_rect_center))
                if not self.enemyAI.ship_hit:
                    self.enemyAI.ship_hit = enemy_hit
                elif self.enemyAI.ship_hit :
                    self.enemyAI.second_hit = enemy_hit
                # print(type(self.enemyAI.second_hit))
                for ship in self.ship_list:
                    if ship.name == cell.ship:

                        cell.ship = None
                        ship.length -= 1
                        if ship.length == 0: # ship destroyed
                            self.enemyAI.reset_hit_logs()
                            if self.check_for_win(self.player_grid): # check if win
                                self.refresh_screen()
                                pygame.time.wait(500)
                                if self.game_over(False): # enemy won
                                    self.ship_list.empty()
                                    self.shoot_list.empty()
                                    run()
            else:
                self.shoot_list.add(Shoot(Path(r"./images/miss.png"),cell_rect_center))
                # print(not self.enemyAI.tested_no_hit)
                if self.enemyAI.ship_hit and self.enemyAI.second_hit:
                    if not self.enemyAI.tested_no_hit:
                        # Record a miss if there were two hits beforehand
                        self.enemyAI.tested_no_hit = enemy_hit
                    else:
                        # If another miss, it means that the AI is not tracking the ship correctly (e.g., two ships next to each other)
                        #  Set "tested_no_hit" to get out of the recursion and avoid looping
                        self.enemyAI.tested_no_hit_2 = enemy_hit

            self.refresh_screen()
            # print(enemy_hit)

    def main(self):
        window_open = True
        clock = pygame.time.Clock()
        self.player_grid.draw_grid()
        self.enemyAI.grid.draw_grid()
        self.enemyAI.randomize_ships()

        self.set_up_player_ships()
        self.button_list.empty()

        self.refresh_screen()
        while window_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    window_open = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        window_open = False
                elif event.type == MOUSEBUTTONDOWN:
                    if self.enemyAI.grid.rect.collidepoint(event.pos):
                        self.enemy_cell_clicked()
                else:
                    pygame.display.update()
            self.refresh_screen()
            clock.tick(30)
        pygame.quit()

class Menu:
    def __init__(self):
        self.buttons = pygame.sprite.Group()
        self.buttons.add(Button("start", Path(r"./images/start_btn.png"), 310, screen.get_rect().centery))
        self.buttons.add(Button("exit", Path(r"./images/exit_btn.png"), 660, screen.get_rect().centery))


    def draw(self):
        screen.fill((60, 70, 80))
        title_text = Text("STATKI", WHITE, screen.get_rect().centerx, 35)
        menu_text = Text("MENU GŁÓWNE", WHITE, screen.get_rect().centerx, 200)
        self.buttons.draw(screen)
        title_text.draw(screen)
        menu_text.draw(screen)

    def get_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            for sprite in self.buttons.sprites():
                if sprite.rect.collidepoint(event.pos):
                    if sprite.name == "exit":
                        pygame.quit()
                        sys.exit()
                    else:
                        run()


def run():
    game = Game()
    game.main()

    
if __name__ == '__main__':
    menu = Menu()
    window_open = True
    while window_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window_open = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_open = False
            menu.get_event(event)
        menu.draw()
        pygame.display.update()

