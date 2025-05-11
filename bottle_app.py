from bottle import route, run, post, request, redirect, response, template, TEMPLATE_PATH
from webbrowser import open
import sqlite3
import datetime
import os

abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_app_dir_path, 'templates')
TEMPLATE_PATH.insert(0, abs_views_path)

appPath = abs_app_dir_path


con = sqlite3.connect(os.path.join(appPath, 'webtech.db'))
cur = con.cursor()

# Megjegyzések a projektből
# query stringek változói stringként kapjuk meg a queryből


@route('/')
def main():
    logged = request.get_cookie('account_username', default=False)
    new_event = request.get_cookie('new_event', default=False)
    new_attendance = request.get_cookie('new_attendance', default=False)
    attend_error = request.get_cookie('attend_error', default=False)
    rm_attend = request.get_cookie('remove_attend', default=False)

    response.delete_cookie('new_event')
    response.delete_cookie('new_attendance')
    response.delete_cookie('attend_error')
    response.delete_cookie('remove_attend')

    your_events = []
    all_events = []

    if logged:
        accountID = request.get_cookie('account_ID')

        # ez kikeresi az adott user által felvett összes eventjének ID-ját és dátum ID-ját
        cur.execute('''SELECT event.ID, event.Date_ID FROM event WHERE event.ID IN
             (SELECT con.eventID FROM con WHERE con.userID = ?)''', (accountID,))
        result = cur.fetchall()

        current_date = datetime.date.today()

        for data in result:
            cur.execute('''SELECT date.Year, date.Month, date.Day FROM date WHERE date.ID = ?''', (data[1],))
            date = cur.fetchone()
            event_date = datetime.date(date[0], date[1], date[2])
            if event_date >= current_date and len(your_events) < 3:
                cur.execute('''SELECT user.Username, date.Year, date.Month, date.Day, event.Name, event.Location, event.Entry_fee
                            FROM ((event
                            INNER JOIN user ON event.Creator_ID = user.ID)
                            INNER JOIN date ON event.Date_ID = date.ID)
                            WHERE event.ID = ?''', (data[0],))
                result2 = cur.fetchone()
                date = str(datetime.date(result2[1], result2[2], result2[3]))
                data = [result2[0], date, result2[4], result2[5], result2[6], data[0]]
                your_events.append(data)

    else:
        pass

    cur.execute('''SELECT event.ID FROM event ORDER BY event.ID DESC LIMIT 1''')
    result = cur.fetchone()
    match result:
        case None:
            pass
        case _:
            maxID = int(result[0])
            eventID = 1
            current_date = datetime.date.today()
            while (eventID <= maxID) and (len(all_events) < 6):
                cur.execute('''SELECT event.Date_ID FROM event WHERE event.ID = ?''', (eventID,))
                dateID = cur.fetchone()[0]
                cur.execute('''SELECT date.Year, date.Month, date.Day FROM date WHERE date.ID = ?''', (dateID,))
                date = cur.fetchone()
                event_date = datetime.date(date[0], date[1], date[2])

                if event_date >= current_date:
                    cur.execute('''SELECT user.Username, date.Year, date.Month, date.Day, event.Name, event.Location, event.Entry_fee
                                        FROM ((event
                                        INNER JOIN user ON event.Creator_ID = user.ID)
                                        INNER JOIN date ON event.Date_ID = date.ID)
                                        WHERE event.ID = ?''', (eventID,))
                    result2 = cur.fetchone()
                    date = str(datetime.date(result2[1], result2[2], result2[3]))
                    data = [result2[0], date, result2[4], result2[5], result2[6], eventID]
                    all_events.append(data)

                eventID += 1

    return template('main.tpl',
                    logged=logged, new_event=new_event, new_attendance=new_attendance,
                    your_events=your_events, all_events=all_events,
                    attend_error=attend_error, rm_attend=rm_attend)


