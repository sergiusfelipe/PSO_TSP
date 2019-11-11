

from operator import attrgetter
import random, sys, copy, math
import matplotlib.pyplot as plt


def graph(caminho):  # Gera um plano com as coordenadas da melhor rota encontrada
    rota = caminho
    cid = len(caminho)
    for j in range(0, cid):
        if j < cid - 1:
            cons1 = rota[j]
            cons2 = rota[j + 1]
        else:
            cons1 = rota[j]
            cons2 = rota[0]

        x1 = coordx[cons1]
        x2 = coordx[cons2]
        y1 = coordy[cons1]
        y2 = coordy[cons2]
        plt.plot((x1, x2), (y1, y2), 'b--')
        plt.plot((x1, x2), (y1, y2), 'ro')
    plt.annotate(u'Ponto de partida', xy=(coordx[rota[0]], coordy[rota[0]]), xytext=(coordx[rota[0]]+25, coordy[rota[0]]+25), arrowprops=dict(facecolor='black', shrink=0.05))
    plt.grid(True)
    plt.show()
    return

class ferramentas: #funcoes que serao utilizados
    def custo_caminho(self,solution): # Gera um fitness de todas as rotar de todas as particulas
        rota = solution
        cid = len(solution)
        custo = 0
        for i in range(0, cid):
            if i < cid - 1:
                cons1 = rota[i]
                cons2 = rota[i + 1]
            else:
                cons1 = rota[i]
                cons2 = rota[0]

            soma = ((coordx[cons1] - coordx[cons2]) ** 2) + ((coordy[cons1] - coordy[cons2]) ** 2)
            eucli = math.sqrt(soma)
            custo += eucli

        return custo

    def caminho_aleatorio(self): # Gera uma rota aleatoria para as particulas iniciais
        vertices = len(coordy)
        caminho = []
        for i in range(0,vertices):
            caminho.append(i)
        random.shuffle(caminho)
        return caminho

class Particle: # Define o formato das particulas

    def __init__(self, solution, cost):
        self.solution = solution

        self.pbest = solution

        self.cost_current_solution = cost
        self.cost_pbest_solution = cost

        self.velocity = []

    def setPBest(self, new_pbest):
        self.pbest = new_pbest

    def getPBest(self):
        return self.pbest

    def setVelocity(self, new_velocity):
        self.velocity = new_velocity

    def getVelocity(self):
        return self.velocity

    def setCurrentSolution(self, solution):
        self.solution = solution

    def getCurrentSolution(self):
        return self.solution

    def setCostPBest(self, cost):
        self.cost_pbest_solution = cost

    def getCostPBest(self):
        return self.cost_pbest_solution

    def setCostCurrentSolution(self, cost):
        self.cost_current_solution = cost

    def getCostCurrentSolution(self):
        return self.cost_current_solution

    def clearVelocity(self):
        del self.velocity[:]


class PSO: # A estrutura do pso

    def __init__(self, iterations, size_population, beta, alfa):
        self.iterations = iterations
        self.size_population = size_population
        self.particles = []
        self.beta = beta
        self.alfa = alfa
        self.solutions = []


        for i in range(0,size_population):
            rc = ferramentas.caminho_aleatorio(self)
            self.solutions.append(rc)
            i += 1

        for solution in self.solutions:
            particle = Particle(solution=solution, cost=ferramentas.custo_caminho(self,solution))
            self.particles.append(particle)

        self.size_population = len(self.particles)

    def setGBest(self, new_gbest):
        self.gbest = new_gbest

    def getGBest(self):
        return self.gbest

    def showsParticles(self):

        print('Showing particles...\n')
        for particle in self.particles:
            print('pbest: %s\t|\tcost pbest: %d\t|\tcurrent solution: %s\t|\tcost current solution: %d' \
                  % (str(particle.getPBest()), particle.getCostPBest(), str(particle.getCurrentSolution()),
                     particle.getCostCurrentSolution()))
        print('')

    def run(self):

        for t in range(self.iterations):

            self.gbest = min(self.particles, key=attrgetter('cost_pbest_solution'))

            for particle in self.particles:

                particle.clearVelocity()
                temp_velocity = []
                solution_gbest = copy.copy(self.gbest.getPBest())
                solution_pbest = particle.getPBest()[:]
                solution_particle = particle.getCurrentSolution()[:]

                # gera todos os operadores swap para calculo (pbest - x(t-1))
                for i in range(num_cida):
                    if solution_particle[i] != solution_pbest[i]:
                        swap_operator = (i, solution_pbest.index(solution_particle[i]), self.alfa)

                        temp_velocity.append(swap_operator)

                        aux = solution_pbest[swap_operator[0]]
                        solution_pbest[swap_operator[0]] = solution_pbest[swap_operator[1]]
                        solution_pbest[swap_operator[1]] = aux

                # gera todos os operadores swap para calculo (gbest - x(t-1))
                for i in range(num_cida):
                    if solution_particle[i] != solution_gbest[i]:
                        swap_operator = (i, solution_gbest.index(solution_particle[i]), self.beta)

                        temp_velocity.append(swap_operator)

                        aux = solution_gbest[swap_operator[0]]
                        solution_gbest[swap_operator[0]] = solution_gbest[swap_operator[1]]
                        solution_gbest[swap_operator[1]] = aux

                particle.setVelocity(temp_velocity)

                for swap_operator in temp_velocity:
                    if random.random() <= swap_operator[2]:
                        aux = solution_particle[swap_operator[0]]
                        solution_particle[swap_operator[0]] = solution_particle[swap_operator[1]]
                        solution_particle[swap_operator[1]] = aux

                particle.setCurrentSolution(solution_particle)
                cost_current_solution = ferramentas.custo_caminho(self,solution_particle)
                particle.setCostCurrentSolution(cost_current_solution)

                if cost_current_solution < particle.getCostPBest():
                    particle.setPBest(solution_particle)
                    particle.setCostPBest(cost_current_solution)


if __name__ == "__main__":
    i = 0
    global coordx
    global coordy

    coordx = []
    coordy = []
    linhas = []


    with open('\\users\stark\OneDrive\Área de Trabalho\Programação\Otimização por Enxame de Partículas - PSO\dj38.txt', 'r') as file: #aqui fica o caminho do arquido de dados
        for linha in file:
            linhas = linha.split()
            coordx.append(float(linhas[1]))
            coordy.append(float(linhas[2]))
            i += 1
    global num_cida
    num_cida = i

    pso = PSO(iterations=750, size_population=290, beta=0.8, alfa=0.7)
    pso.run()
    pso.showsParticles()
    gbest = pso.getGBest().getPBest()
    print('gbest: %s | cost: %d\n' % (gbest, pso.getGBest().getCostPBest()))
    graph(gbest)


    
