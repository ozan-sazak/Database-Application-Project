# -*- coding: utf-8 -*-
"""
Created on Thu May  2 23:41:35 2024

@author: Ozan
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 01:18:40 2024

@author: Ozan
"""

import sqlite3 as sql
import PySimpleGUI as sg
import random
connect = sql.connect('Project.db')

c = connect.cursor()


def login():    
    layout = [
            [sg.Text('Please enter your e-mail and password')],
            [sg.Text('E-mail:'), sg.Input(key='e_mail'), sg.Text('Password:'), sg.Input(key='Password', password_char = '*')],
            [sg.Button('Enter'), sg.Button('Register as Provider'), sg.Exit()]]
    
    return sg.Window('Login', layout)
    
def provider_window():
    layout = [
            [sg.Button('Offer Service'), sg.Button('Bookings')],
            [sg.Button('Logout')]]
    return sg.Window('Provider Panel', layout)


def provider_confirming_bookings(values):
    pro = []
    lst = c.execute("SELECT User.Name, booking.bid FROM User, books, booking WHERE status = 'pending' AND booking.bid = books.bid AND books.customer_id = User.userid ")
    for row in lst:
        pro.append(row)
        
    layout = [[sg.Listbox(values=pro, size=(30, 6), key='chosen_customer')],
              [sg.Button('Confirm Customer'), sg.Button('Reject Customer'),sg.Button('Close')]
                  ]
    
    pp = sg.Window("Customer Rejection Window", layout, finalize=True)
    
    while True:
        event, values = pp.read()
        bookingid = values["chosen_customer"][0]
        bbid = bookingid[1]
        if event=="Confirm Customer":
            c.execute("UPDATE booking SET status = 'confirmed' WHERE booking.bid = ?", (bbid,))
            connect.commit()
            sg.popup("Customer confirmed")
        
        elif event=="Confirm Customer":
            c.execute("UPDATE booking SET status = 'rejected' WHERE booking.bid = ?", (bbid,))
            connect.commit()
            sg.popup("Customer rejected")

        elif event=='Close':
            break
    pp.close()
        
def provider_registering(values):
    layout = [[sg.Text("Registration Panel")],
              [sg.Text('Provider Name:', size=(10,1)), sg.Input(size=(10, 1), key='name')],
              [sg.Text('Provider Surname:', size=(10,1)), sg.Input(size=(10, 1), key='surname')],
              [sg.Text('E-mail:', size=(10,1)), sg.Input(size=(10, 1), key='e-mail')],
              [sg.Text('Password:', size=(10,1)), sg.Input(size=(10, 1), key='pas')],
              [sg.Text('Phone number:', size=(10,1)), sg.Input(size=(10, 1), key='phone')],
              [sg.Button('Register'),sg.Button('Close')]
              ]
    
    pop = sg.Window('Registering Window', layout, finalize=True)
    while True:
        event, values = pop.read()
        n = values['name']
        s = values['surname']
        e = values['e-mail']
        p = values['pas']
        ph = values['phone']
        pid = random.randint(10,50)
        if event == 'Register':
            c.execute("INSERT INTO User VALUES(?, ?, ?, ?, ?, ?)", (pid, n, s, p, ph, e))
            c.execute("INSERT INTO Provider VALUES(?)", (pid,))
            connect.commit()
            sg.popup("Provider Added")
        elif event=='Close':
            break
    pop.close()
    
