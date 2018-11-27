from flask import render_template, request, url_for, redirect, flash, session, jsonify
import json

from FRA.models import Feature, User
from FRA import app, db

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        PASSWORD = str(request.form['password'])
        USERNAME = str(request.form['username'])

        try:
            user = User.query.filter_by(
                username=USERNAME, password=User.hash_password(PASSWORD)).first()
            if user:
                session['logged_in'] = True
                return redirect(url_for('list_features'))
            else:
                error = 'Invalid username or password'
        except:
            error = 'server not reachable'

    return render_template('login.html', error=error)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


@app.route('/')
@app.route('/list')
def list_features():
    if not session.get('logged_in', ''):
        return redirect(url_for('login'))
    result = []
    try:
        result = Feature.query.all()

        # map through result and get only whats needed
        result = list(map(lambda ft: {'id': ft.id, 'client': ft.client, 'priority': ft.client_priority,
                                      'target_date': ft.target_date, 'created_date': str(ft.created_date.date()), 'title': ft.title,
                                      'description': ft.description, 'product_area': ft.product_area, 'status': ft.status}, result))
    except:
        print('error fetching features')
    return render_template('list-features.html', features=result)


@app.route('/request', methods=['GET', 'POST'])
def request_features():
    if not session.get('logged_in', ''):
        return login()

    message = ''
    if request.method == "POST":
        product_area = request.form['product_area']
        target_date = request.form['target_date']
        client = request.form['client']
        priority_option = request.form['client_priority']
        title = request.form['title']
        description = request.form['description']

        try:
            priority_option = json.loads(priority_option)
            client_priority = priority_option[0]

            if len(priority_option) > 1:  # a chosen priority has been assigned
                Feature.reorder_priorities(client, client_priority)

            newFeature = Feature(title=title, description=description,
                                 product_area=product_area, target_date=target_date, client=client,
                                 client_priority=client_priority)
            db.session.add(newFeature)
            db.session.commit()
            message = " %s for %s was added successfully with priority %d" % (
                title, client, int(client_priority))
        except:
            print('error creating feature')

    return render_template('request-feature.html', message=message)


@app.route('/c_priority', methods=['GET'])
def getPriority():
    client = request.args.get('client', '')
    features = Feature.query.filter_by(client=client).all()
    features = list(map(lambda ft: (ft.client_priority, ft.title), features))
    return jsonify(features)