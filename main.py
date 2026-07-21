from tkinter import * 
import platform
import subprocess
from tkinter import messagebox
import random,os,tempfile,smtplib

#?functionality
#!Clear Button Function
def clear():
    bathsoapEntry.delete(0,END)
    facecreamEntry.delete(0,END)
    facewashEntry.delete(0,END)
    hairsprayEntry.delete(0,END)
    hairgelEntry.delete(0,END)
    bodylotionEntry.delete(0,END)

    riceEntry.delete(0,END)
    oilEntry.delete(0,END)
    coffeeEntry.delete(0,END)
    teaEntry.delete(0,END)
    sugarEntry.delete(0,END)
    wheatEntry.delete(0,END)

    maazaEntry.delete(0,END)
    pepisEntry.delete(0,END)
    dewEntry.delete(0,END)
    fantaEntry.delete(0,END)
    cokeEntry.delete(0,END)
    spriteEntry.delete(0,END)

    bathsoapEntry.insert(0,0)
    facecreamEntry.insert(0,0)
    facewashEntry.insert(0,0)
    hairsprayEntry.insert(0,0)
    hairgelEntry.insert(0,0)
    bodylotionEntry.insert(0,0)

    riceEntry.insert(0,0)
    oilEntry.insert(0,0)
    coffeeEntry.insert(0,0)
    teaEntry.insert(0,0)
    sugarEntry.insert(0,0)
    wheatEntry.insert(0,0)

    maazaEntry.insert(0,0)
    pepisEntry.insert(0,0)
    dewEntry.insert(0,0)
    fantaEntry.insert(0,0)
    cokeEntry.insert(0,0)
    spriteEntry.insert(0,0)

    cosmetictaxEntry.delete(0,END)
    grocerytaxEntry.delete(0,END)
    drinkstaxEntry.delete(0,END)

    costmeticpriceEntry.delete(0,END)
    grocerypriceEntry.delete(0,END)
    drinkspriceEntry.delete(0,END)

    nameEntry.delete(0,END)
    phoneEntry.delete(0,END)
    billnumberEntry.delete(0,END)

    textarea.delete(1.0,END)



#*Send Email Function
def send_email():
    def send_gmail():
        try:
            ob=smtplib.SMTP('smtp.gmail.com',587)
            ob.starttls()
            ob.login(senderEntry.get(),passwordEntry.get())
            message=email_textarea.get(1.0,END)
            ob.sendmail(senderEntry.get(),recieverEntry.get(),message)
            ob.quit()
            messagebox.showinfo("Success","Bill Sucessfully Sent",parent=root1)
            root1.destroy()
        except:
            messagebox.showerror('Error','Something went wrong, Please try again!',parent=root1)     

    if textarea.get(1.0,END)=='\n':
        messagebox.showerror('Error','Bill is empty')
    else:
        root1=Toplevel()
        root1.grab_set()
        root1.title('Send Email')
        root1.config(bg='gray20')
        root1.resizable(0,0)

        senderFrame=LabelFrame(root1,text='SENDER',font=('arial',16,'bold'),bd=6,bg='gray20',fg='white')
        senderFrame.grid(row=0,column=0,padx=40,pady=20)

        senderLabel=Label(senderFrame,text="Sender's Email",font=('arial',14,'bold'),bg='gray20',fg='white')
        senderLabel.grid(row=0,column=0,padx=10,pady=8)

        senderEntry=Entry(senderFrame,font=('arial',14,'bold'),bd=2,width=23,relief=RIDGE)
        senderEntry.grid(row=0,column=1,padx=10,pady=8)

        passwordLabel=Label(senderFrame,text="Password",font=('arial',14,'bold'),bg='gray20',fg='white')
        passwordLabel.grid(row=1,column=0,padx=10,pady=8)

        passwordEntry=Entry(senderFrame,font=('arial',14,'bold'),bd=2,width=23,relief=RIDGE,show="#")
        passwordEntry.grid(row=1,column=1,padx=10,pady=8)

        recipientFrame=LabelFrame(root1,text='RECIPIENT',font=('arial',16,'bold'),bd=6,bg='gray20',fg='white')
        recipientFrame.grid(row=1,column=0,padx=40,pady=20)

        recieverLabel=Label(recipientFrame,text="Email Address",font=('arial',14,'bold'),bg='gray20',fg='white')
        recieverLabel.grid(row=0,column=0,padx=10,pady=8)

        recieverEntry=Entry(recipientFrame,font=('arial',14,'bold'),bd=2,width=23,relief=RIDGE)
        recieverEntry.grid(row=0,column=1,padx=10,pady=8)

        messageLabel=Label(recipientFrame,text="Message",font=('arial',14,'bold'),bg='gray20',fg='white')
        messageLabel.grid(row=1,column=0,padx=10,pady=8)

        email_textarea=Text(recipientFrame,font=('arial',14,'bold'),bd=2,relief=SUNKEN,width=42,height=11)
        email_textarea.grid(row=2,column=0,columnspan=2)
        email_textarea.delete(1.0,END)
        email_textarea.insert(END,textarea.get(1.0,END).replace('=','').replace('*','').replace('\t\t\t','\t\t'))

        sendButton=Button(root1,text="SEND",font=('arial',16,'bold'),width=15,command=send_gmail)
        sendButton.grid(row=2,column=0,pady=20)

        root1.mainloop()
