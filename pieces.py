import pygame
import os.path
from copy import deepcopy
from define import *
from tools import *


class Pieces(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Pieces, self).__init__()
        self.screen = screen
        self.init_array_pieces()
        self.init_surf_pieces()

    def init_array_pieces(self):
        self.ar = [['  ' for i in range(8)] for i in range(8)]
        for i in (0, 7):
            if i == 0:
                bw = 'b'
            else:
                bw = 'w'
            self.ar[i][0] = bw + 'r'
            self.ar[i][1] = bw + 'n'
            self.ar[i][2] = bw + 'b'
            self.ar[i][3] = bw + 'q'
            self.ar[i][4] = bw + 'k'
            self.ar[i][5] = bw + 'b'
            self.ar[i][6] = bw + 'n'
            self.ar[i][7] = bw + 'r'
        for i in range(8):
            self.ar[1][i] = 'bp'
            self.ar[6][i] = 'wp'

    def init_surf_pieces(self):
        self.P = {
            'br': Rook(B['rook'], None, 'b'),
            'bn': Knight(B['knight'], None, 'b'),
            'bb': Bishop(B['bishop'], None, 'b'),
            'bq': Queen(B['queen'], None, 'b'),
            'bk': King(B['king'], None, 'b'),
            'bp': Pawn(B['pawn'], None, 'b'),

            'wr': Rook(W['rook'], None, 'w'),
            'wn': Knight(W['knight'], None, 'w'),
            'wb': Bishop(W['bishop'], None, 'w'),
            'wq': Queen(W['queen'], None, 'w'),
            'wk': King(W['king'], None, 'w'),
            'wp': Pawn(W['pawn'], None, 'w'),

            '  ': None
        }

    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                if self.ar[i][j] != '  ':
                    if self.ar[i][j] == '..':
                        pygame.draw.circle(self.screen, RED, cal_rect(0, i+1, j+1), CIRCLE_RADIUS)
                    elif self.ar[i][j][0] == '.':
                        self.P[self.ar[i][j][1:]].rect = cal_rect(1, i+1,j+1)
                        self.screen.blit(self.P[self.ar[i][j][1:]].surf, cal_rect(1, i+1,j+1))
                    else:
                        self.P[self.ar[i][j]].rect = cal_rect(1, i+1,j+1)
                        self.screen.blit(self.P[self.ar[i][j]].surf, cal_rect(1, i+1,j+1))

    def selecting(self, p):
        x, y = p[0]-1, p[1]-1
        lst = self.available_moves(self.ar[x][y], p, self.ar[x][y][0])

        if lst != []:
            for i in lst:
                if self.ar[i[0]][i[1]] != '  ':
                    self.ar[i[0]][i[1]] = '.' + self.ar[i[0]][i[1]]
                else:
                    self.ar[i[0]][i[1]] = '..'

    def available_moves(self, pc, p, type):
        return self.P[pc].a_moves(self.ar, p, type)



    def move(self, r, rr):
        a, b, c, d = r[0]-1, r[1]-1, rr[0]-1, rr[1]-1
        if self.ar[c][d][0] == '.':
            self.ar[c][d] = deepcopy(self.ar[a][b])
            self.ar[a][b] = '  '
        else:
            return 0
        for i in range(8):
            for j in range(8):
                if self.ar[i][j] == '..':
                    self.ar[i][j] = '  '
                if self.ar[i][j][:2] == '.w' or self.ar[i][j][:2] == '.b':
                    self.ar[i][j] = self.ar[i][j][1:]
        return 1

    def precond(self, p):
        if self.ar[p[0]-1][p[1]-1] != '  ':
            return True
        return False

class King(pygame.sprite.Sprite):

    def __init__(self, surf, rect, type):
        super(King, self).__init__()
        self.surf = surf
        self.surf.set_colorkey(BLACK, RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, (PIECE_SIZE, PIECE_SIZE))
        self.rect = rect
        self.type = type

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        index = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
        for i in index:
            nx, ny = x+i[0], y+i[1]
            if check_valid(nx, ny):
                if ar[nx][ny] == '  ' or ar[x][y][0] != ar[nx][ny][0]:
                    lst.append((nx, ny))
        return lst

class Queen(King):
    def __init__(self, surf, rect, type):
        super(Queen, self).__init__(surf, rect, type)

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        index = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
        for i in index:
            nx, ny = x+i[0], y+i[1]
            if check_valid(nx, ny):
                if ar[nx][ny] == '  ' or ar[x][y][0] != ar[nx][ny][0]:
                    lst.append((nx, ny))
        return lst


class Bishop(King):
    def __init__(self, surf, rect, type):
        super(Bishop, self).__init__(surf, rect, type)

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        index = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
        for i in index:
            nx, ny = x+i[0], y+i[1]
            if check_valid(nx, ny):
                if ar[nx][ny] == '  ' or ar[x][y][0] != ar[nx][ny][0]:
                    lst.append((nx, ny))
        return lst

class Rook(King):
    def __init__(self, surf, rect, type):
        super(Rook, self).__init__(surf, rect, type)

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        index = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
        for i in index:
            nx, ny = x+i[0], y+i[1]
            if check_valid(nx, ny):
                if ar[nx][ny] == '  ' or ar[x][y][0] != ar[nx][ny][0]:
                    lst.append((nx, ny))
        return lst

class Knight(King):
    def __init__(self, surf, rect, type):
        super(Knight, self).__init__(surf, rect, type)

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        index = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
        for i in index:
            nx, ny = x+i[0], y+i[1]
            if check_valid(nx, ny):
                if ar[nx][ny] == '  ' or ar[x][y][0] != ar[nx][ny][0]:
                    lst.append((nx, ny))
        return lst

class Pawn(King):
    def __init__(self, surf, rect, type):
        super(Pawn, self).__init__(surf, rect, type)

    def a_moves(self, ar, p, type):
        x, y, lst = p[0]-1, p[1]-1, []
        index = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
        for i in index:
            nx, ny = x+i[0], y+i[1]
            if check_valid(nx, ny):
                if ar[nx][ny] == '  ' or ar[x][y][0] != ar[nx][ny][0]:
                    lst.append((nx, ny))
        return lst