@route('/login')
def login():
    failed = bool(request.get_cookie('failed_login', default=False))
    new_account = request.get_cookie('new_account', default=False)
    reset_pass = request.get_cookie('reset_pass', default=False)
    attend_error = request.get_cookie('attend_error', default=False)

    response.delete_cookie('failed_login')
    response.delete_cookie('new_account')
    response.delete_cookie('reset_pass')
    response.delete_cookie('attend_error')
    return template('login.tpl', failed=failed, new_signup=new_account, reset_pass=reset_pass, attend_error=attend_error)


@post('/login')
def verify_login():
    username = request.forms.username
    password = request.forms.password

    data = [username, password]

    cur.execute('''SELECT user.ID FROM user WHERE Username = ? AND Password = ?''', data)
    ID = cur.fetchone()
    match ID:
        case None:
            response.set_cookie('failed_login', 'yes', max_age=10)
            redirect('/login')
        case _:
            response.set_cookie('account_ID', str(ID[0]))
            response.set_cookie('account_username', str(username))
            redirect('/')


@route('/sign_up')
def signup():
    error = request.get_cookie('signup_error', default='')
    response.delete_cookie('signup_error')
    return template('signup.tpl', error=error)


@post('/sign_up')
def signup():
    username = request.forms.username
    password = request.forms.pass1
    password2 = request.forms.pass2

    if password != password2:
        response.set_cookie('signup_error', "Passwords don't match!")
    elif len(password) < 4:
        response.set_cookie('signup_error', "Password is too short!")
    else:
        cur.execute('''SELECT user.ID FROM user WHERE user.Username = ?''', (username,))
        result = cur.fetchone()
        match result:
            case None:
                cur.execute('''SELECT user.ID FROM user ORDER BY user.ID DESC LIMIT 1''')
                result = cur.fetchone()
                match result:
                    case None:
                        user_ID = 1
                    case _:
                        user_ID = result[0] + 1

                date = str(datetime.date.today()).split('-')
                cur.execute('''SELECT date.ID FROM date WHERE Year = ? AND Month = ? AND Day = ?''', date)
                result = cur.fetchone()
                match result:
                    case None:
                        cur.execute('''SELECT date.ID FROM date ORDER BY date.ID DESC LIMIT 1''')
                        result = cur.fetchone()
                        match result:
                            case None:
                                date_ID = 1
                            case _:
                                date_ID = result[0] + 1
                        data = [date_ID, date[0], date[1], date[2]]
                        cur.execute('''INSERT INTO date VALUES(?,?,?,?)''', data)
                    case _:
                        date_ID = result[0]

                data = [user_ID, username, password, date_ID]
                cur.execute('''INSERT INTO user VALUES(?,?,?,?)''', data)
                con.commit()
                response.set_cookie('new_account', 'True')
                redirect('/login')

            case _:
                response.set_cookie('signup_error', "Username is already taken!")
    redirect('/sign_up')


@route('/help')
def recover():
    error = request.get_cookie('help_error', default='')
    response.delete_cookie('help_error')
    return template('help.tpl', error=error)


@post('/help')
def recover():
    username = request.forms.username
    new_pass_1 = request.forms.new_pass_1
    new_pass_2 = request.forms.new_pass_2

    if new_pass_2 != new_pass_1:
        response.set_cookie('help_error', "Passwords don't match!")
    elif len(new_pass_1) < 4:
        response.set_cookie('help_error', 'Password is too short!')
    else:
        cur.execute('''SELECT user.ID FROM user WHERE user.Username = ?''', (username,))
        result = cur.fetchone()
        match result:
            case None:
                response.set_cookie('help_error', 'There is no user with that username!')
            case _:
                ID = result[0]
                data = [new_pass_1, ID]
                cur.execute('''UPDATE user SET Password = ? WHERE user.ID = ?''', data)
                con.commit()
                response.set_cookie('reset_pass', 'True')
                redirect('/login')
    redirect('/help')
    

@route('/create')
def create():
    return template('create.tpl')