"""
#? Print Function
#!This block of code is to able print on Windows operating system
def print_bill():
    if textarea.get(1.0,END)=='\n':
        messagebox.showerror('Error','Bill is empty')
    else: 
        file=tempfile.mktemp('.txt')
        open(file,'w').write(textarea.get(1.0,END))
        os.startfile(file,'print')   
"""

#!This block of code is to able print on all operating system
def print_bill():
    if textarea.get(1.0, END) == '\n':
        messagebox.showerror('Error', 'Bill is empty')
    else:
        file = tempfile.mktemp('.txt')
        with open(file, 'w') as f:
            f.write(textarea.get(1.0, END))
        
        system = platform.system()
        if system == "Windows":
            os.startfile(file, 'print')
        else:  # macOS, Linux, and other Unix-like systems
            try:
                subprocess.run(['lpr', file], check=True)
            except subprocess.CalledProcessError:
                messagebox.showerror('Error', 'Printing failed. No default printer found.')
            except FileNotFoundError:
                messagebox.showerror('Error', 'Printing system (lpr) not found.')
        
        # Clean up the temporary file
        os.remove(file)

#* Search Bill Function
def search_bill():
    found = False
    for i in os.listdir('bills/'):
        if i.split('.')[0]==billnumberEntry.get():
            f=open(f'bills/{i}','r')
            textarea.delete(1.0,END)
            for data in f:
                textarea.insert(END,data)
            f.close()
            found = True
            break
    if not found:
        messagebox.showerror('Error','Invalid Bill Number')

if not os.path.exists('bills'):
    os.mkdir('bills')

#* Save bill
def save_bill():
    global billnumber
    result=messagebox.askyesno('Confirm','Do you want to save this bill?')
    if result:
        bill_content=textarea.get(1.0,END)
        file=open(f'bills/{billnumber}.txt','w')
        file.write(bill_content)
        file.close()
        messagebox.showinfo('Success',f'bill number{billnumber} is saved successfully')
        billnumber=random.randint(200,1000)


billnumber=random.randint(200,1000)

