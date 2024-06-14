class AnalisadorSintatico:
    def __init__(self, lista) -> None:
        self.tokensnome = {
            '+': 1, '-': 2, '/': 3, '*': 4, 'mod': 5, 'div': 6,
            'or': 7, 'and': 8, 'not': 9, '==': 10, '<>': 11, '>': 12,
            '<': 13, '>=': 14, '<=': 15, ':=': 16, 'program': 17, 'var': 18,
            'integer': 19, 'real': 20, 'string': 21, 'begin': 22, 'end': 23,
            'for': 24, 'to': 25, 'while': 26, 'do': 27, 'break': 28,
            'continue': 29, 'if': 30, 'else': 31, 'then': 32, 'write': 33,
            'read': 34, ';': 35, ':': 36, ',': 37, '.': 38, '(': 39,
            ')': 40, '[': 41, ']': 42, '{': 43, '}': 44, 'STR': 45, 'IDENT': 46
        }
        self.index = -1
        self.lista = lista

    def consome(self, token_esperado):
        self.index += 1
        lista_tupla = self.lista[self.index]
        if lista_tupla[0] == token_esperado:
            return
        else:
            print('ERRO NA LINHA: ', lista_tupla)
            print('TOKEN ESPERADO: ', token_esperado)
            sys.exit()
            return

    def function(self):
        self.consome(self.tokensnome['program'])
        self.consome(self.tokensnome['IDENT'])
        self.corpo()

    def corpo(self):
        self.decl()
        self.consome(self.tokensnome['begin'])
        self.sentencas()
        self.consome(self.tokensnome['end'])
        return

    def decl(self):
        if self.lista[self.index + 1][0] == self.tokensnome['var']:
            self.consome(self.tokensnome['var'])
            self.listaident()
            self.consome(self.tokensnome[':'])
            self.tipo()
            self.consome(self.tokensnome[';'])
            self.decl()
        else:
            return

    def listaident(self):
        self.consome(self.tokensnome['IDENT'])
        self.listaresto()
        return

    def listaresto(self):
        if self.lista[self.index + 1][0] == self.tokensnome[',']:
            self.consome(self.tokensnome[','])
            self.listaident()
        else:
            return

    def tipo(self):
        if self.lista[self.index + 1][0] in (self.tokensnome['integer'], self.tokensnome['real'], self.tokensnome['string']):
            self.consome(self.lista[self.index + 1][0])
        return

    def sentencas(self):
        self.sentenca()
        self.restosentencas()
        return

    def restosentencas(self):
        if self.lista[self.index + 1][0] == self.tokensnome[';']:
            self.consome(self.tokensnome[';'])
            self.sentenca()
            self.restosentencas()
        else:
            return

    def sentenca(self):
        prox_token = self.lista[self.index + 1][0]
        if prox_token == self.tokensnome['IDENT']:
            self.atribuicao()
        elif prox_token == self.tokensnome['if']:
            self.condicional()
        elif prox_token == self.tokensnome['while']:
            self.enquanto()
        elif prox_token == self.tokensnome['read']:
            self.leitura()
        elif prox_token == self.tokensnome['write']:
            self.escrita()
        else:
            return

    def atribuicao(self):
        self.consome(self.tokensnome['IDENT'])
        self.consome(self.tokensnome[':='])
        self.expr()
        return

    def condicional(self):
        self.consome(self.tokensnome['if'])
        self.expr()
        self.consome(self.tokensnome['then'])
        self.sentenca()
        if self.lista[self.index + 1][0] == self.tokensnome['else']:
            self.consome(self.tokensnome['else'])
            self.sentenca()
        return

    def enquanto(self):
        self.consome(self.tokensnome['while'])
        self.expr()
        self.consome(self.tokensnome['do'])
        self.sentenca()
        return

    def leitura(self):
        self.consome(self.tokensnome['read'])
        self.consome(self.tokensnome['('])
        self.consome(self.tokensnome['IDENT'])
        self.consome(self.tokensnome[')'])
        return

    def escrita(self):
        self.consome(self.tokensnome['write'])
        self.consome(self.tokensnome['('])
        self.expr()
        self.consome(self.tokensnome[')'])
        return

    def expr(self):
        self.term()
        self.resto()
        return

    def resto(self):
        prox_token = self.lista[self.index + 1][0]
        if prox_token == self.tokensnome['+']:
            self.consome(self.tokensnome['+'])
            self.term()
            self.resto()
        elif prox_token == self.tokensnome['-']:
            self.consome(self.tokensnome['-'])
            self.term()
            self.resto()
        else:
            return

    def term(self):
        self.uno()
        self.restoMult()
        return

    def restoMult(self):
        prox_token = self.lista[self.index + 1][0]
        if prox_token == self.tokensnome['*']:
            self.consome(self.tokensnome['*'])
            self.uno()
            self.restoMult()
        elif prox_token == self.tokensnome['/']:
            self.consome(self.tokensnome['/'])
            self.uno()
            self.restoMult()
        elif prox_token == self.tokensnome['mod']:
            self.consome(self.tokensnome['mod'])
            self.uno()
            self.restoMult()
        elif prox_token == self.tokensnome['div']:
            self.consome(self.tokensnome['div'])
            self.uno()
            self.restoMult()
        else:
            return

    def uno(self):
        prox_token = self.lista[self.index + 1][0]
        if prox_token == self.tokensnome['+']:
            self.consome(self.tokensnome['+'])
            self.uno()
        elif prox_token == self.tokensnome['-']:
            self.consome(self.tokensnome['-'])
            self.uno()
        else:
            self.factor()
        return

    def factor(self):
        prox_token = self.lista[self.index + 1][0]
        if prox_token == self.tokensnome['integer']:
            self.consome(self.tokensnome['integer'])
        elif prox_token == self.tokensnome['real']:
            self.consome(self.tokensnome['real'])
        elif prox_token == self.tokensnome['IDENT']:
            self.consome(self.tokensnome['IDENT'])
        elif prox_token == self.tokensnome['(']:
            self.consome(self.tokensnome['('])
            self.expr()
            self.consome(self.tokensnome[')'])
        elif prox_token == self.tokensnome['STR']:
            self.consome(self.tokensnome['STR'])
        return

