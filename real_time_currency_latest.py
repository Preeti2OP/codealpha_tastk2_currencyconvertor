from tkinter import *
from tkinter import ttk
import requests
from ttkthemes import ThemedTk
import json

def on_enter(event):
    event.widget['background'] = '#1565c0' 

def on_leave(event):
    event.widget['background'] = '#1976d2'  

def toggle_mode():
    global online_mode
    online_mode = not online_mode
    update_mode_indicator()
    if online_mode:
        start_auto_update()
    else:
        stop_auto_update()

def update_mode_indicator():
    if online_mode:
        mode_label.config(text='Online', bg='green')
    else:
        mode_label.config(text='Offline', bg='red')

def currency_converter():
    try:
        selected_currency_from = combo1.get()
        selected_currency_to = combo2.get()
        amount = amount_entry.get()

        if not amount:
            raise ValueError("Please enter an amount for conversion.")
        
        if not selected_currency_from or not selected_currency_to:
            raise ValueError("Please select both source and target currencies.")
        
        if online_mode:
            url = f'http://api.exchangeratesapi.io/v1/latest?access_key={api_key}&format=1'
            response = requests.get(url).json()
        else:
            response = load_offline_data()
        
        if 'rates' in response:
            conversion_rate = response['rates'].get(selected_currency_to)
            if conversion_rate is not None:
                converted_result = float(amount) * conversion_rate
                formatted_result = f'{amount} {selected_currency_from} = {converted_result:.2f} {selected_currency_to}'
                output_label.config(text=formatted_result)
                time_label.config(text='Last updated: ' + response['date'])
            else:
                output_label.config(text='Invalid TO currency')
                time_label.config(text='')
        else:
            output_label.config(text='Error occurred during conversion')
            time_label.config(text='')
    except Exception as e:
        output_label.config(text=str(e))
        time_label.config(text='')

def start_auto_update():
    update_auto()

def update_auto():
    if online_mode:
        try:
            response = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={api_key}&format=1').json()
            if 'rates' in response:
                save_offline_data(response['rates'])
        except requests.exceptions.RequestException:
            pass
        root.after(60000, update_auto)  

def stop_auto_update():
    pass

def save_offline_data(rates):
    with open('offline_data.json', 'w') as file:
        json.dump(rates, file)

def load_offline_data():
    try:
        with open('offline_data.json', 'r') as file:
            return {'rates': json.load(file)}
    except (FileNotFoundError, json.JSONDecodeError):
        return {'rates': {}}

def swap_currencies():
    selected_currency_from = combo1.get()
    selected_currency_to = combo2.get()
    combo1.set(selected_currency_to)
    combo2.set(selected_currency_from)

def clear_result():
    output_label.config(text='')
    time_label.config(text='')

api_key = 'a9f11bd4577ffa8a73f01faee147509f'

root = ThemedTk(theme="breeze")
root.title("Currency Converter")
root.geometry('500x600')
root.resizable(True, True)  

frame1 = Frame(root, bg='#1976d2', width='500', height='100') 
frame1.pack(fill='both', expand=True)
name_label = Label(frame1, text='Currency Converter', bg='#1976d2', pady=30, fg='white', font='Arial 28 bold')
name_label.pack()

frame2 = Frame(root)
frame2.pack(padx=20, pady=20)

from_label = Label(frame2, text='FROM', fg='black', font='Arial 16 bold')
from_label.grid(row=0, column=0, padx=10)

to_label = Label(frame2, text='TO', fg='black', font='Arial 16 bold')
to_label.grid(row=0, column=1, padx=10)

amount_label = Label(frame2, text='AMOUNT', font='Arial 16 bold')
amount_label.grid(row=2, column=0, pady=10, columnspan=2)

amount_entry = Entry(frame2, width='20', font='Arial 16 italic')
amount_entry.grid(row=3, column=0, columnspan=2)

combo1 = ttk.Combobox(frame2, width=15, font='Arial 14')  
combo1.grid(row=1, column=0, padx=10)

combo2 = ttk.Combobox(frame2, width=15, font='Arial 14')  
combo2.grid(row=1, column=1, padx=10)

output_label = Label(frame2, text='', font='Arial 16 bold', fg='#1565c0')  
output_label.grid(row=4, column=0, columnspan=2, pady=(15, 0))

time_label = Label(frame2, text='', font='Arial 12 italic', fg='gray')
time_label.grid(row=5, column=0, columnspan=2)

convert_button = Button(frame2, text='CONVERT', bg='#1976d2', fg='white', font='Arial 16 bold',
                        command=currency_converter)
convert_button.grid(row=6, column=0, columnspan=2, pady=15)
convert_button.bind("<Enter>", on_enter)
convert_button.bind("<Leave>", on_leave) 

swap_button = Button(frame2, text='SWAP', bg='gray', fg='white', font='Arial 12 bold', command=swap_currencies)
swap_button.grid(row=7, column=0, columnspan=2, pady=10)

clear_button = Button(frame2, text='CLEAR', bg='gray', fg='white', font='Arial 12 bold', command=clear_result)
clear_button.grid(row=8, column=0, columnspan=2, pady=10)

mode_label = Label(root, text='', bg='green', width=10, height=1)
mode_label.pack(pady=(0, 10))

toggle_button = Button(root, text='Toggle Mode', bg='gray', fg='white', font='Arial 12 bold', command=toggle_mode)
toggle_button.pack()

online_mode = True
update_mode_indicator()

try:
    response = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={api_key}&format=1').json()
    if 'rates' in response:
        currencies = list(response['rates'].keys())
        combo1['values'] = currencies
        combo2['values'] = currencies
    else:
        print("Unable to fetch currency data.")
except requests.exceptions.RequestException as e:
    print("An error occurred while fetching currency data:", e)

root.mainloop()
