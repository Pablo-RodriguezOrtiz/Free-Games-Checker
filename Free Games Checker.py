##--------------------------------------------------
##
## Python Version 3.9.5
##
##--------------------------------------------------
import requests
import tkinter as tk
from tkinter import ttk
import webbrowser
from functools import partial

class myapp(): #Create "myapp" class to tkinter windows.
    def __init__(self):
        self.app=tk.Tk()
        self.app.title('Free Games Checker')
        self.app.geometry('850x610')
        self.app.resizable(False, False)

        self.labelplataforma=tk.Label(self.app,text="Plataform: ").grid(row=0,column=0, sticky=tk.W, padx=25)
        self.plataforma=ttk.Combobox(self.app,state='readonly')
        self.plataforma.grid(row=0, column=0,pady=10, padx=35)
        self.plataforma["values"]=["PC","Steam","Xbox-One","PS4","Nintendo Switch","Android","iOS"]
        self.plataforma.current(0)

        self.fullcheck=tk.IntVar()
        self.solofull=tk.Checkbutton(self.app, text="Only FULL Games",variable=self.fullcheck, onvalue=1, offvalue=0)
        self.solofull.grid(row=0, column=1, pady=10)

        self.boton_buscar=tk.Button(self.app,text="Search for FREE Games", command=self.listar_juegos)
        self.boton_buscar.grid(row=0, column=3,pady=10)

        self.framejuegos=tk.Frame(self.app,background='white',width=900, height=475)
        self.framejuegos.grid(row=2, column=0, columnspan=4, padx=25, pady=30)

        self.canvas=tk.Canvas(self.framejuegos, width=780, height=475)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.scroll=tk.Scrollbar(self.framejuegos, orient='vertical', command=self.canvas.yview)
        self.scroll.grid(row=0, column=1, ipady=213)

        self.framejuegos2=tk.Frame(self.canvas)
        self.framejuegos2.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0,0), window=self.framejuegos2, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.titulo=tk.Label(self.framejuegos2, text='Title',background='white',relief='raised', width=42).grid(row=0,column=0,sticky='NSWE')
        self.fecha=tk.Label(self.framejuegos2, text='Published Date',background='white',relief='raised', width=15).grid(row=0,column=1,sticky='NSWE')
        self.tipo=tk.Label(self.framejuegos2, text='Type',background='white',relief='raised', width=10).grid(row=0,column=2,sticky='NSWE')
        self.instrucciones=tk.Label(self.framejuegos2, text='Instructions',background='white',relief='raised', width=15).grid(row=0,column=3,sticky='NSWE')
        self.descarga=tk.Label(self.framejuegos2, text='Link',background='white',relief='raised',width=15).grid(row=0,column=4,sticky='NSWE')

        self.creditos=tk.Label(self.app, text='Created by Pablo Rodríguez using GamerPower.com API\t\t Version 1.0', foreground='grey', font=('Arial',8)).grid(row=3, column=0)

        self.app.mainloop()

    def _on_mousewheel(self, event): #Function to check mouse wheel for scroll.
        self.canvas.yview_scroll(-1*(event.delta/120), "units")
        self.framejuegos2.bind('<Enter>', self._bound_to_mousewheel)
        self.framejuegos2.bind('<Leave>', self._unbound_to_mousewheel)

        return None

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def buscar_juegos(self): #Function to obtain and create a data .json file with all games giveaway info. It checks user platform selection.
        if self.plataforma.get()=="PC":
            free_games_api="https://www.gamerpower.com/api/giveaways?platform=pc"
            data=requests.get(free_games_api)
            return data.json()
        elif self.plataforma.get()=="Steam":
            free_games_api="https://www.gamerpower.com/api/giveaways?platform=steam"
            data=requests.get(free_games_api)
            return data.json()
        elif self.plataforma.get()=="Xbox-One":
            free_games_api="https://www.gamerpower.com/api/giveaways?platform=xbox-one"
            data=requests.get(free_games_api)
            return data.json()
        elif self.plataforma.get()=="PS4":
            free_games_api="https://www.gamerpower.com/api/giveaways?platform=ps4"
            data=requests.get(free_games_api)
            return data.json()
        elif self.plataforma.get()=="Nintendo Switch":
            free_games_api="https://www.gamerpower.com/api/giveaways?platform=switch"
            data=requests.get(free_games_api)
            return data.json()
        elif self.plataforma.get()=="Android":
            free_games_api="https://www.gamerpower.com/api/giveaways?platform=android"
            data=requests.get(free_games_api)
            return data.json()
        elif self.plataforma.get()=="iOS":
            free_games_api="https://www.gamerpower.com/api/giveaways?platform=ios"
            data=requests.get(free_games_api)
            return data.json()

    def listar_juegos(self): #Function to create a free game list using for and the last function.
        self.games=self.buscar_juegos()
        listado=self.framejuegos2.grid_slaves()
        for i in range(len(listado)): #This for destroys the list everytime user checks for new games.
            if isinstance(listado[i],tk.Entry) or isinstance(listado[i], tk.Button):
                listado[i].destroy()
        if self.fullcheck.get()==1: #If Full Games Only check is active, only displays full game giveaways.
            for k in range(len(self.games)):
                if self.games[k]['type']=="Full Game":
                    a=tk.Entry(self.framejuegos2, relief='groove', background='white')
                    a.grid(row=k+1, column=0, sticky='NSWE')
                    a.insert(0,self.games[k]['title'])
                    a.configure(state='readonly')

                    e=tk.Entry(self.framejuegos2, relief='groove', background='white')
                    e.grid(row=k+1, column=1, sticky='NSWE')
                    e.insert(0,self.games[k]['published_date'])
                    e.configure(state='readonly')

                    i=tk.Entry(self.framejuegos2, relief='groove', background='white')
                    i.grid(row=k+1, column=2, sticky='NSWE')
                    i.insert(0,self.games[k]['type'])
                    i.configure(state='readonly')

                    o=tk.Button(self.framejuegos2, text='More info', background='white',command=partial(self.mas_info,self.games[k]['description'],self.games[k]['instructions']), cursor='hand2')
                    o.grid(row=k+1, column=3, sticky='NSWE')

                    u=tk.Button(self.framejuegos2,text="Get Game!", background='white',command=partial(self.abrir_link,self.games[k]['open_giveaway_url']), cursor='hand2')
                    u.grid(row=k+1, column=4, sticky='NSWE')
        else:
            for k in range(len(self.games)):
                a=tk.Entry(self.framejuegos2, relief='groove', background='white')
                a.grid(row=k+1, column=0, sticky='NSWE')
                a.insert(0,self.games[k]['title'])
                a.configure(state='readonly')

                e=tk.Entry(self.framejuegos2, relief='groove', background='white')
                e.grid(row=k+1, column=1, sticky='NSWE')
                e.insert(0,self.games[k]['published_date'])
                e.configure(state='readonly')

                i=tk.Entry(self.framejuegos2, relief='groove', background='white')
                i.grid(row=k+1, column=2, sticky='NSWE')
                i.insert(0,self.games[k]['type'])
                i.configure(state='readonly')

                o=tk.Button(self.framejuegos2, text='More info', background='white',command=partial(self.mas_info,self.games[k]['description'],self.games[k]['instructions']), cursor='hand2')
                o.grid(row=k+1, column=3, sticky='NSWE')

                u=tk.Button(self.framejuegos2,text="Get Game!", background='white',command=partial(self.abrir_link,self.games[k]['open_giveaway_url']), cursor='hand2')
                u.grid(row=k+1, column=4, sticky='NSWE')

    def abrir_link(self,info): #Function to open game link.
        webbrowser.open(info)
    
    def mas_info(self, info, instruccion): #Function to create a little popup with information and instructions.
        self.popup=tk.Toplevel()
        self.popup.title("More information and instructions")
        self.popup.resizable(True, True)
        self.popup.geometry("800x400")

        self.info=tk.Message(self.popup, text=info, width=800).grid(row=0, column=0, sticky='NSWE', pady=25, padx=5)
        self.labelinst=tk.Label(self.popup, text='Instructions:\n').grid(row=1, column=0)
        self.intrucc=tk.Message(self.popup, text=instruccion, width=800).grid(row=2, column=0)

if __name__=='__main__':
    app=myapp()
