import json
import os.path
import shutil
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path

import subprocess
import sys

# Função para instalar um pacote usando pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Verificar se pip está instalado
try:
    import pip
except ImportError:
    install("pip")

# Verificar se Pillow está instalado
try:
    from PIL import Image
except ImportError:
    install("Pillow")

# Agora você pode usar a biblioteca Pillow

#Classe com variaveis de Controle
class control:
    def __init__(self):
        self.index = 0
        self.dist = 85
        self.alterar = False
        self.add = False
        self.image_adress = ""
        self.dados = []
#funçã para ir paro o proximl index
    def prox(self):
        size = len(controle.dados)
        if((self.index + 1) == size):
            pass
        else:
            self.index = self.index + 1
#função pra ir pro index anterior
    def ant(self):
        if((self.index - 1) < 0):
            pass
        else:
            self.index = self.index - 1
#muda o index
    def set_index(self,index):
        self.index = index
#reinicia a contagem de distancia
    def set_distance(self):
        self.dist = 85
#troca o valor da variavel de adicionar
    def add_val(self):
        if (self.add == True):
            self.add = False
        else:
            self.add = True
#troca o valor da varivel de alterar
    def alter_val(self):
        if(self.alterar == True):
            self.alterar = False
        else:
            self.alterar = True

#Iniciazar variaveis de controle
controle = control()

#Função para avançar a imagem
def proxima_img():
    controle.prox()
    display_data()

##Função para retroceder a imagem
def anterior_img():
    controle.ant()
    display_data()

#mostra os dados armazenados no arquivo json
def display_data():
        try:
            with open(data_path, 'r') as data:
                dados = json.load(data)
        except json.JSONDecodeError:
            with open(data_path, 'r') as data:
                file = data.read()
            if not file:
                messagebox.showinfo("ERRO","Não há dados no arquivo")
            else:
                messagebox.showinfo("ERRO", "Ocorreu um erro inesperado")
            return
        select_prod()
        if not(controle.dados):
            return
        #esconder labels e outros:
        frame_opt.place_forget()
        show_data.place_forget()
        add_biju.place_forget()
        flor_label.pack_forget()
        img_select.place_forget()
        confirm_adicionar.place_forget()
        for i in lista_entry:
            i.place_forget()
        #colocar labels que vão ser usados:
        frame_img.place(x=50, y=170)
        voltar.place(x=200, y=600)
        ant.place(x=150, y=600)
        prox.place(x=300, y=600)
        frame_info.place(x=600, y=200)
        #ativar o botão de proximo e anterior
        prox.config(state=NORMAL)
        ant.config(state=NORMAL)
        #desativa botão de backup
        backup_b.config(state=DISABLED)
        #coloca as informações no label
        for i in lista_info:
            i.place(x=20,y=controle.dist)
            controle.dist += 100
        controle.set_distance()
        alter_button.place(x=725, y=625)
        #colocar a imagem do index atual:
        image_path = os.path.abspath(controle.dados[controle.index].get('IMG'))
        image_size = Image.open(image_path)
        image_size = image_size.resize((400,400))
        brinco_img = ImageTk.PhotoImage(image_size)
        label_img.config(image=brinco_img)
        label_img.image = brinco_img
        #exibir dados do index atual:
        cod.config(text="CODIGO: " + controle.dados[controle.index].get("COD"))
        price.config(text="PREÇO: " + str(controle.dados[controle.index].get("PRICE")))
        quant.config(text="QUANTIDADE: " + str(controle.dados[controle.index].get("QUANT")))


#usado para alterar dados no arquivo json
def alterar():
    #desativar os botões de pesquisa e navegação
    search.config(state=DISABLED)
    prox.config(state=DISABLED)
    ant.config(state=DISABLED)
    aplicar_b.config(state=DISABLED)
    alter_button.place_forget()
    confirm_alter.place(x=725, y=625)
    img_select.place(x=185, y=135)
    #remove as infomações dos labels de Info:
    cod.config(text="CODIGO:")
    price.config(text="PREÇO:")
    quant.config(text="QUANTIDADE:")
    #remove as informções e coloca os entrys:
    for i in lista_entry:
        i.delete(0, 'end')
        i.place(x=200, y=controle.dist)
        controle.dist += 100
    controle.set_distance()
    # adiciona os valores do indexes atuais
    cod_entry.insert(0, controle.dados[controle.index].get("COD"))
    price_entry.insert(0, controle.dados[controle.index].get("PRICE"))
    quant_entry.insert(0, controle.dados[controle.index].get("QUANT"))


