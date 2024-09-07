# Simple Database Application of Website "Armut"

## Summary
In this project, we are developing a simple database application of "Armut" website 
using Phyton and SQLite.
#### Preperation Stage:
An Entity/Relationship diagram was constructured, and then it 
was translated into actual tables in SQLite by using SQLite Studio.
#### Main Stage:
In order to build a User Interface, the data was extracted from the created database by using possible SQL queries with Python (SQLite3 library).
Extracted data and built tables were connected together in a menu system 
using PySimpleGUI. For example, there are prepared screens that allow the user to manipulate 
(insert, update, and delete tuples) the data in our tables, as well as other screens that let the 
user execute some meaningful queries.

## Objective:
Uploaded "User Interface Code.py" file includes all Python, and SQL codes that used for building User Interface. That file shows that project owner is 
proficient in effectively integrating SQL queries with Python, utilizing libraries such as sqlite3.

## Functionalities:
When "User Interface Code.py", and "Project.db" is at same location in PC, and "User Interface Code.py" is executed, User Interface can perform these funcionailities:

* Log in to the system as an admin. Add service information into the system (with
 service ID, description, category, price, and service name). View the list of services
 available, and by selecting them individually, see their details in a new window. Click
 on one service and update its properties. Delete one service from the system. Log out
 and log in as a customer. List all the services. Select one and see its details in a
 separate window. Choose one service and add it to your cart. Then, go and check your
 cart.

* Log in to the system as a provider and register yourself in the system. Register with
 your name, surname, email address, password, and phone number. You should enter
 the services that you will offer and wait for confirmation from admins. You need to
 see your application for registration to the system, and it should be “Pending”
 initially. Log out and log in as admin. See the approval-waiting providers. Show that
 you can approve and reject one provider. Log out and log in as a customer. See the list
 of services and choose one. After choosing it, add it to the cart, select a provider, and
 enter the service date. Once you complete your booking order, the status of your
 booking request becomes “Pending,” see this in your booking history. Log out and log
 in as a provider. Show that you can accept or reject a booking (show them with at
 least one example). Log out and log in as a customer, check your booking history, and
 show the update in the booking status (“Confirmed”/”Rejected”).

* Log in to the system as a customer. Change the status of your “Confirmed” booking
 orders to “Completed.” Review your provider based on the service. There should be a
 comment and rating (from 0 to 10). Once you complete your review, the provider's
 rating changes. Initially, the ranking of a provider is null, but after a review, the rating
 score of the provider becomes the average of ratings. Log out and log in as an admin.
 See the list of providers. Disconfirm the providers with low service scores (rating
 averages). See the updated list of confirmed providers.

