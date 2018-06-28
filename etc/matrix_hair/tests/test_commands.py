import itertools
import unittest

import commands
import exceptions


class TestCommands(unittest.TestCase):

    def test_create(self):
        '''
        Testa a criação da matriz com o método `create`.
        '''

        # Testa a criação com dimensões iguais a zero.
        # Deve resultar em exceção.
        for n, m in ((0, 0), (0, 1), (1, 0)):
            with self.subTest(m=m, n=n):
                try:
                    check = False
                    matrix = commands.create(m, n)
                except exceptions.InvalidSize:
                    check = True
                self.assertTrue(check)

        # Testa a criação com dimensões válidas
        for n in range(1, 5):
            for m in range(1, 5):
                with self.subTest(m=m, n=n):
                    matrix = commands.create(m, n)
                    # verifica o número de linhas
                    self.assertTrue(len(matrix) == m)
                    # verifica o conteúdo das colunas
                    self.assertTrue(
                        all(''.join(line) == 'O' * n for line in matrix))

    def test_clear(self):
        '''
        C
        Limpa a matriz. O tamanho permanece o mesmo.
        Todos os pixels ficam brancos (O).
        '''
        m, n = 5, 5
        matrix = commands.create(m, n)
        for line in matrix:
            line[2] = 'A'
        matrix_str = ''.join(itertools.chain.from_iterable(matrix))
        self.assertTrue(matrix_str != 'O' * m * n)

        matrix = commands.clear(matrix)
        matrix_str = ''.join(itertools.chain.from_iterable(matrix))
        self.assertTrue(matrix_str == 'O' * m * n)

    def test_paint_pixel(self):
        '''
        L X Y C
        Colore um pixel de coordenadas (X,Y) na cor C.
        '''
        raise Exception('Implement me!')

    def test_draw_vertical_line(self):
        '''
        V X Y1 Y2 C
        Desenha um segmento vertical na coluna X nas linhas
        de Y1 a Y2 (intervalo inclusivo) na cor C.
        '''
        raise Exception('Implement me!')

    def test_draw_horizontal_line(self):
        '''
        H X1 X2 Y C
        Desenha um segmento horizontal na linha Y nas
        colunas de X1 a X2 (intervalo inclusivo) na cor C.
        '''
        raise Exception('Implement me!')

    def test_draw_rectangle(self):
        '''
        K X1 Y1 X2 Y2 C
        Desenha um retangulo de cor C. (X1,Y1) é o canto superior
        esquerdo e (X2,Y2) o canto inferior direito.
        '''
        raise Exception('Implement me!')

    def test_fill_region(self):
        '''
        F X Y C
        Preenche a região com a cor C. A região R é definida da seguinte forma:
        O pixel (X,Y) pertence à região. Outro pixel pertence à região,
        se e somente se, ele tiver a mesma cor que o pixel (X,Y) e tiver
        pelo menos um lado em comum com um pixel pertencente à região.
        '''
        raise Exception('Implement me!')

    def test_save_image(self):
        '''
        S name
        Escreve a imagem em um arquivo de nome name.
        '''
        raise Exception('Implement me!')

    def test_quit(self):
        '''
        X
        Encerra o programa.
        '''
        raise Exception('Implement me!')


if __name__ == '__main__':
    unittest.main()