#função para adicionar novos dados:
def add_dados():
    #desativa botão de backup
    backup_b.config(state=DISABLED)
    #Desmarca todos os radios
    opt_v.set(None)
    #remove os labels que não seram usados
    show_data.place_forget()
    add_biju.place_forget()
    flor_label.pack_forget()
    # colocar labels e botões que vão ser usados:
    frame_opt.place(x=670,y=170)
    frame_img.place(x=50, y=170)
    voltar.place(x=200, y=600)
    frame_info.place(x=600, y=200)
    img_select.place(x=185, y=135)
    confirm_adicionar.place(x=725, y=625)
    #remove as infomações dos labels de Info:
    cod.config(text="CODIGO:")
    price.config(text="PREÇO:")
    quant.config(text="QUANTIDADE:")
    #zerar as entrys e posicionar os labels e entrys de info
    for i in range(0,len(lista_entry)):
        lista_entry[i].delete(0, 'end')
        lista_entry[i].place(x=200, y=controle.dist)
        lista_info[i].place(x=20, y=controle.dist)
        controle.dist += 100
    controle.set_distance()
    #remover imagem
    label_img.config(image=empty_img)
    label_img.image = empty_img

#salva as alterações
def confirmar_alterar():
    try:
        price = float(price_entry.get())
        quant = int(quant_entry.get())
    except ValueError:
        messagebox.showinfo("ERRO","O preço e a quantidade devem ser um número")
        return
    with open(data_path) as data:
        dados = json.load(data)
        #procura na copia dos dados se há algum código ingual
        print(controle.dados[controle.index])
        if not(controle.dados[controle.index].get('COD') == cod_entry.get().upper()):
            for i in dados:
                if cod_entry.get().upper() == i.get('COD'):
                    messagebox.showwarning("Informe outro código","Já existe um produto com este código!")
                    return
        if not(cod_entry.get() == '' or cod_entry.get() == ' '):
            if controle.image_adress != '':
                save_path = local + "\\produtos_img\\" + cod_entry.get().upper()
                shutil.copy2(controle.image_adress,save_path)
                dict_data = {'COD':cod_entry.get().upper(),'PRICE':price,'QUANT':quant,'IMG':save_path, 'TYPE': controle.dados[controle.index].get("TYPE")}
            else:
                dict_data = {'COD': cod_entry.get().upper(), 'PRICE': price, 'QUANT': quant, 'IMG': controle.dados[controle.index].get('IMG'), "TYPE": controle.dados[controle.index].get('TYPE')}
            with open(data_path, 'w') as new:
                for i in range(0,len(dados)):
                    if controle.dados[controle.index].get("COD") == dados[i].get("COD"):
                        break
                auto_backup(dados)
                dados[i] = dict_data
                new_dados = json.dumps(dados)
                new.write(new_dados)
                confirm_alter.place_forget()
            aplicar_b.config(state=NORMAL)
            controle.image_adress = ''
            search.config(state=NORMAL)
            display_data()
        else:
            messagebox.showinfo("Informe um código","O área de código não pode estar vazia")
            return

def auto_backup(data):
    if not(data == '' or data == ' '):
        with open(autobackup_path, 'w') as new:
            new.write(json.dumps(data))

def backup():
    with open(data_path, 'r') as data:
        try:
            dados = json.load(data)
        except json.JSONDecodeError:
            messagebox.showinfo("ERRO","Não há dados no arquivo para serem salvos")
            return
        with open(backup_path, 'w') as new:
            new.write(json.dumps(dados))