def provider_offering_service_button(values):
    layout = [[sg.Text("Provider Adding Service Panel")],
              [sg.Text('Service ID:', size=(10,1)), sg.Input(size=(10, 1), key='serid')],
              [sg.Text('Service Name:', size=(10,1)), sg.Input(size=(10, 1), key='sername')],
              [sg.Text('Description:', size=(10,1)), sg.Input(size=(10, 1), key='serdescrip')],
              [sg.Text('Cateory:', size=(10,1)), sg.Input(size=(10, 1), key='categ')],
              [sg.Text('Price:', size=(10,1)), sg.Input(size=(10, 1), key='serprice')],
              [sg.Button('Provider Add Service'),sg.Button('Close')]
              ]

    p = sg.Window("Add service informations", layout, finalize=True)
    while True:
        event, values = p.read()
        a = values["serid"]
        b = values["sername"]
        k = values["serdescrip"]
        d = values["categ"]
        e = values["serprice"]
        
        if event == "Provider Add Service":
            c.execute("INSERT INTO Services VALUES(?, ?, ?, ?, ?, ?)", (a, b, k, d, e, "Available"))
            c.execute("INSERT INTO Offered VALUES(?, ?, ?) ", (a, login_user_id, "Pending"))
            connect.commit()
            sg.popup("Service Offered")
        elif event=="Close":
            break
    p.close()
        
def admin_window():
    
    all_services = []
    alll = c.execute('SELECT sid, sname FROM Services')
    for row in alll:
        all_services.append(row)
    
    
    
    layout = [[sg.Text('Welcome ' + login_user_name)],
              [sg.Text('Admin Panel')],
              [sg.Text("Filter Services:"), sg.Combo(['all_services', 'available_services', 'unavailable_services'], default_value='all_services', key='chosen_availability'), sg.Button('List Availability')],
              [sg.Listbox(values=all_services, size=(30, 6), key='chosen_service')],
              [sg.Button('Add Service'), sg.Button('Update Service'), sg.Button('Delete Service'), sg.Button('Details'), sg.Button("See the approval-waiting Providers"),sg.Button("See the Provider List")],
              [sg.Button('Logout')]
    ]
    return sg.Window('Admin Panel', layout)

def admins_provider_list(values):
    pro_list = []
    rate = c.execute("SELECT Name, userid, AVG(rating) FROM Rates, rate_applied, Offered, User WHERE Rates.rateid = rate_applied.rate_id AND rate_applied.sid = Offered.sid AND Offered.provider_id = User.userid")
    for row in rate:
        pro_list.append(row)
    
    layout = [[sg.Text("Providers")],
            [sg.Listbox(values=pro_list, size=(30,6), key = "chosen_provider")],
            [sg.Button("Disconfirm the Provider"), sg.Button("Close")]  
            ]
    popp = sg.Window("Provider List", layout, finalize=True)
    
    while True:
        event, values = popp.read()
        prov = values["chosen_provider"][0]
        provid = prov[1]
        if event == "Disconfirm the Provider":
            c.execute("UPDATE Offered SET Status = 'Disconfirmed' WHERE Offered.provider_id = ?", (provid,))
            connect.commit()
            sg.popup("Provider Disconfirmed")
        elif event == "Close":
            break
    popp.close()
    
def admin_confirms_or_rejets_provider(values):
    provider_list = []
    pr = c.execute("SELECT Offered.sid, Offered.provider_id, User.Name FROM Offered, User WHERE Status = 'Pending' AND Offered.provider_id = User.userid")
    for row in pr:
        provider_list.append(row)

    layout = [[sg.Text("Confirmation")],
              [sg.Listbox(values=provider_list, size=(30, 6), key='chosen_provider')],
              [sg.Button('Confirm Provider'), sg.Button('Reject Provider'),sg.Button("Close")]
              ]
    
    ppp = sg.Window("Confirmation", layout, finalize=True)
    while True:
        event, values = ppp.read()
        a = values["chosen_provider"][0]
        proid = a[1]
        seid = a[0]
        
        if event=="Close":
            break
            ppp.close()
        else:
            if event =="Confirm Provider":
                c.execute("UPDATE Offered SET Status = 'Confirmed' WHERE Offered.sid = ? AND Offered.provider_id = ?", (seid, proid))
                connect.commit()
                sg.popup("Updated!")
                
            elif event == "Reject Provider":
                c.execute("UPDATE Offered SET Status = 'Rejected' WHERE Offered.sid = ? AND Offered.provider_id = ?", (seid, proid))
                connect.commit()
                sg.popup("Updated!")

    
    

