from tkinter import *
window = Tk()
window.title('Tính toán')
window.geometry('320x480+400+200')
lbl = Label(window, text="")
lbl.place(x=150, y=90, anchor="center")

#Tạo một Textbox
txta = Entry(window,width=10)
txta.place(x=60, y=30)
txtb = Entry(window,width=10)
txtb.place(x=180, y=30)
def sel():
    if txta.get()=='' and txtb.get()=='':
        lbl.config(text = "Vui lòng nhập đủ giá trị")
    else:
        if var.get()==1:
            lbl.config(text = float(txta.get())+float(txtb.get()))
        if var.get()==2:
            lbl.config(text = float(txta.get())-float(txtb.get()))
        if var.get()==3:
            lbl.config(text = float(txta.get())*float(txtb.get()))
        if var.get()==4:
            if txtb.get()=='0':
                lbl.config(text = "Vui lòng nhập b khác 0")
            else:
                lbl.config(text = float(txta.get())/float(txtb.get()))
    

var = IntVar()
R1 = Radiobutton(window, text="Cộng", variable=var, value=1,command=sel)
R1.place(x=30, y=100)
R2 = Radiobutton(window, text="Trừ", variable=var, value=2,command=sel)
R2.place(x=90, y=100)
R3 = Radiobutton(window, text="Nhân", variable=var, value=3,command=sel)
R3.place(x=150, y=100)
R4 = Radiobutton(window, text="Chia", variable=var, value=4,command=sel)
R4.place(x=210, y=100)

window.mainloop()