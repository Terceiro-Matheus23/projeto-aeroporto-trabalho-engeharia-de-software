#Juan David Fontecha RA:82419678
#Matheus Terceiro Daniel RA:824121622
#Kaique Nunes Dicheman RA:824132510
import random

# =========================
# BARRA DE VIDA
# =========================
def mostrar_barra(vida, vida_max):
    total = 20
    proporcao = vida / vida_max
    cheios = int(total * proporcao)
    vazios = total - cheios
    return "[" + "❤️" * cheios + "░" * vazios + f"] {vida}/{vida_max}"


# =========================
# ARMA
# =========================
class Arma:
    def __init__(self, nome, bonus):
        self.nome = nome
        self.bonus = bonus


# =========================
# PERSONAGEM
# =========================
class Personagem:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe

        if classe == "Guerreiro":
            self.vida = 130
            self.forca = 14
        elif classe == "Mago":
            self.vida = 90
            self.forca = 18
        else:
            self.vida = 110
            self.forca = 15

        self.vida_max = self.vida
        self.pocoes = 2
        self.ouro = 0
        self.xp = 0
        self.nivel = 1
        self.arma = None
        self.esquiva_ativa = False

    def mostrar_status(self):
        print(f"\n{self.nome} (Nv {self.nivel})")
        print(mostrar_barra(self.vida, self.vida_max))
        arma = self.arma.nome if self.arma else "Nenhuma"
        print(f"Ouro: {self.ouro} | Pocoes: {self.pocoes} | Arma: {arma}")

    def calcular_dano(self):
        bonus = self.arma.bonus if self.arma else 0
        return self.forca + bonus

    def atacar(self, inimigo):
        critico = random.random() < 0.2
        dano = self.calcular_dano() * 2 if critico else self.calcular_dano()
        print(f"{self.nome} atacou causando {dano}")
        inimigo.receber_dano(dano)

    def esquivar(self):
        self.esquiva_ativa = True
        print("Preparado para esquivar")

    def habilidade(self, inimigo):
        if self.classe == "Guerreiro":
            dano = self.calcular_dano() + 8
            print("Golpe pesado")
            inimigo.receber_dano(dano)

        elif self.classe == "Mago":
            self.vida = min(self.vida + 25, self.vida_max)
            print("Cura aplicada")

        else:
            print("Ataque duplo")
            inimigo.receber_dano(self.calcular_dano())
            inimigo.receber_dano(self.calcular_dano())

    def usar_pocao(self):
        if self.pocoes > 0:
            self.vida = min(self.vida + 30, self.vida_max)
            self.pocoes -= 1
            print("Vida recuperada")
        else:
            print("Sem pocoes")

    def receber_dano(self, dano, inimigo):
        # Sistema de esquiva
        if self.esquiva_ativa:
            self.esquiva_ativa = False

            chance = random.random()

            if chance < 0.5:
                print("Voce esquivou completamente do ataque!")
                return

            elif chance < 0.8:
                print("Voce esquivou e contra-atacou!")
                inimigo.receber_dano(self.calcular_dano() // 2)
                return

            else:
                print("Falhou ao esquivar...")

        self.vida -= dano
        print(f"Voce recebeu {dano} de dano")

    def ganhar_xp(self, valor):
        self.xp += valor
        if self.xp >= 50:
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.xp = 0
        self.vida_max += 15
        self.forca += 3
        self.vida = self.vida_max
        print(f"Subiu para nivel {self.nivel}")

    def esta_vivo(self):
        return self.vida > 0


# =========================
# INIMIGO
# =========================
class Inimigo:
    def __init__(self, nome, vida, forca):
        self.nome = nome
        self.vida = vida
        self.forca = forca
        self.vida_max = vida

    def mostrar_status(self):
        print(f"\n{self.nome}")
        print(mostrar_barra(self.vida, self.vida_max))

    def agir(self, jogador):
        dano = random.randint(self.forca - 2, self.forca + 2)
        print(f"{self.nome} atacou causando {dano}")
        jogador.receber_dano(dano, self)

    def receber_dano(self, dano):
        self.vida -= dano

    def esta_vivo(self):
        return self.vida > 0


# =========================
# CHEFAO
# =========================
class Chefao(Inimigo):
    def __init__(self):
        super().__init__("Dragao Anciao", 220, 20)

    def agir(self, jogador):
        if random.random() < 0.4:
            dano = self.forca + 10
            print("Ataque de fogo causando", dano)
        else:
            dano = self.forca
            print("Ataque pesado causando", dano)

        jogador.receber_dano(dano, self)


# =========================
# GERAR INIMIGO
# =========================
def gerar_inimigo():
    lista = [
        ("Goblin", 70, 10),
        ("Orc", 100, 14),
        ("Esqueleto", 80, 12),
        ("Lobo", 90, 13),
        ("Bruxo", 85, 16)
    ]
    return Inimigo(*random.choice(lista))


# =========================
# LOJA
# =========================
def loja(jogador):
    armas = [
        ("Espada", 5, 40),
        ("Machado", 8, 60),
        ("Arco", 6, 50)
    ]

    while True:
        print("\nLOJA")
        print("1 - Pocao (20 ouro)")
        print("2 - Comprar arma")
        print("0 - Voltar")

        escolha = input("Escolha: ")

        if escolha == "0":
            break

        elif escolha == "1":
            if jogador.ouro >= 20:
                jogador.ouro -= 20
                jogador.pocoes += 1
                print("Pocao comprada")
            else:
                print("Ouro insuficiente")

        elif escolha == "2":
            while True:
                print("\nARMAS")
                for i, arma in enumerate(armas):
                    print(f"{i+1} - {arma[0]} (+{arma[1]}) - {arma[2]} ouro")
                print("0 - Voltar")

                op = input("Escolha: ")

                if op == "0":
                    break

                op = int(op) - 1
                if 0 <= op < len(armas):
                    nome, bonus, preco = armas[op]
                    if jogador.ouro >= preco:
                        jogador.ouro -= preco
                        jogador.arma = Arma(nome, bonus)
                        print(f"Equipou {nome}")
                    else:
                        print("Ouro insuficiente")


# =========================
# JOGO
# =========================
print("RPG DE TEXTO")

nome = input("Nome: ")

print("1-Guerreiro 2-Mago 3-Arqueiro")
op = input("Classe: ")

classe = "Guerreiro" if op == "1" else "Mago" if op == "2" else "Arqueiro"
jogador = Personagem(nome, classe)

rodada = 1

while jogador.esta_vivo():
    print(f"\nRodada {rodada}")

    inimigo = Chefao() if rodada == 5 else gerar_inimigo()

    while inimigo.esta_vivo() and jogador.esta_vivo():
        jogador.mostrar_status()
        inimigo.mostrar_status()

        print("\n1-Atacar 2-Esquivar 3-Habilidade 4-Pocao 0-Menu")
        acao = input("Escolha: ")

        if acao == "0":
            loja(jogador)
            continue
        elif acao == "1":
            jogador.atacar(inimigo)
        elif acao == "2":
            jogador.esquivar()
        elif acao == "3":
            jogador.habilidade(inimigo)
        elif acao == "4":
            jogador.usar_pocao()

        if inimigo.esta_vivo():
            inimigo.agir(jogador)

    if jogador.esta_vivo():
        print(f"Venceu {inimigo.nome}")

        ouro = random.randint(20, 40)
        xp = random.randint(20, 40)

        jogador.ouro += ouro
        jogador.ganhar_xp(xp)

        print(f"Ganhou {ouro} ouro e {xp} XP")

        loja(jogador)

        if rodada == 5:
            print("Voce venceu o jogo")
            break

    rodada += 1

print("Fim de jogo")