def list_availability_button(window, values):
    
    all_services = []
    alll = c.execute('SELECT sid, sname FROM Services')
    for row in alll:
        all_services.append(row)
        
    available_services = []
    ava = c.execute("SELECT sid, sname FROM Services WHERE Availability = 'Available'")
    for row in ava:
        available_services.append(row)

    unavailable_services = []
    unava = c.execute("SELECT sid, sname FROM Services WHERE Availability = 'Unavailable'")
    for row in unava:
        unavailable_services.append(row)
        
    if event == 'List Availability':
        chosen_availability = values['chosen_availability']
        if chosen_availability == "all_services":
            window.Element('chosen_service').Update(values=all_services)

        elif chosen_availability == "available_services":
            window.Element('chosen_service').Update(values=available_services)
                
        elif chosen_availability == 'unavailable_services':
            window.Element('chosen_service').Update(values=unavailable_services)
        else:
            sg.popup('Chose an availability filter')
        

            

def admin_details_button(values):
    service = values['chosen_service'][0]
    serviceid = service[0]
    

    detail_list = []
    a = c.execute('SELECT description, sid, category, sname, price, Availability FROM Services WHERE sid=?', (serviceid,))
    for row in a:
        detail_list.append(row)
    layout = [[sg.Text('Service Details')],
              [sg.Listbox(values=detail_list, size=(30, 6), key='details_of_service')],    
              [sg.Button('Close')]]
    
    
    popup_window = sg.Window('Details', layout, finalize=True)
    while True:
            event, _ = popup_window.read()
            if event == 'Close':
                break

    popup_window.close()
    
    
    
def admin_add_service(values):
    layout = [[sg.Text("Adding Service Panel")],
              [sg.Text('Service ID:', size=(10,1)), sg.Input(size=(10, 1), key='id')],
              [sg.Text('Service Name:', size=(10,1)), sg.Input(size=(10, 1), key='name')],
              [sg.Text('Description:', size=(10,1)), sg.Input(size=(10, 1), key='descrip')],
              [sg.Text('Cateory:', size=(10,1)), sg.Input(size=(10, 1), key='cat')],
              [sg.Text('Price:', size=(10,1)), sg.Input(size=(10, 1), key='price')],
              [sg.Text('Availability:', size=(10,1)), sg.Input(size=(10, 1), key='ava')],
              [sg.Button('Add'),sg.Button('Close')]
              ]
    
    popupwin = sg.Window('ADDING', layout, finalize=True)
    
    while True:
        event, values = popupwin.read()
        idd = values['id']
        nme = values["name"]
        des = values["descrip"]
        cate = values["cat"]
        pr = values["price"]
        avai = values["ava"]
        if event=='Add':
            c.execute("INSERT INTO Services VALUES(?, ?, ?, ?, ?, ?)", (des, idd, cate, nme, pr, avai))
            connect.commit()
            return sg.popup("Service Added")
        elif event=="Close":
            break
    
    popupwin.close()
    
    
def admin_update_service(values):
    s = values["chosen_service"][0]
    chosenservice = s[0]
    layout = [[sg.Text("Adding Service Panel")],
              [sg.Text('Service ID:', size=(10,1)), sg.Input(size=(10, 1), key='id')],
              [sg.Text('Service Name:', size=(10,1)), sg.Input(size=(10, 1), key='name')],
              [sg.Text('Description:', size=(10,1)), sg.Input(size=(10, 1), key='descrip')],
              [sg.Text('Cateory:', size=(10,1)), sg.Input(size=(10, 1), key='cat')],
              [sg.Text('Price:', size=(10,1)), sg.Input(size=(10, 1), key='price')],
              [sg.Text('Availability:', size=(10,1)), sg.Input(size=(10, 1), key='ava')],
              [sg.Button('Update'),sg.Button("Close")]
              ]
    popupwin = sg.Window('UPDATING', layout, finalize=True)
    while True:
        event, values = popupwin.read()
        idd = values['id']
        nme = values["name"]
        des = values["descrip"]
        cate = values["cat"]
        pr = values["price"]
        avai = values["ava"]
        if event=='Update':
            c.execute("UPDATE Services SET description = ? WHERE sid = ?", (des, chosenservice))
            c.execute("UPDATE Services SET sid = ? WHERE sid = ?", (idd, chosenservice))
            c.execute("UPDATE Services SET category = ? WHERE sid = ?", (cate, chosenservice))
            c.execute("UPDATE Services SET sname = ? WHERE sid = ?", (nme, chosenservice))
            c.execute("UPDATE Services SET price = ? WHERE sid = ?", (pr, chosenservice))
            c.execute("UPDATE Services SET Availability = ? WHERE sid = ?", (avai, chosenservice))
            connect.commit()
            return sg.popup("Service Updated")
        elif event=="Close":
            break
    
    popupwin.close()