def confirmar_add():
    dict_data = {}
    if opt_v.get() == "None" or opt_v.get() == "":
        messagebox.showinfo("Marque uma Opção","Escolha um tipo de produto")
        return
    try:
        with open(data_path, 'r') as data:
            dados = json.load(data)
            price = float(price_entry.get())
            quant = int(quant_entry.get())
            if not (cod_entry.get() == '' or cod_entry.get() == ' '):
                for i in dados:
                    if i.get('COD') == cod_entry.get().upper():
                        messagebox.showerror("ERRO","Já existe um produto com este codigo")
                        #remover imagem
                        label_img.config(image=empty_img)
                        label_img.image = empty_img
                        return
                if controle.image_adress != '':
                    save_path = local + "\\produtos_img\\" + cod_entry.get().upper()
                    shutil.copy2(controle.image_adress, save_path)
                    dict_data = {'COD': cod_entry.get().upper(), 'PRICE': price, 'QUANT': quant, 'IMG': save_path, "TYPE": opt_v.get()}
                    auto_backup(dados)
                    dados.append(dict_data)
                    with open(data_path, 'w') as new:
                        new_dados = json.dumps(dados)
                        new.write(new_dados)
                        messagebox.showinfo("Sucesso","Os dados foram salvos")
                        add_dados()
                else:
                    messagebox.showerror("ERRO","ESCOLHA IMAGEM!")
                    return
            else:
                messagebox.showinfo("Informe um código","O área de código não pode estar vazia")
                return
    except json.JSONDecodeError:
        with open(data_path, 'r') as data:
            file = data.read()
            if not file:
                with open(data_path, 'w') as new:
                    try:
                        price = float(price_entry.get())
                        quant = int(quant_entry.get())
                    except ValueError:
                        messagebox.showinfo("ERRO","O preço e a quantidade não podem estar vazios e devem ser um número")
                        return
                    if not (cod_entry.get() == '' or cod_entry.get() == ' '):
                        if controle.image_adress != '':
                            save_path = local + "\\produtos_img\\" + cod_entry.get().upper()
                            shutil.copy2(controle.image_adress, save_path)
                            dict_data = {'COD': cod_entry.get().upper(), 'PRICE': price, 'QUANT': quant,
                                         'IMG': save_path, "TYPE": opt_v.get()}
                            list = [dict_data]
                            new_dados = json.dumps(list)
                            new.write(new_dados)
                            messagebox.showinfo("Sucesso", "Os dados foram salvos")
                            add_dados()
                        else:
                            messagebox.showerror("ERRO", "ESCOLHA UMA IMAGEM!")
                            return
                    else:
                        messagebox.showinfo("Informe um código","O área de código não pode estar vazia")
                        return
    except ValueError:
        messagebox.showinfo("ERRO","O preço e a quantidade não podem estar vazios e devem ser um número")
    finally:
        controle.image_adress = ''

def select_img():
    formats = ['png','peg','jpg']
    controle.image_adress = ''
    img_path = filedialog.askopenfilename()
    img_test = img_path[-3:]
    if not(img_test in formats):
        messagebox.showinfo("ERRO","Selecione um arquivo valido: png, jpg ou jpeg")
        controle.image_adress = ''
        return
    controle.image_adress = img_path
    brinco_img = Image.open(img_path)
    brinco_img = brinco_img.resize((400,400))
    brinco_img = ImageTk.PhotoImage(brinco_img)
    label_img.config(image=brinco_img)
    label_img.image = brinco_img

def aply_filter():
    mark_var = var1.get() + var2.get() + var3.get()
    if mark_var == 0:
        messagebox.showwarning("Escolha um Produto","Você deve marcar ao menos um produto")
    else:
        messagebox.showinfo("Sucesso","Os filtros foram aplicados")
    if img_select.winfo_ismapped() or show_data.winfo_ismapped():
        return
    else:
        controle.set_index(0)
        display_data()

