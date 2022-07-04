from random import randint
import threading
from turtle import color
from matplotlib.patches import Wedge
import pandas as pd
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import datetime
import time
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import matplotlib.pyplot as plt
import datetime
import time
import requests
import pandas as pd 
import datetime
import pytz
import os.path


crypto_name = "btceur"

step = 300

limit = 288

time2 = "1 day"
time
################################# Create a data file if it doenst exist

file_exists = os.path.exists('data_found.csv')

if file_exists == False:

    with open ('data_found.csv', 'w', newline= '')as f:
        fieldnames = ['Found', 'Btc', 'Eth', 'Xrp']
        thewriter = csv.DictWriter(f, fieldnames= fieldnames)

        thewriter.writeheader()
        thewriter.writerow({'Found': 100, 'Btc':0.01, 'Eth': 0.1, 'Xrp': 500}) 

################################# Various function

def get_time():

    now = datetime.datetime.now()
    Time = str(now.strftime("%H:%M"))

    return Time


def get_price(pair):
    #pair = crypto_name

    req = requests.get(f"https://www.bitstamp.net/api/v2/ticker/{pair}/")

    price = req.json()["last"]

    return price

def current_found():
    
    f = open("data_found.csv")
    csv_f = list(csv.reader(f))
    Found_already_have = float((csv_f[1][0])) 
    f.close()

    return Found_already_have

def current_crypto(crypto_name):

    if crypto_name == "btceur":
        x= 1
    elif crypto_name == "etheur":
        x=2
    else:
        x=3

    f = open("data_found.csv")
    csv_f = list(csv.reader(f))
    crypto_already_have = float((csv_f[1][x])) 
    f.close()

    return crypto_already_have

global current_price
current_price = get_price(pair= crypto_name)
print(current_price)

################################# Historical data

def histo():

    
    pair = crypto_name
    
    

    parameters = {
        "step":step,
        "limit":limit,
    }


    req = requests.get(f"https://www.bitstamp.net/api/v2/ohlc/{pair}/", params=parameters)

    req = req.json()["data"]["ohlc"]

    df = pd.DataFrame(req)

    

    tz = pd.to_datetime(df["timestamp"], unit='s').dt.tz_localize('utc')
    

    for i in range(len(tz)) :
        tz[i] = tz[i].astimezone(pytz.timezone('Europe/Berlin'))
        if step == 3600:
            tz[i] = tz[i].strftime("%d:%m:%H") 
        else:
            tz[i] = tz[i].strftime("%H:%M") 
            
        

    df["time"] = tz

    df = df[["time","close"]]

    df.to_csv("crypto_data.csv")

histo()

################################# Draw graph


plt.style.use("ggplot")