def admin_delete_service(values):
    s = values['chosen_service'][0]
    service = s[0]
    
    c.execute('DELETE FROM Services WHERE sid=?', (service,))
    connect.commit()
    return sg.popup("Service Deleted")



def customer_window():
    all_services = []
    alll = c.execute('SELECT sid, sname FROM Services')
    for row in alll:
        all_services.append(row)
    
    
    
    layout = [[sg.Text('Welcome ' + login_user_name)],
              [sg.Text('Customer Panel')],
              [sg.Text("Filter Services:"), sg.Combo(['all_services', 'available_services', 'unavailable_services'], default_value='all_services', key='chosen_availability'), sg.Button('List Availability')],
              [sg.Listbox(values=all_services, size=(30, 6), key='chosen_service')],
              [sg.Button('Show My Cards'),sg.Button('Service Details'),sg.Button('Add To Cards')],
              [sg.Button('Logout')]
    ]
    return sg.Window('Customer Panel', layout)

def customer_service_detail_button(values):
    service = values['chosen_service'][0]
    serviceid = service[0]
    

    detail_list = []
    a = c.execute('SELECT description, sid, category, sname, price, Availability FROM Services WHERE sid=?', (serviceid,))
    for row in a:
        detail_list.append(row)
    layout = [[sg.Text('Service Details')],
              [sg.Listbox(values=detail_list, size=(30, 6), key='details_of_service')],    
              [sg.Button('Close')]]
    
    
    popup_window = sg.Window('Details', layout, finalize=True)
    while True:
            event, _ = popup_window.read()
            if event == 'Close':
                break

    popup_window.close()
    


def addingToCards(values):
    service = values['chosen_service'][0]
    serviceid = service[0]
    r = random.randint(1,100)
    c.execute("INSERT INTO booking VALUES(?, ?)", (r,"pending"))
    c.execute('INSERT INTO books (bid, customer_id, sid) VALUES (?, ?, ?)',
                   (r, login_user_id, serviceid))
    connect.commit()
    sg.popup("Service is added to your cards")
    return


def customer_seeing_their_cards(values):
    a = c.execute('SELECT sname, booking.bid, booking.status, Services.sid FROM Services, books, booking WHERE books.customer_id = ? AND books.sid = Services.sid AND booking.bid = books.bid' ,(login_user_id,))
    card_list = []
    for row in a:
        card_list.append(row)
    layout = [[sg.Text('Cards')],
              [sg.Listbox(values=card_list, size=(30, 6), key='service_in_cards')],    
              [sg.Text('Rating Point', size=(10,1)), sg.Input(size=(10, 1), key='rating')],
              [sg.Text('Comments:', size=(10,1)), sg.Input(size=(10, 1), key='comment')],
              [sg.Button('Close'),sg.Button("Update Booking Status"),sg.Button("Rate Provider")]]
    popup_window = sg.Window('Cards', layout, finalize=True)
    while True:
        event, values = popup_window.read()
        ser = values["service_in_cards"][0]
        r = values["rating"]
        com = values["comment"]
        rid = random.randint(5,50)
        chsn = ser[3]
        bb = ser[1]
        if event=="Update Booking Status":
            c.execute("UPDATE booking SET status = 'completed' WHERE booking.bid = ?", (bb,))
            connect.commit()
            sg.popup("Status Updated")
        elif event == "Rate Provider":
            c.execute("INSERT INTO Rates VALUES(?, ?, ?)", (rid, com, r))
            c.execute("INSERT INTO review VALUES(?, ?)", (rid, login_user_id))
            c.execute("INSERT INTO rate_applied VALUES(?, ?)", (rid, chsn))
            connect.commit()
            sg.popup("Rate has been given")
        elif event == 'Close':
            break

    popup_window.close()
    


    
