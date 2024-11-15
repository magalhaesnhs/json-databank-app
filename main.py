import json
import os.path
import shutil
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
#funçã para ir paro o proximl index
    def prox(self):
        with open(data_path,'r') as data:
            dados = json.load(data)
            size = len(dados)
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
        #esconder labels e outros:
        show_data.place_forget()
        add_biju.place_forget()
        flor_label.pack_forget()
        img_select.place_forget()
        for i in lista_entry:
            i.place_forget()
        #colocar labels que vão ser usados:
        frame_img.place(x=50, y=100)
        voltar.place(x=200, y=600)
        ant.place(x=150, y=600)
        prox.place(x=300, y=600)
        frame_info.place(x=600, y=200)
        #ativar o botão de proximo e anterior
        prox.config(state=NORMAL)
        ant.config(state=NORMAL)
        #coloca as informações no label
        for i in lista_info:
            i.place(x=20,y=controle.dist)
            controle.dist += 100
        controle.set_distance()
        alter_button.place(x=725, y=625)
        #colocar a imagem do index atual:
        image_path = os.path.abspath(dados[controle.index].get('IMG'))
        image_size = Image.open(image_path)
        image_size = image_size.resize((400,400))
        brinco_img = ImageTk.PhotoImage(image_size)
        label_img.config(image=brinco_img)
        label_img.image = brinco_img
        #exibir dados do index atual:
        cod.config(text="CODIGO: " + dados[controle.index].get("COD"))
        price.config(text="PREÇO: " + str(dados[controle.index].get("PRICE")))
        quant.config(text="QUANTIDADE: " + str(dados[controle.index].get("QUANT")))


#usado para alterar dados no arquivo json
def alterar():
    prox.config(state=DISABLED)
    ant.config(state=DISABLED)
    alter_button.place_forget()
    confirm_alter.place(x=725, y=625)
    img_select.place(x=185, y=65)
    #desativar o botão de pesquisa
    search.config(state=DISABLED)
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
    with open(data_path, 'r') as data:
        dados = json.load(data)
        # adiciona os valores do indexes atuais
        cod_entry.insert(0, dados[controle.index].get("COD"))
        price_entry.insert(0, dados[controle.index].get("PRICE"))
        quant_entry.insert(0, dados[controle.index].get("QUANT"))


#função para adicionar novos dados:
def add_dados():
    show_data.place_forget()
    add_biju.place_forget()
    flor_label.pack_forget()
    # colocar labels e botões que vão ser usados:
    frame_img.place(x=50, y=100)
    voltar.place(x=200, y=600)
    frame_info.place(x=600, y=200)
    img_select.place(x=185, y=65)
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
        quant = float(quant_entry.get())
    except ValueError:
        messagebox.showinfo("ERRO","O preço e a quantidade devem ser um número")
        return
    with open(data_path) as data:
        dados = json.load(data)
        if not(cod_entry.get() == '' or cod_entry.get() == ' '):
            if controle.image_adress != '':
                save_path = local + "\\brinco_images\\" + cod_entry.get()
                shutil.copy2(controle.image_adress,save_path)
                dict_data = {'COD':cod_entry.get().upper(),'PRICE':price,'QUANT':quant,'IMG':save_path}
            else:
                dict_data = {'COD': cod_entry.get(), 'PRICE': price, 'QUANT': quant, 'IMG': dados[controle.index].get('IMG')}
            with open(data_path, 'w') as new:
                dados[controle.index] = dict_data
                new_dados = json.dumps(dados)

                new.write(new_dados)
                confirm_alter.place_forget()
            display_data()
            controle.image_adress = ''

def confirmar_add():
    dict_data = {}
    try:
        with open(data_path, 'r') as data:
            dados = json.load(data)
            price = float(price_entry.get())
            quant = float(quant_entry.get())
            if not (cod_entry.get() == '' or cod_entry.get() == ' '):
                for i in dados:
                    if i.get('COD') == cod_entry.get().upper():
                        messagebox.showerror("ERRO","Já existe um produto com este codigo")
                        #remover imagem
                        label_img.config(image=empty_img)
                        label_img.image = empty_img
                        return
                if controle.image_adress != '':
                    save_path = local + "\\brinco_images\\" + cod_entry.get()
                    shutil.copy2(controle.image_adress, save_path)
                    dict_data = {'COD': cod_entry.get().upper(), 'PRICE': price, 'QUANT': quant, 'IMG': save_path}
                    backup(dados)
                    dados.append(dict_data)
                    with open(data_path, 'w') as new:
                        new_dados = json.dumps(dados)
                        new.write(new_dados)
                        messagebox.showinfo("Sucesso","Os dados foram salvos")
                        add_dados()
                else:
                    messagebox.showerror("ERRO","ESCOLHA IMAGEM!")
                    return
    except json.JSONDecodeError:
        with open(data_path, 'r') as data:
            file = data.read()
            if not file:
                with open(data_path, 'w') as new:
                    try:
                        price = float(price_entry.get())
                        quant = float(quant_entry.get())
                    except ValueError:
                        messagebox.showinfo("ERRO","O preço e a quantidade não podem estar vazios e devem ser um número")
                        return
                    if not (cod_entry.get() == '' or cod_entry.get() == ' '):
                        if controle.image_adress != '':
                            save_path = local + "\\brinco_images\\" + cod_entry.get()
                            shutil.copy2(controle.image_adress, save_path)
                            dict_data = {'COD': cod_entry.get().upper(), 'PRICE': price, 'QUANT': quant,
                                         'IMG': save_path}
                            list = [dict_data]
                            new_dados = json.dumps(list)
                            new.write(new_dados)
                            messagebox.showinfo("Sucesso", "Os dados foram salvos")
                            add_dados()
                        else:
                            messagebox.showerror("ERRO", "ESCOLHA UMA IMAGEM!")
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

#Função para procurar por um produto
def procurar():
    search = (barra.get().upper())
    try:
        with open(data_path,'r') as data:
            dados = json.load(data)
    except json.JSONDecodeError:
        messagebox.showinfo("ERRO","O arquivo está vazio")
        return
    for i in range(0,len(dados)):
        if(dados[i].get("COD") == search):
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
    #ativar o botão de pesquisa
    search.config(state=NORMAL)
    #remover os labels:
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

def backup(data):
    if not(data == '' or data == ' '):
        print("asdasd")
        with open(backup_path, 'w') as new:
            new.write(json.dumps(data))

#Variaveis de localização de arquivos de dados
local = str(Path.cwd())
data_path = local + "\\dados.json"
backup_path = local + "\\dados_backup.json"

#Configurações da Janelapyinstaller --onefile --noconsole imp.py
janela = Tk()
janela.geometry("1024x720")
janela.resizable(False,False)
janela.title("BANCO DE DADOS")
janela.config(background="yellow")

#Botão de pesquisa
search = Button(janela,text="Procurar",width=10,command=procurar)


#Botão de exibir img
show_data = Button(janela,text="Produtos",font=("arial",12),width=50,height=10,command=display_data)

#Botão para adicionar novos dados
add_biju = Button(janela,text="Adicionar",font=("arial",12),width=50,height=10,command=add_dados)

#Botão para alterar dados
alter_button = Button(janela,text="Alterar Dados",font=("arial",12),width=15,command=alterar)

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
barra.place(x=24,y=25)

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

#Place
barra.place(x=24,y=25)
show_data.place(x=50,y=150)
search.place(x=940,y=21)
flor_label.pack(side=RIGHT)
add_biju.place(x=50,y=400)

janela.mainloop()