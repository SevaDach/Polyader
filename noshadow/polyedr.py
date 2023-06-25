from math import pi, sqrt
from common.r3 import R3
from common.tk_drawer import TkDrawer


class Edge:
    """ Ребро полиэдра """
    # Параметры конструктора: начало и конец ребра (точки в R3)

    def __init__(self, beg, fin):
        self.beg, self.fin = beg, fin


class Facet:
    """ Грань полиэдра """
    # Параметры конструктора: список вершин

    def __init__(self, vertexes):
        self.vertexes = vertexes
        self.ploschad = 0


def pl(tochki1,c):
    tochki = []
    for i in range(len(tochki1)):
        tochki.append(tochki1[i].__mul__(1/c))
    v1 = R3(tochki[0].x, tochki[0].y, tochki[0].z)
    ppl = 0
    for i in range(1, len(tochki)-1):
            
            
            
        v2 = R3(tochki[i].x, tochki[i].y, tochki[i].z)
        v3 = R3(tochki[i+1].x, tochki[i+1].y, tochki[i+1].z)
            
        v2v1 = R3(v2.x - v1.x, v2.y-v1.y, v2.z-v1.z)
        v3v1 = R3(v3.x - v1.x, v3.y-v1.y, v3.z-v1.z)
            #bb = R3(tochki[i-1].x-tochki[i].x, tochki[i-1].y-tochki[i].y, tochki[i-1].z-tochki[i].z)
        cc=  0.5*sqrt(v2v1.cross(v3v1).x*v2v1.cross(v3v1).x       +v2v1.cross(v3v1).y*v2v1.cross(v3v1).y    +v2v1.cross(v3v1).z*v2v1.cross(v3v1).z)
        ppl += cc
    return ppl



class Polyedr:
    """ Полиэдр """
    # Параметры конструктора: файл, задающий полиэдр

    def __init__(self, file):
        
        self.ploschad = 0
        
        # списки вершин, рёбер и граней полиэдра
        self.vertexes, self.edges, self.facets = [], [], []

        self.plohie = []
        self.plohiexxx = []
        self.plohieyyy = []
        self.plohiezzz = []
        
        # список строк файла
        with open(file) as f:
            for i, line in enumerate(f):
                if i == 0:
                    # обрабатываем первую строку; buf - вспомогательный массив
                    buf = line.split()
                    # коэффициент гомотетии
                    c = float(buf.pop(0))
                    # углы Эйлера, определяющие вращение
                    alpha, beta, gamma = (float(x) * pi / 180.0 for x in buf)
                elif i == 1:
                    # во второй строке число вершин, граней и рёбер полиэдра
                    nv, nf, ne = (int(x) for x in line.split())
                elif i < nv + 2:
                    # задание всех вершин полиэдра
                    x, y, z = (float(x) for x in line.split())
                    
                    rasst = abs(x-2)
                    if rasst >= 1:
                        #print('plohaia')
                        self.plohie.append(R3(x, y, z).rz(
                        alpha).ry(beta).rz(gamma) * c)
                    
                    for i in range(len(self.plohie)):
                        self.plohiexxx.append(self.plohie[i].x)
                        self.plohieyyy.append(self.plohie[i].y)
                        self.plohiezzz.append(self.plohie[i].z)
                                        
                    self.vertexes.append(R3(x, y, z).rz(
                        alpha).ry(beta).rz(gamma) * c)
                else:
                    # вспомогательный массив
                    buf = line.split()
                    # количество вершин очередной грани
                    size = int(buf.pop(0))
                    # массив вершин этой грани
                    vertexes = [self.vertexes[int(n) - 1] for n in buf]
                    schetcik_plohih_v_grane = 0

                    for i in range(len(vertexes)):
                        if vertexes[i].x in self.plohiexxx and vertexes[i].y in self.plohieyyy and vertexes[i].z in self.plohiezzz:
                            
                            
                            
                            
                            #print('suka')
                            schetcik_plohih_v_grane +=1
                    #print(schetcik_plohih_v_grane, len(vertexes))
                                      
                    
                    if schetcik_plohih_v_grane == len(vertexes):
                        #print('suka')
                        self.ploschad += pl(vertexes,c)
                        
                    # задание рёбер грани
                    for n in range(size):
                        self.edges.append(Edge(vertexes[n - 1], vertexes[n]))
                    # задание самой грани
                    self.facets.append(Facet(vertexes))

    # Метод изображения полиэдра
    def draw(self, tk):
        tk.clean()
        for e in self.edges:
            tk.draw_line(e.beg, e.fin)
        print('Сумма лощадей граней, все вершины которых не являются "хорошими" точками =', round(self.ploschad,1))