#*Bill Area
def bill_area():
    if nameEntry.get()== '' or phoneEntry.get() == '':
        messagebox.showerror('Error','Customer Details Required')
    elif costmeticpriceEntry.get()=='' and grocerypriceEntry.get()=='' and drinkspriceEntry.get()=='':
        messagebox.showerror('Error','No item Selected')
    elif costmeticpriceEntry.get()=='GHS 0\t' and grocerypriceEntry.get()=='GHS 0' and drinkspriceEntry.get()=='GHS 0':
        messagebox.showerror('Error','No Products Selected')
    else:
        textarea.delete(1.0,END)   
        textarea.insert(END,'\t\tWELCOME CUSTOMER\n')
        textarea.insert(END,f'Bill Number: {billnumber}\n')
        textarea.insert(END,f'Customer Name: {nameEntry.get()}\n')
        textarea.insert(END,f'Customer Phone Number: {phoneEntry.get()}\n') 
        textarea.insert(END,'\n==========================================================\n')
        textarea.insert(END,'Product\t\t\tQTY\t\t\tPrice')
        textarea.insert(END,'\n==========================================================\n')
        if bathsoapEntry.get()!='0':
            textarea.insert(END,f'Bath Soap\t\t\t{bathsoapEntry.get()}\t\t\t{soapprice}GHS\n')
        if facecreamEntry.get()!='0':
            textarea.insert(END,f'Face Cream\t\t\t{facecreamEntry.get()}\t\t\t{facecreamprice}GHS\n')
        if facewashEntry.get()!='0':
            textarea.insert(END,f'Face Wash\t\t\t{facewashEntry.get()}\t\t\t{facewashprice}GHS\n')
        if hairsprayEntry.get()!='0':
            textarea.insert(END,f'Hair Spray\t\t\t{hairsprayEntry.get()}\t\t\t{hairsprayprice}GHS\n')
        if hairgelEntry.get()!='0':
            textarea.insert(END,f'Hair Gel\t\t\t{hairgelEntry.get()}\t\t\t{hairgelprice}GHS\n')
        if bodylotionEntry.get()!='0':
            textarea.insert(END,f'Body Lotion\t\t\t{bodylotionEntry.get()}\t\t\t{bodylotionprice}GHS\n')                               

        #! Grocies
        if riceEntry.get()!='0':
            textarea.insert(END,f'Rice\t\t\t{riceEntry.get()}\t\t\t{riceprice}GHS\n')    
        if oilEntry.get()!='0':
            textarea.insert(END,f'Oil\t\t\t{oilEntry.get()}\t\t\t{oilprice}GHS\n')     
        if coffeeEntry.get()!='0':
            textarea.insert(END,f'Coffee\t\t\t{coffeeEntry.get()}\t\t\t{coffeeprice}GHS\n')
        if teaEntry.get()!='0':
            textarea.insert(END,f'Tea\t\t\t{teaEntry.get()}\t\t\t{teaprice}GHS\n')
        if sugarEntry.get()!='0':
            textarea.insert(END,f'Sugar\t\t\t{sugarEntry.get()}\t\t\t{sugarprice}GHS\n')
        if wheatEntry.get()!='0':
            textarea.insert(END,f'Wheat\t\t\t{wheatEntry.get()}\t\t\t{wheatprice}GHS\n') 
        
        #! Drinks
        if maazaEntry.get()!='0':
            textarea.insert(END,f'Maaza\t\t\t{maazaEntry.get()}\t\t\t{maazaprice}GHS\n')
        if pepisEntry.get()!='0':
            textarea.insert(END,f'Pepsi\t\t\t{pepisEntry.get()}\t\t\t{pepsiprice}GHS\n')
        if dewEntry.get()!='0':
            textarea.insert(END,f'Dew\t\t\t{dewEntry.get()}\t\t\t{dewprice}GHS\n')
        if fantaEntry.get()!='0':
            textarea.insert(END,f'Fanta\t\t\t{fantaEntry.get()}\t\t\t{fantaprice}GHS\n')
        if cokeEntry.get()!='0':
            textarea.insert(END,f'Coca Cola\t\t\t{cokeEntry.get()}\t\t\t{cokeprice}GHS\n')
        if spriteEntry.get()!='0':
            textarea.insert(END,f'Sprite\t\t\t{spriteEntry.get()}\t\t\t{spriteprice}GHS\n')  
        textarea.insert(END,'\n*************************************************\n')

        if cosmetictaxEntry.get()!='GHS 0.0':
            textarea.insert(END,f'\n Cosmestics Tax\t\t{cosmetictaxEntry.get()}')
        if grocerytaxEntry.get()!='GHS 0.0':
            textarea.insert(END,f'\n Grocery Tax\t\t{grocerytaxEntry.get()}')
        if drinkstaxEntry.get()!='GHS 0.0':
            textarea.insert(END,f'\n Drinks Tax\t\t{drinkstaxEntry.get()}')
        textarea.insert(END,f'\n Total Bill\t\t{totalbill}')
        textarea.insert(END,'\n*************************************************\n') 
        save_bill()

