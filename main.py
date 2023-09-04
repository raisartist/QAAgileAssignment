from flask import Flask, render_template, request
import sqlite3
from forms import customer_form, event_form

conn = sqlite3.connect('database.db')
print ("Opened database successfully");

# conn.execute('DROP TABLE IF EXISTS events')
conn.execute('CREATE TABLE IF NOT EXISTS customers (name VARCHAR UNIQUE, dateJoined TEXT, useCase TEXT, location TEXT)')
print ("Customers table created successfully");
conn.execute('CREATE TABLE IF NOT EXISTS events (name VARCHAR UNIQUE, location TEXT, dateStarted TEXT, durationMins INTEGER)')
print ("Events table created successfully");
conn.close()

app = Flask(__name__)
app.secret_key = "my super secret key for the app"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

# Customers

@app.route("/customers_database")
def customers_database():
    form = customer_form()
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    current = connection.cursor()
    current.execute("select * from customers")

    rows = current.fetchall(); 
    return render_template("customers_database.html", rows = rows, form=form)

@app.route("/delete_customer/<customer_name>", methods = ['POST', 'GET'])
def delete_customer(customer_name):
    if request.method == 'POST':
        try: 
            with sqlite3.connect("database.db") as connection:
                current = connection.cursor()
                current.execute("DELETE FROM customers WHERE name = (?)",(customer_name,) )
                
                connection.commit()
                message = "Customer record successfully deleted"
                isError = False
        except Exception as error:
            connection.rollback()
            message = str(error)
            isError = True
        
        finally:
            connection.close()
            return render_template("result.html",message = message, isError = isError)
            # flash(message)
            # return redirect(url_for("customers_database"))

@app.route("/update_customer/<name>/<dateJoined>/<location>/<useCase>")
def update_customer(name, dateJoined, location, useCase):
    form = customer_form()
    return render_template("update_customer.html", name = name, dateJoined = dateJoined, location = location, useCase = useCase, form = form)

@app.route("/update_set_customer/<customer_name>", methods = ['POST', 'GET'])
def update_set_customer(customer_name):
    form = customer_form(request.form)
    isValid = form.validate_on_submit()
    if isValid == True:
        if request.method == 'POST':
            try:
                name = form.name.data
                dateJoined = form.dateJoined.data
                useCase = form.useCase.data
                location = form.location.data
                with sqlite3.connect("database.db") as connection:
                        current = connection.cursor()
                        current.execute("UPDATE customers SET name = (?), dateJoined = (?), useCase = (?), location = (?) WHERE name = (?)",(name, dateJoined, useCase, location, customer_name) )
                        
                        connection.commit()
                        message = "Customer record successfully updated"
                        isError = False
            except Exception as error:
                connection.rollback()
                message = str(error)
                isError = True
            
            finally:
                connection.close()
                # flash(message)
                # return redirect(url_for("customers_database"))
                return render_template("result.html",message = message, isError = isError)
    else:
        return render_template("result.html",message = isValid, isError = True)

@app.route("/add_customer", methods = ['POST', 'GET'])
def add_customer():
    form = customer_form(request.form)
    isValid = form.validate_on_submit()
    if isValid == True:
        if request.method == 'POST':
            try:
                name = form.name.data
                dateJoined = form.dateJoined.data
                useCase = form.useCase.data
                location = form.location.data
                with sqlite3.connect("database.db") as connection:
                        current = connection.cursor()
                        current.execute("INSERT OR IGNORE INTO customers (name,dateJoined,useCase,location) VALUES (?,?,?,?)",(str(name),str(dateJoined),str(useCase),str(location)) )
                        
                        connection.commit()
                        message = "Customer record successfully added"
                        isError = False
            except Exception as error:
                connection.rollback()
                message = str(error)
                isError = True
            
            finally:
                connection.close()
                # flash(message)
                # return redirect(url_for("customers_database"))
                return render_template("result.html",message = message, isError = isError)
    else:
        return render_template("result.html",message = isValid, isError = True)

# Events

@app.route("/events_database")
def events_database():
    form = event_form()
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    current = connection.cursor()
    current.execute("select * from events")

    rows = current.fetchall(); 
    return render_template("events_database.html", rows = rows, form=form)

@app.route("/add_event", methods = ['POST', 'GET'])
def add_event():
    form = event_form(request.form)
    isValid = form.validate_on_submit()
    if isValid == True:
        if request.method == 'POST':
            try:
                name = form.name.data
                dateStarted= form.dateStarted.data
                durationMins = form.durationMins.data
                location = form.location.data
                with sqlite3.connect("database.db") as connection:
                        current = connection.cursor()
                        current.execute("INSERT OR IGNORE INTO events (name,dateStarted,durationMins,location) VALUES (?,?,?,?)",(str(name),str(dateStarted),str(durationMins),str(location)) )
                        connection.commit()
                        message = "Event record successfully added"
                        isError = False
            except Exception as error:
                connection.rollback()
                message = str(error)
                isError = True
            
            finally:
                connection.close()
                # flash(message)
                # return redirect(url_for("customers_database"))
                return render_template("result.html",message = message, isError = isError)
    else:
        return render_template("result.html",message = isValid, isError = True)

@app.route("/update_event/<name>/<dateStarted>/<location>/<durationMins>")
def update_event(name, dateStarted, location, durationMins):
    form = event_form()
    return render_template("update_event.html", name = name, dateStarted = dateStarted, location = location, durationMins = durationMins, form = form)

@app.route("/update_set_event/<event_name>", methods = ['POST', 'GET'])
def update_set_event(event_name):
    form = event_form(request.form)
    isValid = form.validate_on_submit()
    if isValid == True:
        if request.method == 'POST':
            try:
                name = form.name.data
                dateStarted = form.dateStarted.data
                durationMins = form.durationMins.data
                location = form.location.data
                with sqlite3.connect("database.db") as connection:
                        current = connection.cursor()
                        current.execute("UPDATE events SET name = (?), dateStarted = (?), durationMins = (?), location = (?) WHERE name = (?)",(name, dateStarted, durationMins, location, event_name) )
                        
                        connection.commit()
                        message = "Event record successfully updated"
                        isError = False
            except Exception as error:
                connection.rollback()
                message = str(error)
                isError = True
            
            finally:
                connection.close()
                # flash(message)
                # return redirect(url_for("customers_database"))
                return render_template("result.html",message = message, isError = isError)
    else:
        return render_template("result.html",message = isValid, isError = True)
    
@app.route("/delete_event/<event_name>", methods = ['POST', 'GET'])
def delete_event(event_name):
    if request.method == 'POST':
        try: 
            with sqlite3.connect("database.db") as connection:
                current = connection.cursor()
                current.execute("DELETE FROM events WHERE name = (?)",(event_name,) )
                
                connection.commit()
                message = "Event record successfully deleted"
                isError = False
        except Exception as error:
            connection.rollback()
            message = str(error)
            isError = True
        
        finally:
            connection.close()
            return render_template("result.html",message = message, isError = isError)
            # flash(message)
            # return redirect(url_for("customers_database"))
    
if __name__ == "__main__":
    app.run(debug=True)