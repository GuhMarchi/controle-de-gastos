import json
import sqlite3


import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def conectar_banco():
    conexao = sqlite3.connect("Controle_de_gastos.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descrição TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL
        )
    """)
    conexao.commit()
    return conexao, cursor


def carregar_gastos():
    try:
        with open("Controle_de_gastos.json" , "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

gastos = carregar_gastos()
conexao, cursor = conectar_banco()


def adicionar_gastos():
    descrição = input("Digite a descrição do gasto: ").strip()
    valor = float(input("Digite o valor do gasto R$: "))
    categoria = input("Digite em qual cateria (Ex: Alimentação, carro, etc.) ele se encaixa: ").strip()
    gastos.append({"Descrição":descrição, "Valor":valor, "Categoria":categoria })
    cursor.execute("INSERT INTO gastos (descrição, valor, categoria) VALUES (?, ?, ?)", (descrição, valor, categoria))
    conexao.commit()
    
def lista_de_gastos():
    for i, gasto in enumerate(gastos):
        print(i + 1, gasto["Descrição"], "R$", gasto["Valor"], gasto["Categoria"])
        
def total_gastos():
    total = 0
    for gasto in gastos:
        total += gasto["Valor"]
    print(f"Total gasto: R$ {total:.2f}")
           
def gastos_por_categoria():
    categorias = {}
    for gasto in gastos:
        categoria = gasto["Categoria"]
        valor = gasto["Valor"]
        
        if categoria in categorias:
            categorias[categoria] += valor
        else:
            categorias[categoria] = valor
    
    for categoria, total in categorias.items():
        print(f"{categoria}: R$ {total:.2f}")
        
def salvar_gastos():
    with open ("Controle_de_gastos.json", "w") as arquivo:
        json.dump(gastos, arquivo)
    print("Gastos salvos!")


        
        
while True:
    print("1 - Adicionar gastos")
    print("2 - Listar gastos")
    print("3 - Total Gastos")
    print("4 - Gastos por Categoria")
    print("5 - Salvar gastos")
    print("6 - Sair ")
    
    opcao = input("Escolha a opção que deseja executar:")
    if opcao == "1":
        adicionar_gastos()
    elif opcao == "2":
        lista_de_gastos()
    elif opcao == "3":
        total_gastos()    
    elif opcao == "4":
        gastos_por_categoria()
    elif opcao == "5":
        salvar_gastos()
    elif opcao == "6":
        salvar_gastos()
        print("Saindo!")
        break
    