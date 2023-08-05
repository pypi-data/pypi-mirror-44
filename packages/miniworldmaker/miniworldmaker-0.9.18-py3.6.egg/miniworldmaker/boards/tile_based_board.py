from collections import defaultdict
from typing import Union
import pygame
from miniworldmaker.boards.board import Board
from miniworldmaker.tokens.token import Token

class TileBasedBoard(Board):

    def __init__(self, columns=20, rows=16, tile_size=20, tile_margin=0):
        super().__init__(columns=columns, rows=rows)
        self._tile_size = tile_size
        self._tile_margin = tile_margin
        self.set_size(self.tile_size, columns, rows, tile_margin)
        self._dynamic_actors_dict = defaultdict(list)  # the dict is regularly updated
        self._dynamic_actors = []  # List with all dynamic actors
        self._static_actors_dict = defaultdict(list)

    def _update_actors_positions(self) -> None:
        self._dynamic_actors_dict.clear()
        for actor in self._dynamic_actors:
            x, y = actor.position[0], actor.position[1]
            self._dynamic_actors_dict[(x, y)].append(actor)

    def get_colliding_tokens(self, actor: Token) -> list:
        self._update_actors_positions()
        colliding_actors = self.get_tokens_in_area(actor.rect)
        if actor in colliding_actors:
            colliding_actors.remove(actor)
        return colliding_actors

    def get_tokens_in_area(self, area: Union[pygame.Rect, tuple]) -> list:
        self._dynamic_actors_dict.clear()
        self._update_actors_positions()
        if type(area) == tuple:
            x, y = area[0], area[1]
        else:
            x, y = self.get_board_position_from_pixel(area.topleft)
        actors = []
        if self.is_on_board(self.rect):
            if self._dynamic_actors_dict[x, y]:
                actors.extend(self._dynamic_actors_dict[(x, y)])
            if self._static_actors_dict[x, y]:
                actors.extend(self._static_actors_dict[(x, y)])
        return actors

    def remove_from_board(self, token: Token) -> None:
        if token in self._dynamic_actors:
            self._dynamic_actors.remove(token)
        if token in self._static_actors_dict[(token.x, token.y)]:
            self._static_actors_dict[(token.x, token.y)].remove(token)
        super().remove_from_board(token)

    def remove_actors_from_cell(self, cell: tuple)->None:
        """
        Entfernt alle Actors aus einer Zelle
        Parameters
        ----------
        cell : Die Zelle aus der der Akteur entfernt werden soll.

        Returns
        -------

        """
        for actor in self._dynamic_actors_dict[cell[0], cell[1]]:
            self.remove_from_board(actor)
        for actor in self._static_actors_dict[cell[0], cell[1]]:
            self.remove_from_board(actor)

    def add_to_board(self, token: Token, position: tuple = None) -> Token:
        if token.is_static:
            self._static_actors_dict[(position[0], position[1])].append(token)
        else:
            self._dynamic_actors.append(token)
        super().add_to_board(token, position)
        if token.size == (0, 0):
            token.size = (self.tile_size, self.tile_size)
        token.changed()
        return token

    def update_actor(self, actor: Token, attribute, value):
        if attribute == "is_static" and value is True:
            self._static_actors_dict[(actor.x(), actor.y())].append(actor)
            if actor in self._dynamic_actors_dict:
                self._dynamic_actors_dict.pop(actor)
        else:
            self._dynamic_actors.append(actor)

    def is_empty_cell(self, position: tuple) -> bool:
        """
        Checks if cell is empty
        :param position: the position of the cell
        :return: True if cell is empty
        """
        if not self.get_tokens_in_area(position):
            return True
        else:
            return False

    @staticmethod
    def get_neighbour_cells(position: tuple) -> list:
        """
        Gets a list with all neighbour cells
        :param position: The position of the cell
        :return: the neighbour cells as list
        """
        cells = []
        y_pos = position[0]
        x_pos = position[1]
        cells.append([x_pos + 1, y_pos])
        cells.append([x_pos + 1, y_pos + 1])
        cells.append([x_pos, y_pos + 1])
        cells.append([x_pos - 1, y_pos + 1])
        cells.append([x_pos - 1, y_pos])
        cells.append([x_pos - 1, y_pos - 1])
        cells.append([x_pos, y_pos - 1])
        cells.append([x_pos + 1, y_pos - 1])
        return cells

    def is_on_board(self, area: Union[tuple, pygame.Rect]) -> bool:
        if type(area) == tuple:
            area = self.get_rect_from_board_position(area)
        x, y = self.get_board_position_from_pixel(area.center)
        if x > self.columns - 1:
            return False
        elif y > self.rows - 1:
            return False
        elif x < 0 or y < 0:
            return False
        else:
            return True

    def borders(self, actor : Token) -> str:
        if actor.x == self.columns - 1:
            return "right"
        elif actor.y == self.rows - 1:
            return "bottom"
        elif actor.x == 0:
            return "left"
        elif actor.y == 0:
            return "top"
        else:
            return None
