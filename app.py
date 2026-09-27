from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB = 'patient_records.db'


def get_connection():
    return sqlite3.connect(DB, timeout=10)


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            dob TEXT,
            gender TEXT,
            phone TEXT,
            email TEXT,
            address TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            specialization TEXT,
            phone TEXT,
            email TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id TEXT PRIMARY KEY,
            patient_name TEXT,
            doctor_name TEXT,
            date TEXT,
            time TEXT,
            reason TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            department_id TEXT PRIMARY KEY,
            department_name TEXT NOT NULL,
            head_doctor TEXT,
            location TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            prescription_id TEXT PRIMARY KEY,
            patient_name TEXT,
            doctor_name TEXT,
            medicine TEXT,
            dosage TEXT,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template('index.html')


# ---------------- PATIENTS ----------------

@app.route('/patients', methods=['GET', 'POST'])
def patients():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute('''
            INSERT INTO patients
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form['patient_id'],
            request.form['name'],
            request.form['dob'],
            request.form['gender'],
            request.form['phone'],
            request.form['email'],
            request.form['address']
        ))

        conn.commit()
        conn.close()
        return redirect('/patients')

    cursor.execute('SELECT * FROM patients')
    data = cursor.fetchall()
    conn.close()

    return render_template('patients.html', patients=data)


# ---------------- DOCTORS ----------------

@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute('''
            INSERT INTO doctors VALUES (?, ?, ?, ?, ?)
        ''', (
            request.form['doctor_id'],
            request.form['name'],
            request.form['specialization'],
            request.form['phone'],
            request.form['email']
        ))

        conn.commit()
        conn.close()
        return redirect('/doctors')

    cursor.execute('SELECT * FROM doctors')
    data = cursor.fetchall()
    conn.close()

    return render_template('doctors.html', doctors=data)


# ---------------- APPOINTMENTS ----------------

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute('''
            INSERT INTO appointments VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            request.form['appointment_id'],
            request.form['patient_name'],
            request.form['doctor_name'],
            request.form['date'],
            request.form['time'],
            request.form['reason']
        ))

        conn.commit()
        conn.close()
        return redirect('/appointments')

    cursor.execute('SELECT * FROM appointments')
    data = cursor.fetchall()
    conn.close()

    return render_template('appointments.html', appointments=data)


# ---------------- DEPARTMENTS ----------------

@app.route('/departments', methods=['GET', 'POST'])
def departments():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute('''
            INSERT INTO departments VALUES (?, ?, ?, ?)
        ''', (
            request.form['department_id'],
            request.form['department_name'],
            request.form['head_doctor'],
            request.form['location']
        ))

        conn.commit()
        conn.close()
        return redirect('/departments')

    cursor.execute('SELECT * FROM departments')
    data = cursor.fetchall()
    conn.close()

    return render_template('departments.html', departments=data)


# ---------------- PRESCRIPTIONS ----------------

@app.route('/prescriptions', methods=['GET', 'POST'])
def prescriptions():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute('''
            INSERT INTO prescriptions VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            request.form['prescription_id'],
            request.form['patient_name'],
            request.form['doctor_name'],
            request.form['medicine'],
            request.form['dosage'],
            request.form['date']
        ))

        conn.commit()
        conn.close()
        return redirect('/prescriptions')

    cursor.execute('SELECT * FROM prescriptions')
    data = cursor.fetchall()
    conn.close()

    return render_template('prescriptions.html', prescriptions=data)


if __name__ == '__main__':
    app.run(debug=True)