@post('/create')
def validate():
    cur.execute('''SELECT event.ID FROM event ORDER BY event.ID DESC LIMIT 1''')
    result = cur.fetchone()
    match result:
        case None:
            event_id = 1
        case _:
            event_id = result[0] + 1

    creator_id = request.get_cookie('account_ID')

    date = str(request.forms.date).split('-')
    cur.execute('''SELECT date.ID FROM date WHERE Year = ? AND Month = ? AND Day = ?''', date)
    result = cur.fetchone()
    match result:
        case None:
            # ha nincs benne a db-ben
            data = [date[0], date[0], date[1], date[0], date[1], date[2]]
            cur.execute('''SELECT date.ID FROM date
                            WHERE (Year > ?) OR (Year = ? AND Month > ?) OR (Year = ? AND Month = ? AND Day > ?)''', data)
            result = cur.fetchall()
            print(result)
            match result:
                case []:
                    # ha nincs nagyobb nála, az új elem a legnagyobb vagy az első elem
                    cur.execute('''SELECT date.ID FROM date ORDER BY date.ID DESC LIMIT 1''')
                    result = cur.fetchone()
                    if result is None:
                        date_ID = 1
                    else:
                        date_ID = result[0] + 1
                case _:
                    # ha van nála nagyobb, az utolsótól bumpolunk
                    for ID in reversed(result):
                        ID = ID[0]
                        data = [ID+1, ID]
                        cur.execute('''UPDATE date SET ID = ? WHERE ID = ?''', data)
                        cur.execute('''UPDATE user SET Date_ID = ? WHERE Date_ID = ?''', data)
                        cur.execute('''UPDATE event SET Date_ID = ? WHERE Date_ID = ?''', data)
                    date_ID = result[0][0]

            data = [date_ID, date[0], date[1], date[2]]
            cur.execute('''INSERT INTO date VALUES(?,?,?,?)''', data)
            con.commit()

        case _:
            date_ID = result[0]

    location = request.forms.location

    name = request.forms.name

    fee = request.forms.fee

    data = [event_id, creator_id, date_ID, location, fee, name]
    cur.execute('''INSERT INTO event VALUES(?,?,?,?,?,?)''', data)

    cur.execute('''SELECT con.ID FROM con ORDER BY con.ID DESC LIMIT 1''')
    result = cur.fetchone()

    match result:
        case None:
            ID = 1
        case _:
            ID = result[0] + 1

    data = [ID, creator_id, event_id]

    cur.execute('''INSERT INTO con VALUES(?,?,?)''', data)
    con.commit()
    response.set_cookie('new_event', 'True')
    redirect('/')


@route('/attend')
def attend():
    userID = request.get_cookie('account_ID', default=False)
    eventID = request.query.id

    if userID:
        data = [userID, eventID]
        cur.execute('''SELECT con.ID FROM con WHERE userID = ? AND eventID = ?''', data)
        result = cur.fetchone()
        match result:
            case None:
                cur.execute('''SELECT con.ID FROM con ORDER BY con.ID DESC LIMIT 1''')
                ID = cur.fetchone()[0] + 1
                data = [ID, userID, eventID]
                cur.execute('''INSERT INTO con VALUES(?,?,?)''', data)
                response.set_cookie('new_attendance', 'True')
                con.commit()
                redirect('/')
            case _:
                response.set_cookie('attend_error', 'True')
                redirect('/')
    else:
        response.set_cookie('attend_error', 'True')
        redirect('/login')


@route('/unattend')
def un_attend():
    userID = request.get_cookie('account_ID')
    eventID = request.query.id

    data = [userID, eventID]


    cur.execute('''SELECT con.ID FROM con WHERE con.userID = ? AND con.eventID = ?''', data)
    conID = cur.fetchone()[0]
    cur.execute('''DELETE FROM con WHERE con.ID = ?''', (conID,))

    cur.execute('''SELECT con.ID FROM con ORDER BY con.ID DESC LIMIT 1''')
    maxID = cur.fetchone()[0]

    while conID < maxID:
        data = [conID, conID+1]
        cur.execute('''UPDATE con SET ID = ? WHERE con.ID = ?''', data)
        conID += 1

    response.set_cookie('remove_attend', 'True')
    con.commit()
    redirect('/')

@route('/logout')
def logout():
    response.delete_cookie('account_username')
    response.delete_cookie('account_ID')

    redirect('/')

open('http://localhost:8080/')

run(host='localhost', port=8080)