def anime(i):

    
    
    if step == 60 and i !=404:
        x_value = get_time()
        total_1 = get_price(pair= crypto_name)
        fieldnames = ["count", "x_value", "total_1"]


        with open('crypto_data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                "x_value": x_value,
                "total_1": total_1,
                
            }

            csv_writer.writerow(info)
            

            
            x_value = get_time()
            total_1 = get_price(pair= crypto_name)





    data = pd.read_csv('crypto_data.csv')
    
    x = data['time']
    y = data['close']
    
    plt.cla()
    
    plt.plot(x, y, 'b-', label = crypto_name)




    dat = data.iloc[:,1:1:1]

    j = dat.index[-1]


    ax = plt.gca()
    
    plt.grid(color='w', linestyle='solid')

    ax.set_xlim([max(0,j-limit),j+1])

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
    plt.setp(ax.get_yticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
    plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    
    plt.legend()
    
    #plt.title(crypto_name,color= 'white', fontdict={'fontsize':8})
    #plt.xlabel('Time',color= 'white',fontdict={'fontsize':10})
    #plt.ylabel('Price', color= 'white',fontdict={'fontsize':8})    


    

################################# Tkinter various

root = Tk()

root.geometry('1280x800')
root.title('Paper Trading')
root.state('zoomed')
root.config(background='grey')



def draw_pie():
    
    color = ['y','b','r','g']

    a = float(current_crypto(crypto_name='btceur'))*float(get_price(pair='btceur'))
    b = float(current_crypto(crypto_name='etheur'))*float(get_price(pair='etheur'))
    c = float(current_crypto(crypto_name='xrpeur'))*float(get_price(pair='xrpeur'))
    d = current_found()


    my_dict={'Nos':[a,b,c,d]}

    df = pd.DataFrame(data=my_dict)
    lbl =['Btc','Eth','Xrp','Eur']
    global fig1
    fig1 = df.plot.pie(y='Nos', figsize=(2.5,2), legend = None, labels= lbl, wedgeprops= {'edgecolor':'black'}, radius =1.4, colors= color, ylabel = ' ').get_figure();
    fig1.set_facecolor('grey')

    plotcanvas2 = FigureCanvasTkAgg(fig1,root)
    plotcanvas2.get_tk_widget().place(x=800, y= 100)


draw_pie()

sli = [1,2,3,4]

fig = plt.figure(clear=True,figsize=(5.5, 3.5), dpi=90)
plotcanvas = FigureCanvasTkAgg(fig,master=root)
plotcanvas.get_tk_widget().place(x=0, y= 0)
fig.patch.set_facecolor('grey')


text_price_label = Label(root, text= "Current price: ")
text_price_label.place(x=18, y= 520)

title = Label(root, text= f"{crypto_name} {time2}:")
title.place(x=20, y= 20)

portafolio= Label(root, text= "Portafolio: ")
portafolio.place(x=780, y= 20)

found_label2 = Label(root, width=12, height=2, text= f"{round(current_found(),3)} €")
found_label2.place(x=960, y= 550)

portafolio_btc = Label(root, width=12, height=2, text= f"{round(current_crypto(crypto_name= 'btceur'),3)} btc")
portafolio_btc .place(x=960, y= 600)

portafolio_eth = Label(root, width=12, height=2, text= f"{round(current_crypto(crypto_name= 'etheur'),3)} eth")
portafolio_eth.place(x=960, y= 650)

portafolio_xrp = Label(root, width=12, height=2, text= f"{round(current_crypto(crypto_name= 'xrp'),3)} xrp")
portafolio_xrp.place(x=960, y= 700)

time

price_label = Label(root, text= f"{current_price} €")
price_label.place(x=18, y= 560)

found_label = Label(root, text= f"{round(current_found(),3)} €")
found_label.place(x=15, y= 720)


found_in_crypto_label = Label(root, text= round(current_crypto(crypto_name= crypto_name),3))
found_in_crypto_label.place(x=200, y= 720)

found_in_cryptoEur_label = Label(root, text= f"{round(current_crypto(crypto_name= crypto_name)* float(get_price(pair= crypto_name)),3)} €")
found_in_cryptoEur_label.place(x=400, y= 720)

time

################################# crypto

def click_eth():
    global crypto_name 
    crypto_name = "etheur"

    histo()
    Buy_b['text'] = f"Buy {crypto_name}"
    Sell_b['text'] = f"Sell {crypto_name}"

    found_in_crypto_label['text'] = round(current_crypto(crypto_name= crypto_name),3)

    found_in_cryptoEur_label['text'] = f"{round(current_crypto(crypto_name= crypto_name)* float(get_price(pair= crypto_name)),3)} €"

    anime(404)

    plotcanvas.draw()

    title['text'] = f"{crypto_name} {time2}"
    

eth_button = Button(root, text="etheur", command = click_eth,height= 4, width=12)
eth_button.place(x=730, y= 520)


def click_btc():
    global crypto_name 
    crypto_name = "btceur"

    histo()

    Buy_b['text'] = f"Buy {crypto_name}"   
    Sell_b['text'] = f"Sell {crypto_name}" 

    found_in_crypto_label['text'] = round(current_crypto(crypto_name= crypto_name),3)

    found_in_cryptoEur_label['text'] = f"{round(current_crypto(crypto_name= crypto_name)* float(get_price(pair= crypto_name)),3)} €"
        
    anime(404)
    
    plotcanvas.draw()

    title['text'] = f"{crypto_name} {time2}"



btc_button = Button(root, text="btceur", command = click_btc,height= 4, width=12)
btc_button.place(x=730, y= 600)


def click_xrp():
    global crypto_name 
    crypto_name = "xrpeur"

    histo()

    Buy_b['text'] = f"Buy {crypto_name}"
    Sell_b['text'] = f"Sell {crypto_name}"

    found_in_crypto_label['text'] = round(current_crypto(crypto_name= crypto_name),3)
    
    found_in_cryptoEur_label['text'] = f"{round(current_crypto(crypto_name= crypto_name)* float(get_price(pair= crypto_name)),3)} €"

    anime(404)
    plotcanvas.draw()

    title['text'] = f"{crypto_name} {time2}"



xrp_button = Button(root, text="xrpeur", command = click_xrp,height= 4, width=12)
xrp_button.place(x=730, y= 680)

################################# Time

def click_h():

    global step 
    step = 60
    global limit 
    limit = 60

    histo()

    anime(404)
    plotcanvas.draw()
    
    global time2
    time2 = "1 hour"
    title['text'] = f"{crypto_name} {time2}"

    
 
   

h_button = Button(root, text="1h", command = click_h,height= 4, width=12)
h_button.place(x=600, y= 520)

def click_d():
    global step 
    step = 300
    global limit 
    limit = 288

    histo()
    
    anime(404)
    plotcanvas.draw()

    global time2
    time2 = "1 day"
    title['text'] = f"{crypto_name} {time2}"

d_button = Button(root, text="1d", command = click_d,height= 4, width=12)
d_button.place(x=600, y= 600)

def click_w():
    global step 
    step = 3600
    global limit 
    limit = 168

    histo()

    anime(404)
    plotcanvas.draw()



    global time2
    time2 = "1 week"
    title['text'] = f"{crypto_name} {time2}"



 

w_button = Button(root, text="1w", command = click_w,height= 4, width=12)
w_button.place(x=600, y= 680)

################################# Found


add_found = Entry(root, width=10, borderwidth=2, cursor= "xterm")
add_found.place(x= 15, y= 640)



def click_add_found():
    Found_wanted_to_add = int(add_found.get())
    add_found.delete(0, 'end')

    Found_already_have = current_found()

    df = pd.read_csv("data_found.csv")

    total = Found_wanted_to_add + Found_already_have
    
    df.at[0,'Found']= total
    df.to_csv("data_found.csv", index=False)

    found_label['text'] = f"{round(total,3)} €"
    found_label2['text'] = f"{round(total,3)} €"

  
    


    




add_found_b = Button(root, text="Add Found", command = click_add_found,height= 1, width=10)
add_found_b.place(x=15, y= 680)

#################################  Buy

Buy = Entry(root, width=10, borderwidth=2, cursor= "xterm")
Buy.place(x= 200, y= 640)


def click_buy():
    crypto_wanted_buy = float(Buy.get())

    y = current_found()

    if crypto_wanted_buy > y:

        Buy.delete(0, 'end')
        warnlabel = Label(root, text="Not enough found", bg='red')
        warnlabel.place(x=200, y=570)
        root.after(2000, lambda: warnlabel.destroy())
        return

    x = float(get_price(pair= crypto_name))

    Crypto_in_crypto = crypto_wanted_buy/x

    Buy.delete(0, 'end')

    crypto_already_have = float(current_crypto(crypto_name= crypto_name))

    df = pd.read_csv("data_found.csv")

    total_c = Crypto_in_crypto + crypto_already_have
    
    if crypto_name == "btceur":
        x= 'Btc'
    elif crypto_name == "etheur":
        x= 'Eth'
    else:
        x= 'Xrp'

    df.at[0,x]= total_c
    df.to_csv("data_found.csv", index=False)

    now_found= y- crypto_wanted_buy

    df.at[0,'Found']= now_found
    df.to_csv("data_found.csv", index=False)

    found_in_crypto_label['text'] = round(current_crypto(crypto_name= crypto_name),3)

    found_label['text'] = f"{round(now_found,3)} €"
    found_label2['text'] = f"{round(now_found,3)} €"

    if x == "Btc":
        portafolio_btc['text'] = f"{round(current_crypto(crypto_name= crypto_name),3)} btc"
    elif x == "Eth":
        portafolio_eth['text'] = f"{round(current_crypto(crypto_name= crypto_name),3)} eth"
    else:
        portafolio_xrp['text'] = f"{round(current_crypto(crypto_name= crypto_name),3)} xrp"

   

    



Buy_b = Button(root, text=f"Buy {crypto_name}", command = click_buy,height= 1, width=10)
Buy_b.place(x=200, y= 680)

################################# Sell

Sell = Entry(root, width=10, borderwidth=2, cursor= "xterm")
Sell.place(x= 400, y= 640)


def click_sell():
    crypto_wanted_sell = float(Sell.get())

    y = current_crypto(crypto_name=crypto_name)

    if crypto_wanted_sell > y:

        Sell.delete(0, 'end')
        warnlabel = Label(root, text="Not enough crypto", bg='red')
        warnlabel.place(x=400, y=570)
        root.after(2000, lambda: warnlabel.destroy())
        return

    x = float(get_price(pair= crypto_name))

    Crypto_in_eur = crypto_wanted_sell*x

    Sell.delete(0, 'end')

    found_already_have = current_found()
    crypto_already_have = float(current_crypto(crypto_name=crypto_name))

    df = pd.read_csv("data_found.csv")

    total_eur = found_already_have + Crypto_in_eur
    total_c = crypto_already_have - crypto_wanted_sell
    
    if crypto_name == "btceur":
        x= 'Btc'
    elif crypto_name == "etheur":
        x= 'Eth'
    else:
        x= 'Xrp'

    df.at[0,x]= total_c
    df.to_csv("data_found.csv", index=False)



    df.at[0,'Found']= total_eur
    df.to_csv("data_found.csv", index=False)

    found_in_crypto_label['text'] = round(total_c,3)

    found_label['text'] = f"{round(total_eur,3)} €"
    found_label2['text'] = f"{round(total_eur,3)} €"

    if x == "Btc":
            portafolio_btc['text'] = f"{round(current_crypto(crypto_name= crypto_name),3)} btc"
    elif x == "Eth":
        portafolio_eth['text'] = f"{round(current_crypto(crypto_name= crypto_name),3)} eth"
    else:
        portafolio_xrp['text'] = f"{round(current_crypto(crypto_name= crypto_name),3)} xrp"

    


Sell_b = Button(root, text=f"Sell {crypto_name}", command = click_sell,height= 1, width=10)
Sell_b.place(x=400, y= 680)


#def click_bug():
#    draw_pie()

#bug = Button(root, text="bug", command = click_bug, height= 1, width=10)
#bug.place(x=1120, y= 750)



################################# Multi_thread

def MyLoop():   

    while True:
        global current_price
        current_price = float(get_price(pair= crypto_name))
        crypto = float(current_crypto(crypto_name=crypto_name))
        price_label['text'] = f"{current_price} €"

        print(current_price)

        global ap
        ap = current_price* crypto

        found_in_cryptoEur_label['text'] = f"{round(ap,3)} €"
        
        
        time.sleep(4)
    



p1 = threading.Thread(target=MyLoop)

p1.Daemon = True

p1.start()

################################# 



ani = FuncAnimation(plt.gcf(), anime, interval = 60000)

root.mainloop()
