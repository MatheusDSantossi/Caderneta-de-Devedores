from tkinter import ttk
from tkinter import *


import sqlite3


class Pessoas:

    db_caderneta = "caderneta_data_base.db"

    def __init__(self, window):

        self.wind = window
        self.wind.geometry("905x500+300+100")
        self.wind.title("Caderneta de Clientes")
        self.wind.configure(bg="black")

        frame = LabelFrame(self.wind, text = "Cadastrar Novo Cliente na Caderneta: ", bg="lightblue", fg="darkgreen",font=("Times New Roman", 20), padx= 10, pady=140)
        frame.grid(row=0, column=0, columnspan=10, pady=0)

        nomeDoC = Label(frame, text="Nome do Cliente: ", bg="lightblue", fg="darkgreen", font=("Times", 15)).grid(row=1, column=0)
        
        self.cliente = Entry(frame, font=10)
        self.cliente.grid(row=1, column=1)

        valorNaC = Label(frame, text="Valor Na Conta: ", bg="lightblue", fg="darkgreen", font=("Times", 15)).grid(row=2, column=0)
        
        self.conta = Entry(frame, font=10)
        self.conta.grid(row=2, column=1)

        adicionar = ttk.Button(frame, text="Novo Cliente", command=self.adding_customer)
        adicionar.grid(row=3, columnspan=2, sticky=W+E)

        self.message = Label(frame, text="", bg="lightblue", fg="red")
        self.message.grid(row=8, column=0)

        self.tree = ttk.Treeview(height=21, column=2)
        self.tree.grid(row=0, column=50, columnspan=3)
        self.tree.heading("#0", text="Cliente", anchor=CENTER)
        self.tree.heading(2, text="Conta", anchor=CENTER)

        deletar = ttk.Button(frame, text="Deletar Cliente", command=self.deleting_customer)
        deletar.grid(row=4, columnspan=2, sticky=W+E)

        editar = ttk.Button(frame, text="Editar", command=self.editing_costumer)
        editar.grid(row=5, columnspan=2, sticky=W+E)


        self.viewing_records()

    def run_query(self, query, paramenters=()):

        with sqlite3.connect(self.db_caderneta) as conn:

            cursor = conn.cursor()
            query_result = cursor.execute(query, paramenters)
            conn.commit()

        return query_result


    def viewing_records(self):

        records = self.tree.get_children()

        for element in records:

            self.tree.delete(element)

        query = "SELECT * FROM clientes ORDER BY cliente DESC"
        db_rows = self.run_query(query)


        for row in db_rows:

            self.tree.insert("", 0, text=row[1], values=row[2])


    def validation(self):

        return len(self.cliente.get()) != 0 and self.conta.get() != 0

        
    def adding_customer(self):

        if self.validation():

            query = "INSERT INTO clientes VALUES(NULL, ?, ?)"
            paramenters = (self.cliente.get(), self.conta.get())
            self.run_query(query, paramenters)
            self.message["text"] = f"CLIENTE {self.cliente.get()} CADASTRADO COM SUCESSO!"

            self.cliente.delete(0, END)
            self.conta.delete(0, END)


        else:

            self.message["text"] = "POR FAVOR PREENCHA OS CAMPOS OBRIGATÓRIOS"

        self.viewing_records()

    def deleting_customer(self):

        self.message["text"] = ""

        try: 

            self.tree.item(self.tree.selection())["text"]

        except IndexError as e:

            self.message["text"] = "POR FAVOR SELECIONAR UM CLIENTE!"
            return

        self.message["text"] = ""
        cliente = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM clientes WHERE cliente=?"
        self.run_query(query, (cliente,))
        self.message["text"] = f"CLIENTE {cliente} DELETADO!"
        
        self.viewing_records()

    def editing_costumer(self):

        self.message["text"] = ""

        try:

            valor = self.tree.item(self.tree.selection())["values"][0]

        except IndexError as e:

            self.message["text"] = "POR FAVOR SELECIONAR UM CADASTRO PARA ATUALIZAR"
            return
        
        cliente = self.tree.item(self.tree.selection())["text"]
        conta_velha = self.tree.item(self.tree.selection())["values"][0]

        self.edit_wind = Toplevel()
        self.edit_wind.title("titulo : EDITAR PRODUTO: ")

        screen_width = self.edit_wind.winfo_screenwidth()
        screen_height = self.edit_wind.winfo_screenheight()

        width = 365
        height = 250

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.edit_wind.geometry("%dx%d+%d+%d" % (width, height, x, y)) 
        # self.edit_wind.resizable(0, 0)

        self.edit_wind.configure(bg = "DarkBlue")

        Label(self.edit_wind, text= " NOME DO CLIENTE ANTIGO: ", bg="WHITE").grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=cliente), state="readonly").grid(row=0, column=2)
        Label(self.edit_wind, text=" DIGITE O NOVO CLIENTE: ", bg="DarkBlue", fg="WHITE").grid(row=1, column=1)

        novo_cliente = Entry(self.edit_wind)
        novo_cliente.grid(row=1, column=2)

        Label(self.edit_wind, text=f"CONTA ANTIGA DO(a) {cliente}: ", bg="WHITE").grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=DoubleVar(self.edit_wind, value=conta_velha), state="readonly").grid(row=2, column=2)
        Label(self.edit_wind, text=f" DIGITE A NOVA CONTA DO(a) {conta_velha}", bg="DarkBlue", fg="WHITE").grid(row=3, column=1)

        conta_nova = Entry(self.edit_wind)
        Label(self.edit_wind, text=f"a {conta_nova.get()}", bg="WHITE").grid(row=5, column=1)
        # if conta_nova:
        #     texto = conta_nova.get()
        #     numero = str(texto)
        #     conta_somada = numero + str(conta_velha)
        
        conta_nova.grid(row=3, column=2)

        button = Button(self.edit_wind, bd=2, text=f"EDITAR CLIENTE ", bg="black", fg="yellow", command=lambda:self.edit_records(novo_cliente.get(), conta_nova.get(), cliente, conta_velha)).grid(row=5, column=1, sticky=W)
        self.edit_wind.mainloop()


    def edit_records(self, cliente, conta_nova, cliente_velho, conta_velha):

        query = "UPDATE clientes SET cliente=?, conta=? WHERE cliente=? AND conta=?"
        paramenters = (cliente, conta_nova, cliente_velho, conta_velha)

        self.run_query(query, paramenters)
        self.edit_wind.destroy()
        self.message["text"] = f"CADASTRO {cliente_velho} EDITADO COM SUCESSO!"
        self.viewing_records()
            
    
if __name__ == "__main__":

    window = Tk()
    application = Pessoas(window)
    window.mainloop()

    # nomes = open("nomes_salvos", "w")

    # nomes.write(nome_cliente)

    # nomes.close()



