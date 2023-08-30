from tkinter import *
from tkinter import ttk
import requests
from ttkthemes import ThemedTk

def currency_converter():
    try:
        selected_currency_from = combo1.get()
        selected_currency_to = combo2.get()
        amount = amount_entry.get()

        url = f'{url_base}{selected_currency_from}'
        response = requests.get(url).json()

        if 'conversion_rates' in response:
            conversion_rate = response['conversion_rates'].get(selected_currency_to)
            if conversion_rate is not None:
                converted_result = float(amount) * conversion_rate
                formatted_result = f'{amount} {selected_currency_from} = {converted_result:.2f} {selected_currency_to}'
                output_label.config(text=formatted_result)
                time_label.config(text='Last updated: ' + response['time_last_update_utc'])
            else:
                output_label.config(text='Invalid TO currency')
                time_label.config(text='')
        else:
            output_label.config(text='Error occurred during conversion')
            time_label.config(text='')
            print("Unable to fetch conversion rate.")
    except Exception as e:
        output_label.config(text='Error occurred during conversion')
        time_label.config(text='')
        print("An error occurred:", e)

root = ThemedTk(theme="arc")  
root.title("CURRENCY CONVERTER")
root.geometry('500x500')

frame1 = Frame(root, bg='#081F4D', width='500', height='100')
frame1.pack(fill='both', expand=True)
name_label = Label(frame1, text='Currency Converter', bg='#081F4D', pady=30, fg='white', font='segoe 28 bold')
name_label.pack()

frame2 = Frame(root)
frame2.pack(padx=20, pady=20)

from_label = Label(frame2, text='FROM', fg='black', font='segoe 16 bold')
from_label.grid(row=0, column=0, padx=10)

to_label = Label(frame2, text='TO', fg='black', font='segoe 16 bold')
to_label.grid(row=0, column=1, padx=10)

amount_label = Label(frame2, text='AMOUNT', font='segoe 16 bold')
amount_label.grid(row=2, column=0, pady=10, columnspan=2)

amount_entry = Entry(frame2, width='20', font='segoe 16 italic')
amount_entry.grid(row=3, column=0, columnspan=2)

combo1 = ttk.Combobox(frame2, width=18)
combo1.grid(row=1, column=0, padx=10)

combo2 = ttk.Combobox(frame2, width=18)
combo2.grid(row=1, column=1, padx=10)

output_label = Label(frame2, text='', font='segoe 16 bold', fg='green')
output_label.grid(row=4, column=0, columnspan=2, pady=15)

time_label = Label(frame2, text='', font='segoe 12 italic', fg='gray')
time_label.grid(row=5, column=0, columnspan=2)

button = Button(frame2, text='CONVERT', bg='#081F4D', fg='white', font='segoe 16 bold', command=currency_converter)
button.grid(row=6, column=0, columnspan=2, pady=15)

url_base = 'https://v6.exchangerate-api.com/v6/531fd05d2e78a9125d4981b5/latest/'

try:
    response = requests.get(f'{url_base}USD').json()
    if 'conversion_rates' in response:
        currencies = list(response['conversion_rates'].keys())
        combo1['values'] = currencies
        combo2['values'] = currencies
    else:
        print("Unable to fetch currency data.")
except requests.exceptions.RequestException as e:
    print("An error occurred while fetching currency data:", e)

root.mainloop()