class Interpretador:
    def __init__(self):
        self.variaveis = {}
        self.labels = {}
        self.ponteiro = 0

    def carregar_labels(self, instrucoes):
        for i, instrucao in enumerate(instrucoes):
            if instrucao[0] == 'LABEL':
                self.labels[instrucao[1]] = i

    def executar(self, instrucoes):
        while self.ponteiro < len(instrucoes):
            instrucao = instrucoes[self.ponteiro]
            operador = instrucao[0]
            if operador in ('+', '-', '*', '/', 'mod', 'div'):
                self.operacao_aritmetica(instrucao)
            elif operador in ('or', 'and', 'not'):
                self.operacao_logica(instrucao)
            elif operador in ('==', '<>', '>', '<', '>=', '<='):
                self.operacao_relacional(instrucao)
            elif operador == ':=':
                self.atribuicao(instrucao)
            elif operador == 'IF':
                self.condicional(instrucao)
            elif operador == 'JUMP':
                self.jump(instrucao)
            elif operador == 'CALL':
                self.chamada_sistema(instrucao)
            elif operador == 'LABEL':
                pass  # Labels são processados na inicialização
            else:
                raise ValueError(f"Operador desconhecido: {operador}")
            self.ponteiro += 1

    def operacao_aritmetica(self, instrucao):
        operador, guardar, operando1, operando2 = instrucao
        if operador == '+':
            self.variaveis[guardar] = self.variaveis.get(operando1, 0) + self.variaveis.get(operando2, 0)
        elif operador == '-':
            self.variaveis[guardar] = self.variaveis.get(operando1, 0) - self.variaveis.get(operando2, 0)
        elif operador == '*':
            self.variaveis[guardar] = self.variaveis.get(operando1, 0) * self.variaveis.get(operando2, 0)
        elif operador == '/':
            self.variaveis[guardar] = self.variaveis.get(operando1, 0) / self.variaveis.get(operando2, 0)
        elif operador == 'mod':
            self.variaveis[guardar] = self.variaveis.get(operando1, 0) % self.variaveis.get(operando2, 0)
        elif operador == 'div':
            self.variaveis[guardar] = self.variaveis.get(operando1, 0) // self.variaveis.get(operando2, 0)

    def operacao_logica(self, instrucao):
        operador, guardar, operando1, operando2 = instrucao
        if operador == 'or':
            self.variaveis[guardar] = self.variaveis.get(operando1, False) or self.variaveis.get(operando2, False)
        elif operador == 'and':
            self.variaveis[guardar] = self.variaveis.get(operando1, False) and self.variaveis.get(operando2, False)
        elif operador == 'not':
            self.variaveis[guardar] = not self.variaveis.get(operando1, False)

    def operacao_relacional(self, instrucao):
        operador, guardar, operando1, operando2 = instrucao
        if operador == '==':
            self.variaveis[guardar] = self.variaveis.get(operando1) == self.variaveis.get(operando2)
        elif operador == '<>':
            self.variaveis[guardar] = self.variaveis.get(operando1) != self.variaveis.get(operando2)
        elif operador == '>':
            self.variaveis[guardar] = self.variaveis.get(operando1) > self.variaveis.get(operando2)
        elif operador == '<':
            self.variaveis[guardar] = self.variaveis.get(operando1) < self.variaveis.get(operando2)
        elif operador == '>=':
            self.variaveis[guardar] = self.variaveis.get(operando1) >= self.variaveis.get(operando2)
        elif operador == '<=':
            self.variaveis[guardar] = self.variaveis.get(operando1) <= self.variaveis.get(operando2)

    def atribuicao(self, instrucao):
        _, guardar, operando1, _ = instrucao
        self.variaveis[guardar] = self.variaveis.get(operando1, 0)

    def condicional(self, instrucao):
        _, condicao, label1, label2 = instrucao
        if self.variaveis.get(condicao, False):
            self.ponteiro = self.labels[label1] - 1
        else:
            self.ponteiro = self.labels[label2] - 1

    def jump(self, instrucao):
        _, label, _, _ = instrucao
        self.ponteiro = self.labels[label] - 1

    def chamada_sistema(self, instrucao):
        _, comando, valor, _ = instrucao
        if comando == 'PRINT':
            print(self.variaveis.get(valor, ''))
        elif comando == 'SCAN':
            self.variaveis[valor] = input()

if __name__ == "__main__":
    import lexico, sys
    if len(sys.argv) > 1:
        lista = lexico.main(sys.argv[1])
        AnSint = AnalisadorSintatico(lista)
        AnSint.function()

        # Carregar e executar o interpretador
        interpretador = Interpretador()
        interpretador.carregar_labels(lista)
        interpretador.executar(lista)