def select_prod():
    lista_dados = []
    mark_var = var1.get() + var2.get() + var3.get()
    try:
        with open(data_path, 'r') as data:
            dados = json.load(data)
    except json.JSONDecodeError:
        return
    if mark_var == 3:
        controle.dados = dados
    elif mark_var == 0:
        messagebox.showwarning("Escolha um Produto","Você deve marcar ao menos um produto")
        controle.dados = []
        return
    elif mark_var == 2:
        #caso bijuterias esteja desmarcado
        if var1.get() == 0:
            for i in dados:
                if i.get("TYPE") == 'C' or i.get("TYPE") == 'R':
                    lista_dados.append(i)
            if not(lista_dados):
                messagebox.showinfo("Não encontrado","Não existem produtos do tipo chinelo e Relogio")
                controle.dados = []
                return
            else:
                controle.dados = lista_dados
        #caso chinelo esteja desmarcado
        if var2.get() == 0:
            for i in dados:
                if i.get("TYPE") == 'B' or i.get("TYPE") == 'R':
                    lista_dados.append(i)
            if not(lista_dados):
                messagebox.showinfo("Não encontrado","Não existem produtos do tipo Bijuterias e Relogio")
                controle.dados = []
                return
            else:
                controle.dados = lista_dados
        #caso relogio esteja desmarcado
        if var3.get() == 0:
            for i in dados:
                if i.get("TYPE") == 'C' or i.get("TYPE") == 'B':
                    lista_dados.append(i)
            if not(lista_dados):
                messagebox.showinfo("Não encontrado","Não existem produtos do tipo Bijuteria e Chinelo")
                controle.dados = []
                return
            else:
                controle.dados = lista_dados
    else:
        if var1.get() == 1:
            for i in dados:
                if i.get("TYPE") == 'B':
                    lista_dados.append(i)
            if not(lista_dados):
                messagebox.showinfo("Não encontrado","Não existem produtos do tipo Bijuterias")
                controle.dados = []
                return
            else:
                controle.dados = lista_dados
        elif var2.get() == 1:
            for i in dados:
                if i.get("TYPE") == 'C':
                    lista_dados.append(i)
            if not(lista_dados):
                messagebox.showinfo("Não encontrado","Não existem produtos do tipo Chinelo")
                controle.dados = []
                return
            else:
                controle.dados = lista_dados
        else:
            for i in dados:
                if i.get("TYPE") == 'R':
                    lista_dados.append(i)
            if not(lista_dados):
                messagebox.showinfo("Não encontrado","Não existem produtos do tipo Relogio")
                controle.dados = []
                return
            else:
                controle.dados = lista_dados

#Função para procurar por um produto
def procurar():
    try:
        with open(data_path,'r') as data:
            dados = json.load(data)
    except json.JSONDecodeError:
        messagebox.showinfo("ERRO","O arquivo está vazio")
        return
    select_prod()
    if not(controle.dados):
        return
    if barra.get() == "":
        messagebox.showwarning("Vazio","Informe um valor válido")
        return
    search = barra.get().upper()
    for i in range(0,len(controle.dados)):
        if dados[i].get("COD") == search:
            controle.set_index(i)
            display_data()
            return
    if True:
        messagebox.showinfo("NOT FOUND","Não foi encontrado")

def retroceder():
    #zera  a variavel de endereço de imagens
    controle.image_adress = ''
    #recolocar os labels:
    show_data.place(x=50,y=150)
    add_biju.place(x=50,y=400)
    flor_label.pack(side=RIGHT)
    #ativar o botão de pesquisa, aplicar e realizar backup
    search.config(state=NORMAL)
    aplicar_b.config(state=NORMAL)
    backup_b.config(state=NORMAL)
    #remover os labels:
    frame_opt.pack_forget()
    frame_img.place_forget()
    voltar.place_forget()
    ant.place_forget()
    confirm_adicionar.place_forget()
    confirm_alter.place_forget()
    prox.place_forget()
    alter_button.place_forget()
    frame_info.place_forget()
    img_select.place_forget()
    for i in lista_entry:
        i.place_forget()
    if(controle.alterar == True):
        controle.alter_val()
    if(controle.add == True):
        controle.add_val()
    controle.index = 0

#Variaveis de localização de arquivos de dados
local = str(Path.cwd())
data_path = local + "\\dados.json"
autobackup_path = local + "\\auto_backup.json"
backup_path = local + '\\backup.json'

#Configurações da Janelapyinstaller --onefile --noconsole imp.py
janela = Tk()
janela.geometry("1024x720")
janela.resizable(False,False)
janela.title("BANCO DE DADOS")
janela.config(background="yellow")

#Botão de pesquisa
search = Button(janela,text="Procurar",width=10,command=procurar)

#Painel de filtros de display
display_filter = Frame(janela,width=150,background="yellow")

#Botão para aplicar filtros
aplicar_b = Button(display_filter,text="Aplicar",command=aply_filter)

#label para as opções de display
display_label = Label(display_filter,text="Exibir:",background="yellow").grid(row=0,column=0)

#variaveis usadas pra armazenar valores dos filtros
var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()

