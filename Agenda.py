import sys
import pickle
from functools import total_ordering


def nulo_ou_vazio(texto):
    return texto is None or not texto.strip()

def valida_faixa_inteiro(pergunta, inicio, fim, padrão=None):
    while True:
        try:
            entrada = input(pergunta)
            if nulo_ou_vazio(entrada) and padrão is not None:
                return padrão
            valor = int(entrada)
            if inicio <= valor <= fim:
                return valor
            print(f"Valor fora do intervalo [{inicio}, {fim}].")
        except ValueError:
            print("Por favor, digite um número válido.")

class ListaÚnica:
    def __init__(self, elem_class):
        self.lista = []
        self.elem_class = elem_class

    def __len__(self):
        return len(self.lista)

    def __iter__(self):
        return iter(self.lista)

    def __getitem__(self, index):
        return self.lista[index]

    def adiciona(self, elem):
        if self.pesquisa(elem) == -1:
            self.lista.append(elem)

    def remove(self, elem):
        self.lista.remove(elem)

    def pesquisa(self, elem):
        self.verifica_tipo(elem)
        try:
            return self.lista.index(elem)
        except ValueError:
            return -1

    def verifica_tipo(self, elem):
        if not isinstance(elem, self.elem_class):
            raise TypeError(f"Elemento deve ser do tipo {self.elem_class.__name__}")

    def ordena(self, chave=None):
        self.lista.sort(key=chave)

@total_ordering
class Nome:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f"<Nome: {self.nome}>"

    def __eq__(self, outro):
        return self.nome == outro.nome

    def __lt__(self, outro):
        return self.nome < outro.nome

    @staticmethod
    def cria_chave(nome):
        return nome.strip().lower()

class Telefone:
    def __init__(self, numero, tipo=None):
        self.numero = numero
        self.tipo = tipo

    def __str__(self):
        tipo = f" ({self.tipo})" if self.tipo else ""
        return f"{self.numero}{tipo}"

    def __eq__(self, outro):
        return self.numero == outro.numero and self.tipo == outro.tipo

class Telefones(ListaÚnica):
    def __init__(self):
        super().__init__(Telefone)

class TiposTelefone(ListaÚnica):
    def __init__(self):
        super().__init__(str)

class DadoAgenda:
    def __init__(self, nome):
        self.nome = nome
        self.telefones = Telefones()

    def pesquisa_telefone(self, telefone):
        return self.telefones.pesquisa(telefone)

class Agenda(ListaÚnica):
    def __init__(self):
        super().__init__(DadoAgenda)
        self.tipos_telefone = TiposTelefone()

    def adiciona_tipo(self, tipo):
        self.tipos_telefone.adiciona(tipo)

    def pesquisa_nome(self, nome):
        for dado in self.lista:
            if dado.nome == nome:
                return dado
        return None

    def ordena(self):
        super().ordena(lambda dado: str(dado.nome))


class Menu:
    def __init__(self):
        self.opcoes = [["Sair", None]]

    def adiciona_opcao(self, nome, funcao):
        self.opcoes.append([nome, funcao])

    def exibe(self):
        print("\n==== MENU ====")
        for i, opcao in enumerate(self.opcoes):
            print(f"[{i}] - {opcao[0]}")
        print()

    def execute(self):
        while True:
            self.exibe()
            escolha = valida_faixa_inteiro("Escolha uma opção: ", 0, len(self.opcoes) - 1)
            if escolha == 0:
                break
            self.opcoes[escolha][1]()

class AppAgenda:
    def __init__(self):
        self.agenda = Agenda()
        self.agenda.adiciona_tipo("Celular")
        self.agenda.adiciona_tipo("Residencial")
        self.agenda.adiciona_tipo("Trabalho")
        self.menu = Menu()
        self.menu.adiciona_opcao("Novo", self.novo)
        self.menu.adiciona_opcao("Lista", self.lista)

    @staticmethod
    def pede_nome():
        return input("Nome: ")

    @staticmethod
    def pede_telefone():
        return input("Telefone: ")

    def novo(self):
        nome = self.pede_nome()
        if nulo_ou_vazio(nome):
            print("Nome inválido.")
            return
        if self.agenda.pesquisa_nome(nome):
            print("Nome já existe.")
            return
        dado = DadoAgenda(nome)
        telefone = self.pede_telefone()
        if telefone:
            dado.telefones.adiciona(Telefone(telefone))
        self.agenda.adiciona(dado)
        print("Contato adicionado.")

    def lista(self):
        if len(self.agenda) == 0:
            print("Agenda vazia.")
            return
        for dado in self.agenda:
            print(f"Nome: {dado.nome}")
            for telefone in dado.telefones:
                print(f"  Telefone: {telefone}")
        print()

    def execute(self):
        self.menu.execute()

if __name__ == "__main__":
    app = AppAgenda()
    app.execute()