import pygame
import pygame.gfxdraw

from const import *
from board import Board
from dragger import Dragger
from config import Config

class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

        # chinh
        self.drawn_moves = set()

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if(row + col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)


        letters = 'abcdefgh'
        font = pygame.font.SysFont("Arial", 18, bold=True)
        for row in range(ROWS):
            label = font.render(str(ROWS - row), True, (234, 235, 200)) if row%2 == 1 else font.render(str(ROWS - row), True, (119, 154, 88))
            x = 5 
            y = row * SQSIZE + 5
            surface.blit(label, (x, y))

        for col in range(COLS):
            label = font.render(letters[col], True, (119, 154, 88)) if col%2 == 1 else font.render(letters[col], True, (234, 235, 200))
            x = col * SQSIZE + SQSIZE // 2 + 28
            y = ROWS * SQSIZE - 22
            surface.blit(label, (x, y))

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        piece.set_texture(size = 64)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            self.drawn_moves.clear()
            for move in piece.moves:
                # chinh
                if (move.final.row, move.final.col) in self.drawn_moves:
                    continue
                if self.board.squares[move.final.row][move.final.col].isempty() == False:
                    if self.board.squares[move.final.row][move.final.col].has_enemy_piece(self.board.squares[move.initial.row][move.initial.col].piece.color):
                        img = pygame.image.load('assets/images/circle.png').convert_alpha()
                        img_center = move.final.col * SQSIZE + SQSIZE // 2, move.final.row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)
                else:
                    light_gray = (100, 100, 120, 80)
                    center_x = move.final.col * SQSIZE + SQSIZE // 2
                    center_y = move.final.row * SQSIZE + SQSIZE // 2
                    radius = SQSIZE // 6
                    pygame.gfxdraw.filled_circle(surface, center_x, center_y, radius, light_gray)
                    pygame.gfxdraw.aacircle(surface, center_x, center_y, radius, light_gray)
                    self.drawn_moves.add((move.final.row, move.final.col))

    # chinh
    def reset_moves(self):
        self.drawn_moves.clear()

    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