#*Total Function                           
def total():
    global soapprice,facecreamprice,facewashprice,hairsprayprice,hairgelprice,bodylotionprice
    global riceprice,oilprice,coffeeprice,teaprice,sugarprice,wheatprice
    global maazaprice,pepsiprice,dewprice,fantaprice,cokeprice,spriteprice
    global totalbill

    #*Cosmetics price calculation
    soapprice=int(bathsoapEntry.get())*20
    facecreamprice=int(facecreamEntry.get())*30
    facewashprice=int(facewashEntry.get())*25
    hairsprayprice=int(hairsprayEntry.get())*50
    hairgelprice=int(hairgelEntry.get())*40
    bodylotionprice=int(bodylotionEntry.get())*60

    totalcosmeticprice=soapprice+facecreamprice+facewashprice+hairsprayprice+hairgelprice+bodylotionprice
    costmeticpriceEntry.delete(0,END)
    costmeticpriceEntry.insert(0,'GHS' +str(totalcosmeticprice))
    cosmetictax=totalcosmeticprice*0.05
    cosmetictaxEntry.delete(0,END)
    cosmetictaxEntry.insert(0,'GHS'+str(cosmetictax))
    

    #*Grocery Price calculation
    riceprice=int(riceEntry.get())*70
    oilprice=int(oilEntry.get())*45
    coffeeprice=int(coffeeEntry.get())*25
    teaprice=int(teaEntry.get())*15
    sugarprice=int(sugarEntry.get())*32
    wheatprice=int(wheatEntry.get())*45

    totalgroceryprice=riceprice+oilprice+coffeeprice+teaprice+sugarprice+wheatprice
    grocerypriceEntry.delete(0,END)
    grocerypriceEntry.insert(0,'GHS' +str(totalgroceryprice))
    grocerytax=totalgroceryprice*0.06
    grocerytaxEntry.delete(0,END)
    grocerytaxEntry.insert(0,'GHS'+str(grocerytax))

    #*Cold Drink Price calculation
    maazaprice=int(maazaEntry.get())*5
    pepsiprice=int(pepisEntry.get())*7
    dewprice=int(dewEntry.get())*6
    fantaprice=int(fantaEntry.get())*8
    cokeprice=int(cokeEntry.get())*10
    spriteprice=int(spriteEntry.get())*7

    totaldrinksprice=maazaprice+pepsiprice+dewprice+fantaprice+cokeprice+spriteprice
    drinkspriceEntry.delete(0,END)
    drinkspriceEntry.insert(0,'GHS' + str(totaldrinksprice))
    drinkstax=totaldrinksprice*0.02
    drinkstaxEntry.delete(0,END)
    drinkstaxEntry.insert(0,'GHS'+str(drinkstax))

    totalbill=totalcosmeticprice+totalgroceryprice+totaldrinksprice+cosmetictax+grocerytax+drinkstax

#! GUI Port
root=Tk()
root.title("Retail Billing System")
root.geometry("1350x820")
root.iconbitmap('')
headingLabel=Label(root,text="Retail Billing System v1.1",font=('times new roman',30,'bold'),bg='gray20',fg='gold',bd=12,relief=GROOVE)
headingLabel.pack(fill=X)

customer_details_frame=LabelFrame(root,text="Customer Details",font=('times new roman',15,'bold'),bg='gray20',fg='gold',bd=12,relief=GROOVE)
customer_details_frame.pack(fill=X)

nameLabel=Label(customer_details_frame,text='Name:',font=('times new roman',15,'bold'),bg='gray20',fg='white')
nameLabel.grid(row=0,column=0,padx=20)

nameEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
nameEntry.grid(row=0,column=1,padx=8)

phoneLabel=Label(customer_details_frame,text='Phone Number:',font=('times new roman',15,'bold'),bg='gray20',fg='white')
phoneLabel.grid(row=0,column=2,padx=20,pady=2)

phoneEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
phoneEntry.grid(row=0,column=3,padx=8)

billnumberLabel=Label(customer_details_frame,text='Bill Number:',font=('times new roman',15,'bold'),bg='gray20',fg='white')
billnumberLabel.grid(row=0,column=4,padx=20,pady=2)

billnumberEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
billnumberEntry.grid(row=0,column=5,padx=8)

searchButton=Button(customer_details_frame,text='SEARCH',font=('arial',12,'bold'),bd=7,width=8,command=search_bill)
searchButton.grid(row=0,column=6,padx=20,pady=8)

productsFrame=Frame(root)
productsFrame.pack()

cosmeticsFrame=LabelFrame(productsFrame,text='Cosmestics',font=('times new roman',30,'bold'),bg='gray20',fg='gold',bd=12,relief=GROOVE)
cosmeticsFrame.grid(row=0,column=0)

bathsoapLabel=Label(cosmeticsFrame,text='Bath Soap:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
bathsoapLabel.grid(row=0,column=0,pady=9,padx=10,sticky="w")

bathsoapEntry=Entry(cosmeticsFrame,font=("times new roman",15,'bold'),width=10,bd=7)
bathsoapEntry.grid(row=0,column=1,pady=9,padx=10)
bathsoapEntry.insert(0,0)

facecreamLabel=Label(cosmeticsFrame,text='Face Cream:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
facecreamLabel.grid(row=1,column=0,pady=9,padx=10,sticky="w")

facecreamEntry=Entry(cosmeticsFrame,font=("times new roman",15,'bold'),width=10,bd=7)
facecreamEntry.grid(row=1,column=1,pady=9,padx=10)
facecreamEntry.insert(0,0)

facewashLabel=Label(cosmeticsFrame,text='Face Wash:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
facewashLabel.grid(row=2,column=0,pady=9,padx=10,sticky="w")

facewashEntry=Entry(cosmeticsFrame,font=("times new roman",15,'bold'),width=10,bd=7)
facewashEntry.grid(row=2,column=1,pady=9,padx=10)
facewashEntry.insert(0,0)

hairsprayLabel=Label(cosmeticsFrame,text='Hair Spray:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
hairsprayLabel.grid(row=3,column=0,pady=9,padx=10,sticky="w")

hairsprayEntry=Entry(cosmeticsFrame,font=("times new roman",15,'bold'),width=10,bd=7)
hairsprayEntry.grid(row=3,column=1,pady=9,padx=10)
hairsprayEntry.insert(0,0)

hairgelLabel=Label(cosmeticsFrame,text='Hair Gel:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
hairgelLabel.grid(row=4,column=0,pady=9,padx=10,sticky="w")

hairgelEntry=Entry(cosmeticsFrame,font=("times new roman",15,'bold'),width=10,bd=7)
hairgelEntry.grid(row=4,column=1,pady=9,padx=10)
hairgelEntry.insert(0,0)

bodylotionLabel=Label(cosmeticsFrame,text='Body Lotion:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
bodylotionLabel.grid(row=5,column=0,pady=9,padx=10,sticky="w")

bodylotionEntry=Entry(cosmeticsFrame,font=("times new roman",15,'bold'),width=10,bd=7)
bodylotionEntry.grid(row=5,column=1,pady=9,padx=10)
bodylotionEntry.insert(0,0)

groceryFrame=LabelFrame(productsFrame,text='Grocery',font=('times new roman',30,'bold'),bg='gray20',fg='gold',bd=12,relief=GROOVE)
groceryFrame.grid(row=0,column=1)

riceLabel=Label(groceryFrame,text='Rice:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
riceLabel.grid(row=0,column=0,pady=9,padx=10,sticky="w")

riceEntry=Entry(groceryFrame,font=("times new roman",15,'bold'),width=10,bd=7)
riceEntry.grid(row=0,column=1,pady=9,padx=10)
riceEntry.insert(0,0)

oilLabel=Label(groceryFrame,text='Oil:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
oilLabel.grid(row=1,column=0,pady=9,padx=10,sticky="w")

oilEntry=Entry(groceryFrame,font=("times new roman",15,'bold'),width=10,bd=7)
oilEntry.grid(row=1,column=1,pady=9,padx=10)
oilEntry.insert(0,0)

coffeeLabel=Label(groceryFrame,text='Coffee:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
coffeeLabel.grid(row=2,column=0,pady=9,padx=10,sticky="w")

coffeeEntry=Entry(groceryFrame,font=("times new roman",15,'bold'),width=10,bd=7)
coffeeEntry.grid(row=2,column=1,pady=9,padx=10)
coffeeEntry.insert(0,0)

teaLabel=Label(groceryFrame,text='Tea:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
teaLabel.grid(row=3,column=0,pady=9,padx=10,sticky="w")

teaEntry=Entry(groceryFrame,font=("times new roman",15,'bold'),width=10,bd=7)
teaEntry.grid(row=3,column=1,pady=9,padx=10)
teaEntry.insert(0,0)

sugarLabel=Label(groceryFrame,text='Sugar:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
sugarLabel.grid(row=4,column=0,pady=9,padx=10,sticky="w")

sugarEntry=Entry(groceryFrame,font=("times new roman",15,'bold'),width=10,bd=7)
sugarEntry.grid(row=4,column=1,pady=9,padx=10)
sugarEntry.insert(0,0)

wheatLabel=Label(groceryFrame,text='Wheat:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
wheatLabel.grid(row=5,column=0,pady=9,padx=10,sticky="w")

wheatEntry=Entry(groceryFrame,font=("times new roman",15,'bold'),width=10,bd=7)
wheatEntry.grid(row=5,column=1,pady=9,padx=10)
wheatEntry.insert(0,0)

drinksFrame=LabelFrame(productsFrame,text='Cold Drinks',font=('times new roman',30,'bold'),bg='gray20',fg='gold',bd=12,relief=GROOVE)
drinksFrame.grid(row=0,column=2)

maazaLabel=Label(drinksFrame,text='Maaza:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
maazaLabel.grid(row=0,column=0,pady=9,padx=10,sticky="w")

maazaEntry=Entry(drinksFrame,font=("times new roman",15,'bold'),width=10,bd=7)
maazaEntry.grid(row=0,column=1,pady=9,padx=10)
maazaEntry.insert(0,0)

pepisLabel=Label(drinksFrame,text='Pepis:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
pepisLabel.grid(row=1,column=0,pady=9,padx=10,sticky="w")

pepisEntry=Entry(drinksFrame,font=("times new roman",15,'bold'),width=10,bd=7)
pepisEntry.grid(row=1,column=1,pady=9,padx=10)
pepisEntry.insert(0,0)

dewLabel=Label(drinksFrame,text='Dew:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
dewLabel.grid(row=2,column=0,pady=9,padx=10,sticky="w")

dewEntry=Entry(drinksFrame,font=("times new roman",15,'bold'),width=10,bd=7)
dewEntry.grid(row=2,column=1,pady=9,padx=10)
dewEntry.insert(0,0)

fantaLabel=Label(drinksFrame,text='Fanta:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
fantaLabel.grid(row=3,column=0,pady=9,padx=10,sticky="w")

fantaEntry=Entry(drinksFrame,font=("times new roman",15,'bold'),width=10,bd=7)
fantaEntry.grid(row=3,column=1,pady=9,padx=10)
fantaEntry.insert(0,0)

cokeLabel=Label(drinksFrame,text='Coca Cola:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
cokeLabel.grid(row=4,column=0,pady=9,padx=10,sticky="w")

cokeEntry=Entry(drinksFrame,font=("times new roman",15,'bold'),width=10,bd=7)
cokeEntry.grid(row=4,column=1,pady=9,padx=10)
cokeEntry.insert(0,0)

spriteLabel=Label(drinksFrame,text='Sprite:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
spriteLabel.grid(row=5,column=0,pady=9,padx=10,sticky="w")

spriteEntry=Entry(drinksFrame,font=("times new roman",15,'bold'),width=10,bd=7)
spriteEntry.grid(row=5,column=1,pady=9,padx=10)
spriteEntry.insert(0,0)

billframe=Frame(productsFrame,bd=8,relief=GROOVE)
billframe.grid(row=0,column=3,padx=10)

billareaLabel=Label(billframe,text='Bill Area',font=("times new roman",15,'bold'),bd=7,relief=GROOVE)
billareaLabel.pack(fill=X)

scrollbar=Scrollbar(billframe,orient=VERTICAL)
scrollbar.pack(side=RIGHT,fill=Y)
textarea=Text(billframe,height=18,width=60,yscrollcommand=scrollbar.set)
textarea.pack()
scrollbar.config(command=textarea.yview)

billmenuFrame=LabelFrame(root,text='Bill Menu',font=('times new roman',30,'bold'),bg='gray20',fg='gold',bd=12,relief=GROOVE)
billmenuFrame.pack()

costmeticpriceLabel=Label(billmenuFrame,text='Costmetic Price:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
costmeticpriceLabel.grid(row=0,column=0,pady=9,padx=10,sticky="w")

costmeticpriceEntry=Entry(billmenuFrame,font=("times new roman",15,'bold'),width=10,bd=7)
costmeticpriceEntry.grid(row=0,column=1,pady=9,padx=10)

grocerypriceLabel=Label(billmenuFrame,text='Grocery Price:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
grocerypriceLabel.grid(row=1,column=0,pady=9,padx=10,sticky="w")

grocerypriceEntry=Entry(billmenuFrame,font=("times new roman",15,'bold'),width=10,bd=7)
grocerypriceEntry.grid(row=1,column=1,pady=9,padx=10)

drinkspriceLabel=Label(billmenuFrame,text='Cold Drinks Price:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
drinkspriceLabel.grid(row=2,column=0,pady=9,padx=10,sticky="w")

drinkspriceEntry=Entry(billmenuFrame,font=("times new roman",15,'bold'),width=10,bd=7)
drinkspriceEntry.grid(row=2,column=1,pady=9,padx=10)

cosmetictaxLabel=Label(billmenuFrame,text='Costmetic Tax:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
cosmetictaxLabel.grid(row=0,column=2,pady=9,padx=10,sticky="w")

cosmetictaxEntry=Entry(billmenuFrame,font=("times new roman",15,'bold'),width=10,bd=7)
cosmetictaxEntry.grid(row=0,column=3,pady=9,padx=10)

grocerytaxLabel=Label(billmenuFrame,text='Grocery Tax:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
grocerytaxLabel.grid(row=1,column=2,pady=9,padx=10,sticky="w")

grocerytaxEntry=Entry(billmenuFrame,font=("times new roman",15,'bold'),width=10,bd=7)
grocerytaxEntry.grid(row=1,column=3,pady=9,padx=10)

drinkstaxLabel=Label(billmenuFrame,text='Cold Drinks Tax:', font=("times new roman",15,'bold'),bg='gray20',fg='white')
drinkstaxLabel.grid(row=2,column=2,pady=9,padx=10,sticky="w")

drinkstaxEntry=Entry(billmenuFrame,font=("times new roman",15,'bold'),width=10,bd=7)
drinkstaxEntry.grid(row=2,column=3,pady=9,padx=10)

buttonFrame=Frame(billmenuFrame,bd=8,relief=GROOVE)
buttonFrame.grid(row=0,column=4,rowspan=3)

totalButton=Button(buttonFrame,text='Total',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=total)
totalButton.grid(row=0,column=0,pady=20,padx=2)

billButton=Button(buttonFrame,text='Bill',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=bill_area)
billButton.grid(row=0,column=1,pady=20,padx=2)

emailButton=Button(buttonFrame,text='Email',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=send_email)
emailButton.grid(row=0,column=2,pady=20,padx=2)

printButton=Button(buttonFrame,text='Print',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=print_bill)
printButton.grid(row=0,column=3,pady=20,padx=2)

clearButton=Button(buttonFrame,text='Clear',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=clear)
clearButton.grid(row=0,column=4,pady=20,padx=2)

root.mainloop() 