#Filtros
c1 = Checkbutton(display_filter,text="Bijuterias",variable=var1,onvalue=1,offvalue=0,background="yellow")
c2 = Checkbutton(display_filter,text="Roupas",variable=var2,onvalue=1,offvalue=0,background="yellow")
c3 = Checkbutton(display_filter,text="Relogios",variable=var3,onvalue=1,offvalue=0,background="yellow")
list_check = [c1,c2,c3]
#criando os check buttons
coluna = 1
for i in list_check:
    i.grid(row=0,column=coluna)
    coluna += 1

#Botão de exibir img
show_data = Button(janela,text="Produtos",font=("arial",12),width=50,height=10,command=display_data)

#Botão para adicionar novos dados
add_biju = Button(janela,text="Adicionar",font=("arial",12),width=50,height=10,command=add_dados)

#Frame para as opções
frame_opt = Frame(janela,width=300,height=100,background="black")

#Variavel do radio de opções
opt_v = tk.StringVar()

#Opções de tipo de produto
opt_dict = {"Bijuterias":"B",
            "Roupas":"C",
            "Relogios":"R"}

#criando dos radios de opção 
coluna = 0
for (key,value) in opt_dict.items():
    opt_add = Radiobutton(frame_opt,text=key,variable=opt_v,value=value).grid(row=0,column=coluna)
    coluna += 1

#Botão para alterar dados
alter_button = Button(janela,text="Alterar Dados",font=("arial",12),width=15,command=alterar)

#Botão para fazer backup manual
backup_b = Button(janela,text="Fazer Backup",font=("arial",8),width=10,command=backup)

#Botão pra confirmar as alterações
confirm_alter = Button(janela,text="Confirmar",font=("arial",12),width=10,command=confirmar_alterar)
confirm_adicionar = Button(janela,text="Confirmar",font=("arial",12),width=10,command=confirmar_add)
#Botão de mudar a imagem
img_select = Button(janela,text="Selecionar Imagem",font=("arial",10),width=15,command=select_img)

#Botão de Avançar ou regredir a imagem
prox = Button(janela,text=">>",command=proxima_img)
ant = Button(janela,text="<<",command=anterior_img)

#Botão para voltar
voltar = Button(janela,text="Voltar",command=retroceder,width=10)

#Frame para imagens
frame_img = Frame(janela,width=400,height=400,pady=0,padx=0)

#Frame para Informações
frame_info = Frame(janela,width=350,height=400,background="black")

#Label para imagens
label_img = Label(frame_img)
label_img.pack()

#Label para informações
cod = Label(frame_info,text="CODIGO:",font=("consolas",12))
price = Label(frame_info,text="PREÇO:",font=("consolas",12))
quant = Label(frame_info,text="QUANTIDADE:",font=("consolas",12))
#armazena os labes em um List para iterar
lista_info = [cod,price,quant]

#Barra de Pesquisa
barra = Entry(janela,width=150)

#Area para entrar informações
cod_entry = Entry(frame_info, width=20)
price_entry = Entry(frame_info, width=20)
quant_entry = Entry(frame_info, width=20)
#armazena os entrys em um List para iterar
lista_entry = [cod_entry,price_entry,quant_entry]

#imagens decorativas
flor_arq = local +"\\flor.png"
flor_img = Image.open(flor_arq)
flor_img = ImageTk.PhotoImage(flor_img)
flor_label = Label(janela,width=400,height=400,bg="yellow",highlightthickness=0,image=flor_img)

#imagem do icone
icon = Image.open(local + "\\ksenso_icon.jpg")
icon = ImageTk.PhotoImage(icon)
janela.iconphoto(False,icon)

#Empty image
empty_img = Image.open(local + "\\empty.jpg")
empty_img = empty_img.resize((400,400))
empty_img = ImageTk.PhotoImage(empty_img)

#marcar os checkboxes
var1.set(1)
var2.set(1)
var3.set(1)
#desmarcar os radios
opt_v.set(None)

#Place
barra.place(x=24,y=25)
show_data.place(x=50,y=150)
search.place(x=940,y=21)
display_filter.place(x=20,y=50)
flor_label.pack(side=RIGHT)
add_biju.place(x=50,y=400)
aplicar_b.grid(row=0,column=4)
backup_b.place(x=950,y=690)

janela.mainloop()