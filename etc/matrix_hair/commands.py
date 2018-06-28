import itertools

from PIL import Image

import exceptions


def create(m, n):
    '''
    I M N
    Cria uma nova matriz MxN. Todos os pixels são brancos (O).
    '''
    if all([m > 0, n > 0]):
        return [['O'] * n for i in range(m)]
    else:
        raise exceptions.InvalidSize()


def clear(matrix):
    '''
    C
    Limpa a matriz. O tamanho permanece o mesmo.
    Todos os pixels ficam brancos (O).
    '''
    for i in range(len(matrix)):
        matrix[i] = ['O'] * len(matrix[i])
    return matrix


def paint_pixel(matrix, x, y, color):
    '''
    L X Y C
    Colore um pixel de coordenadas (X,Y) na cor C.
    '''
    matrix[x:y] = color


def draw_vertical_line(matrix, x, y1, y2, color):
    '''
    V X Y1 Y2 C
    Desenha um segmento vertical na coluna X nas linhas
    de Y1 a Y2 (intervalo inclusivo) na cor C.
    '''
    raise Exception('Implement me!')


def draw_horizontal_line(matrix, x1, y2, y, color):
    '''
    H X1 X2 Y C
    Desenha um segmento horizontal na linha Y nas
    colunas de X1 a X2 (intervalo inclusivo) na cor C.
    '''
    raise Exception('Implement me!')


def draw_rectangle(matrix, x1, y1, x2, y2, color):
    '''
    K X1 Y1 X2 Y2 C
    Desenha um retangulo de cor C. (X1,Y1) é o canto superior
    esquerdo e (X2,Y2) o canto inferior direito.
    '''
    raise Exception('Implement me!')


def fill_region(matrix, x, y, color):
    '''
    F X Y C
    Preenche a região com a cor C. A região R é definida da seguinte forma:
    O pixel (X,Y) pertence à região. Outro pixel pertence à região,
    se e somente se, ele tiver a mesma cor que o pixel (X,Y) e tiver
    pelo menos um lado em comum com um pixel pertencente à região.
    '''
    raise Exception('Implement me!')


def save_image(matrix, filename):
    '''
    S name
    Escreve a imagem em um arquivo de nome name.
    '''
    raise Exception('Implement me!')


def quit():
    '''
    X
    Encerra o programa.
    '''
    raise Exception('Implement me!')