# def view_services():
#     c.execute('SELECT sname FROM Services')
#     rows = c.fetchall()
#     c.close()
#     return rows

def button_login(values):
    global login_user_email
    global login_user_password
    global login_user_name
    global login_user_surname
    global login_user_id
    global login_user_type
    
    global window
    
    mail = values['e_mail']
    password = values['Password']
    
    if mail == '':
        sg.popup('E-Mail cannot be empty')
    elif password == '':
        sg.popup('Password cannot be empty')
    else:
        # checks if this is a valid user
        c.execute('SELECT e_mail, Password, Name, Surname, userid FROM User WHERE e_mail = ? AND Password = ?', (mail, password))
        row = c.fetchone()
        
    if row is None:
        sg.popup('ID or password is wrong!')
    else:
        # store user's information in global variables
        login_user_email = row[0]
        login_user_password = row[1]
        login_user_name = row[2]
        login_user_surname = row[3]
        login_user_id = row[4]
        
        
        #to determine if the user is a customer or admin
        c.execute('SELECT e_mail FROM Admins, User WHERE userid = admin_id AND e_mail = ?', (mail,))
        row_admin = c.fetchone()
        
        if row_admin is None:
            c.execute('SELECT e_mail FROM Customer, User WHERE userid = customer_id AND e_mail = ?', (mail,))
            row_customer = c.fetchone()
            if row_customer is None:
                c.execute("SELECT e_mail FROM Provider, User WHERE userid = prover_id AND e_mail = ?", (mail,))
                
                row_provider = c.fetchone()
                if row_provider is None:
                    
                    sg.popup('User type error!')
            
                else:
                    login_user_type = 'Provider'
                    sg.popup('Welcome, ' + login_user_name)
                    window.close()
                    window = provider_window()
                 
                    
            else:
                login_user_type = 'Customer'
                sg.popup('Welcome, ' + login_user_name)
                window.close()
                window = customer_window()
                
                
        else:
            # user is an admin
            login_user_type = 'Admin'
            sg.popup('Welcome, ' + login_user_name)
            window.close()
            window = admin_window()
            
window = login()

while True:
    event, values = window.read()
    if event == "Enter":
        button_login(values)
    elif event == "Add Service":
        admin_add_service(values)
    elif event == "Update Service":
        admin_update_service(values)
    elif event == "Delete Service":
        admin_delete_service(values)
    elif event == "Details":
        admin_details_button(values)
    elif event == 'Show My Cards':
        customer_seeing_their_cards(values)        
    elif event == 'Service Details':
        customer_service_detail_button(values)
    elif event == 'Add To Cards':
        addingToCards(values)
    elif event == "See the Provider List":
        admins_provider_list(values)
    elif event == "Bookings":
        provider_confirming_bookings(values)
    elif event == 'Close Window':
        window.close()
        customer_window()
    elif event == "See the approval-waiting Providers":
        admin_confirms_or_rejets_provider(values)
    elif event== "Offer Service":
        provider_offering_service_button(values)
    elif event == 'Register as Provider':
        provider_registering(values)
    elif event == 'List Availability':
        list_availability_button(window, values)
    elif event == "Close":
        window.close()
        admin_window()
        
    elif event == 'Logout':
        login_user_email = -1
        login_user_name = -1
        login_user_type = -1
        window.close()
        window = login()
    elif event == sg.WIN_CLOSED:
        break
        
window.close()
connect.commit()
connect.close()

        
        
            