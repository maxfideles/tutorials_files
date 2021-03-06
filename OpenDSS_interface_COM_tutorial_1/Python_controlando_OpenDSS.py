# coding: utf-8

import win32com.client
from pylab import *


class DSS():

    def __init__(self, end_modelo_DSS):

        self.end_modelo_DSS = end_modelo_DSS

        # Criar a conexão entre Python e OpenDSS
        self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")

        # Iniciar o Objeto DSS
        if self.dssObj.Start(0) == False:
            print "Problemas em iniciar o OpenDSS"
        else:
            # Criar variáveis paras as principais interfaces
            self.dssText = self.dssObj.Text
            self.dssCircuit = self.dssObj.ActiveCircuit
            self.dssSolution = self.dssCircuit.Solution
            self.dssCktElement = self.dssCircuit.ActiveCktElement
            self.dssBus = self.dssCircuit.ActiveBus
            self.dssLines = self.dssCircuit.Lines
            self.dssTransformers = self.dssCircuit.Transformers

    def versao_DSS(self):

        return self.dssObj.Version

    def compile_DSS(self):

        # Limpar informações da ultima simulação
        self.dssObj.ClearAll()

        self.dssText.Command = "compile " + self.end_modelo_DSS

    def solve_DSS_snapshot(self, multiplicador_carga):

        # Configurações
        self.dssText.Command = "Set Mode=SnapShot"
        self.dssText.Command = "Set ControlMode=Static"

        # Multiplicar o valor nominal das cargas pelo multiplicador_carga
        self.dssSolution.LoadMult = multiplicador_carga

        # Resolve o Fluxo de Potência
        self.dssSolution.Solve()

    def get_resultados_potencia(self):
        self.dssText.Command = "Show powers kva elements"

    def get_nome_circuit(self):

        return self.dssCircuit.Name

    def get_potencias_circuit(self):

        p = -self.dssCircuit.TotalPower[0]
        q = -self.dssCircuit.TotalPower[1]

        return p, q

    def ativa_barra(self, nome_barra):

        # Ativa a barra pelo seu nome
        self.dssCircuit.SetActiveBus(nome_barra)

        # Retornar o nome da barra ativada
        return self.dssBus.Name

    def get_distancia_barra(self):
        return self.dssBus.Distance

    def get_kVBase_barra(self):
        return self.dssBus.kVBase

    def get_VMagAng_barra(self):
        return self.dssBus.VMagAngle

    def ativa_elemento(self, nome_elemento):

        # Ativa elemento pelo seu nome completo Tipo.Nome
        self.dssCircuit.SetActiveElement(nome_elemento)

        # Retonar o nome do elemento ativado
        return self.dssCktElement.Name

    def get_barras_elemento(self):

        barras = self.dssCktElement.BusNames

        barra1 = barras[0]
        barra2 = barras[1]

        return barra1, barra2

    def get_tensoes_elemento(self):

        return self.dssCktElement.VoltagesMagAng

    def get_potencias_elemento(self):
        return self.dssCktElement.Powers

    def get_nome_linha(self):
        return self.dssLines.Name

    def get_tamanho_linha(self):
        return self.dssLines.Length

    def set_tamanho_linha(self, tamanho):
        self.dssLines.Length = tamanho

    def get_nome_trafo(self):
        return self.dssTransformers.Name

    def get_tensao_terminal_trafo(self, terminal):

        # Ativa um dos terminais do transformador
        self.dssTransformers.Wdg = terminal

        return self.dssTransformers.kV

    def get_nome_e_tamanho_linhas(self):

        # Definindo duas listas
        nome_linhas_lista = []
        tamanho_linhas_lista = []

        # Seleciona a primeira linha
        self.dssLines.First

        for i in range(self.dssLines.Count):

            nome_linhas_lista.append(self.dssLines.Name)
            tamanho_linhas_lista.append(self.dssLines.Length)

            self.dssLines.Next

        return nome_linhas_lista, tamanho_linhas_lista


if __name__ == "__main__":
    print """Autor: Paulo Radatz \nData: Fevereiro/2018 \nE-mail: paulo.radatz@gmail.com/paulo.radatz@usp.br \n"""

    # Criar um objeto da classe DSS
    objeto = DSS(r"D:\Gdrive\Tutoriais\OpenDSS-Python\Projeto_Funcionando\Master.dss")

    print u"Versão do OpenDSS: " + objeto.versao_DSS() + "\n"

    # Resolver o Fluxo de Potência
    objeto.compile_DSS()
    objeto.solve_DSS_snapshot(1.0)

    # Arquivo de Resultado
    ##objeto.get_resultados_potencia()

    # Informações do elemento Circuit
    p, q = objeto.get_potencias_circuit()
    print u"Nosso exemplo apresenta o nome do elemnto Circuit: " + objeto.get_nome_circuit()
    print u"Fornece Potência Ativa: " + str(p) + " kW"
    print u"Fornece Potência Reativa: " + str(q) + " kvar \n"

    # Informações da Barra escolhida
    print u"Barra Ativa: " + objeto.ativa_barra("C")
    print u"Distância do EnergyMeter: " + str(objeto.get_distancia_barra())
    print u"Tensão de Base da Barra (kV) : " + str(sqrt(3) * objeto.get_kVBase_barra())
    print u"Tensões dessa Barra (kV): " + str(objeto.get_VMagAng_barra()) + "\n"

    # Informações do elemento escolhido
    print u"Elemento Ativo: " + objeto.ativa_elemento("Line.Linha1")
    barra1, barra2 = objeto.get_barras_elemento()
    print u"Esse elemento está conectado entre as barras: " + barra1 + " e " + barra2
    print u"As tensões nodais desse elemento (kV): " + str(objeto.get_tensoes_elemento())
    print u"As potências desse elemento (kW) e (kvar): " + str(objeto.get_potencias_elemento()) + "\n"

    # Informações dos dados da linha escolhida
    print u"Elemento Ativo: " + objeto.ativa_elemento("Line.Linha1")
    print u"Nome da linha ativa: " + objeto.get_nome_linha()
    print u"Tamanho da linha ativa: " + str(objeto.get_tamanho_linha())
    print u"Alterando o tamanho da linha para 0.4 km."
    objeto.set_tamanho_linha(0.4)
    print u"Novo tamanho da linha ativa: " + str(objeto.get_tamanho_linha()) + "\n"

    # informações do transformador
    print u"Transformador Ativo: " + objeto.ativa_elemento("Transformer.Trafo")
    print u"Nome do Transformador ativo: " + objeto.get_nome_trafo()
    print u"Tensão nominal do primário: " + str(objeto.get_tensao_terminal_trafo(1))
    print u"Tensão nominal do secundário: " + str(objeto.get_tensao_terminal_trafo(2)) + "\n"

    # Nome e tamanho de todas as linhas
    nome_linhas, tamanho_linhas = objeto.get_nome_e_tamanho_linhas()
    print u"Nomes das linhas: " + str(nome_linhas)
    print u"Tamanhos das linhas: " + str(tamanho_linhas)