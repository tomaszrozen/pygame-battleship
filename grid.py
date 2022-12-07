
import pygame
from constants import *
from cell import Cell

class Grid:
    # Klasa kontener dla obiektów Cell (komórek), wykonuje sprawdzenia i aktualizaję komórek, rysuje siatkę na ekranie
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, GRID_SIZE, GRID_SIZE)
        self.surface = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.cells = []

    def draw_grid(self):
        self.surface.fill(BLUE)
        grid_x = 0
        grid_y = 0
        for _ in range(COLS + 1):
            pygame.draw.line(self.surface, WHITE, (grid_x, 0), (grid_x, GRID_SIZE), 4)
            pygame.draw.line(self.surface, WHITE, (0, grid_y), (GRID_SIZE, grid_y), 4)
            grid_x += CELL_SIZE
            grid_y += CELL_SIZE

    def create_cells(self):
        # Tworzy liste self.cells na podstawie wymiarów siatki
        cell_y = self.pos_y
        for col in range(ROWS):
            cell_x = self.pos_x
            for row in range(COLS):
                self.cells.append(Cell(x_coord=cell_x,
                                        y_coord=cell_y,
                                        row=row,
                                        column=col))

                cell_x += CELL_SIZE
            cell_y += CELL_SIZE
    
    def get_cell(self, x, y):
        # Zwraca pasujący komórkę, do współrzędnyh x,y pochodząych od kliknięcia myszki
        for cell in self.cells:
            if cell.x_coord <= x <= cell.x_coord + CELL_SIZE:
                if cell.y_coord <= y <= cell.y_coord + CELL_SIZE:
                    return cell

    def check_ship(self, ship_endpoint, horizontal):
        # Zwraca szczegóły komórki, której prostokąt (rect) koliduje z środkowym lewym punktem statku
        # przekazanym jako "ship_endpoint", argument "horizontal" służy do określenia czy metoda ma zwrócić
        # środkowy lewy punkt staku czy środkowy górny (wykorzystywane do wyrównania staku do środka komórki)
        for cell in self.cells:
            if cell.rect.collidepoint(ship_endpoint):
                if horizontal:
                    return cell.rect.midleft, cell.row, cell.column
                else:
                    return cell.rect.midtop, cell.row, cell.column
    
    def update_cells_with_ship(self, starting_x, starting_y, ship_name, length, horizontal):
        # aktualizuje atrybut "ship" komórki w której znajduje się statek o nazwę statku
        # wukorzystue koordynaty początku statku, długość i orientację aby zaktualizować odpowiednie komórki
        ship_coordinates = []
        for i in range(length):
            ship_coordinates.append((starting_x, starting_y))
            if horizontal:
                starting_x += 1
            else:
                starting_y += 1
        for cell in self.cells:
            cell_coordinates = (cell.row, cell.column)
            if cell_coordinates in ship_coordinates:
                cell.ship = ship_name

    def return_cell(self, coordinates):
        # Służy do zwracania obiektu wybranego przez AI
        for cell in self.cells:
            if cell.column == coordinates[0]:
                if cell.row == coordinates[1]:
                    return cell
