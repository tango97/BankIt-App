from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cid_generator import randN

# ###########################
# Database Configuration
# 
# Note: Kindly make sure the status is any one of the following: Active, Closed, Pending <Some Activity> 
# ###########################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer.db'
db = SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cid = db.Column(db.Integer(), nullable=False)
    ssnid = db.Column(db.Integer(), nullable=False)
    accountId = db.Column(db.Integer(), nullable=False)
    accountBalance = db.Column(db.Integer(), nullable=False)
    account_type = db.Column(db.String(1), nullable=False)
    status = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message = db.Column(db.Text, nullable=False)

    def __init__(self, cid, ssnid, accountId, accountBalance, account_type, status, message):
        self.cid = cid
        self.ssnid = ssnid
        self.accountId = accountId
        self.accountBalance = accountBalance
        self.account_type = account_type
        self.status = status
        self.message = message
        

    def __repr__(self):
        return "Customer id: "+str(self.cid)


class CustomerDetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cid = db.Column(db.Integer(), nullable=False)
    ssnid = db.Column(db.Integer(), nullable=False)
    customer_name = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    address = db.Column(db.String(10), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(10), nullable=False)

    def __init__(self, cid, ssnid, customer_name, age, address, state, city):
        self.cid = cid
        self.ssnid = ssnid
        self.customer_name = customer_name
        self.age = age
        self.address = address
        self.state = state
        self.city = city

    def __repr__(self):
        return "Customer id: "+str(self.cid)

# ###########################
# Initializing Dummy Data (Run in Python Terminal)
# ###########################

# from app import db
# from app import Customer
# db.create_all()

# db.session.add(Customer(cid=123456789, ssnid=518612602, accountId=553794213, accountBalance=10000, account_type='S', status='Pending Approval', message='Just Created'))
# db.session.add(Customer(cid=888888888, ssnid=372781404, accountId=310556749, accountBalance=2000, account_type='C', status='Active', message='Nothing'))
# db.session.add(Customer(cid=999999999, ssnid=177513079, accountId=500864310, accountBalance=500000, account_type='S', status='Pending Approval', message='NA'))
# db.session.add(Customer(cid=777777777, ssnid=196751448, accountId=546723186, accountBalance=1000000, account_type='S', status='Pending Approval', message='NA'))
# db.session.add(Customer(cid=666666666, ssnid=388288542, accountId=620951719, accountBalance=10, account_type='C', status='Closed', message='Closed due to low balance'))
# db.session.add(Customer(cid=777777777, ssnid=196751448, accountId=546723186, accountBalance=500, account_type='C', status='Active', message='Secondary Account of Type Current'))

# db.session.commit()

# ###########################
# Routing
# ###########################

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/CustomerStatus')
def CustomerStatus():
    all_customer = Customer.query.all()
    return render_template('customer-Status.html', rows=all_customer)

@app.route('/AccountStatus')
def AccountStatus():
    all_account = Customer.query.all()
    return render_template('account-Status.html', rows=all_account)

@app.route('/CustomerSearch', methods=['GET', 'POST'])
def CustomerSearch():
    if request.method == 'POST':
        if 'cid' in request.form:
            cid = request.form['cid']
            results = db.session.query(Customer).filter(Customer.cid == cid)
            return render_template('customer-Search.html', result=results)
        else:
            ssnid = request.form['ssnid']
            results = db.session.query(Customer).filter(Customer.ssnid == ssnid)
            return render_template('customer-Search.html', result=results)
    else:   
        return render_template('customer-Search.html')

@app.route('/AccountSearch', methods=['GET', 'POST'])
def AccountSearch():
    if request.method == 'POST':
        if 'accid' in request.form:
            accid = request.form['accid']
            results = db.session.query(Customer).filter(Customer.accountId == accid)
            return render_template('account-Search.html', result=results)
        else:
            cid = request.form['cid']
            results = db.session.query(Customer).filter(Customer.cid == cid)
            return render_template('account-Search.html', result=results)
    else:   
        return render_template('account-Search.html')

@app.route('/createcustomer', methods=['GET', 'POST'])
def Createcustomer():
    cid = int(randN())
    print(cid)
    # rendered = render_template('create-customer.html', cid=cid) 
    if request.method == 'POST':
        if 'ssnid' in request.form:
            ssnid = int(request.form['ssnid'])
            customer_name = request.form['customer_name']
            age = int(request.form['age'])
            address = request.form['address']
            state = request.form['state']
            city = request.form['city']
            
            # inserting data
            db.create_all()
            db.session.add(CustomerDetails(cid=cid, ssnid=ssnid, customer_name=customer_name, age=age, address=address, state=state, city=city))
            db.session.commit()
            return render_template('create-customer.html')
        else:
            return render_template('create-customer.html') 
    else:
        return render_template('create-customer.html') 


@app.route('/addaccount', methods =['GET','POST'])
def Addaccount():  
    if request.method == 'POST':
        if 'cid' in request.form:
            cid = int(request.form['cid'])
            account_type = request.form['account_type']
            accountBalance = request.form['accountBalance']

            results = db.session.query(CustomerDetails).filter(CustomerDetails.cid==cid)
            for row in results:
                ssnid = row.ssnid
            accountId = int(randN())
            db.session.add(Customer(cid=cid, ssnid=ssnid, accountId=accountId, accountBalance=accountBalance, account_type=account_type, status='Pending Approval', message='Just Created'))
            db.session.commit()
            return render_template('create-account.html')
        else:
            return render_template('create-account.html')

        
    else:
        return render_template('create-account.html')

@app.route('/updatecustomer', methods =['GET','POST'])
def UpdateCustomer(): 
    if request.method == 'POST':
        if 'cid' in request.form:
            cid = int(request.form['cid'])
            customer_name = request.form['customer_name']
            address = request.form['address']
            age = int(request.form['age'])

            results = db.session.query(CustomerDetails).filter(CustomerDetails.cid == cid)
            print(results[0])
            for row in results:
                row.customer_name = customer_name
                row.address = address
                row.age = age
            db.session.commit()
            return render_template('update-customer.html')
        else:
            return render_template('update-customer.html')
    else:
        return render_template('update-customer.html')


@app.route('/deletecustomer', methods =['GET','POST'])
def DeleteCustomer(): 
    if request.method == 'POST':
        if 'cid' in request.form:
            cid = int(request.form['cid'])
            db.session.query(Customer).filter(Customer.cid == cid).delete()
            db.session.query(CustomerDetails).filter(CustomerDetails.cid == cid).delete()
            db.session.commit()
            return render_template('delete-customer.html')
        else:
            return render_template('delete-customer.html')
    else:
        return render_template('delete-customer.html')


if __name__ == '__main__':
    app.run(debug=True)
