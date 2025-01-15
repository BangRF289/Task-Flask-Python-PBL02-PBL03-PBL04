# from peewee import *
# from flask import Flask, render_template, request, url_for, redirect

# app = Flask(__name__)

# global appType 
# appType = 'Monolith'

# database = SqliteDatabase('carsweb.db')

# class BaseModel(Model):
#      class Meta:
#         database = database

# class TBCars(BaseModel):
#     carname = TextField()
#     carbrand = TextField()
#     carmodel = TextField()
#     carprice = TextField()

# def create_tables():
#     with database:
#         database.create_tables([TBCars])

# @app.route('/')
# def indeks():
#     return render_template('index.html', appType=appType)

# @app.route('/createcar')
# def createcar():
#     return render_template('createcar.html', appType=appType)

# @app.route('/createcarsave',methods=['GET','POST'])
# def createcarsave():
#     fName = request.form['carName']
#     fBrand = request.form['carBrand']
#     fModel = request.form['carModel']
#     fPrice = request.form['carPrice']

#     viewData = {
#         "name" : fName,
#         "brand" : fBrand,
#         "model" : fModel,
#         "price" : fPrice 
#     }

#     #simpan di DB
#     car_simpan = TBCars.create(
#         carname = fName,
#         carbrand = fBrand,
#         carmodel = fModel,
#         carprice = fPrice
#         )
#     return redirect(url_for('readcar'))

# @app.route('/readcar')
# def readcar():
#     rows = TBCars.select()
#     return render_template('readcar.html', rows=rows, appType=appType)

# @app.route('/updatecar')
# def updatecar():
#     return render_template('updatecar.html', appType=appType)

# @app.route('/updatecarform', methods=['POST'])
# def updatecarform():
#     car_id = request.form['carId']
#     car = TBCars.get_or_none(TBCars.id == car_id)
#     if car:
#         return render_template('updatecarform.html', car=car, appType=appType)
#     else:
#         return "Car not found", 404


# @app.route('/updatecarsave', methods=['POST'])
# def updatecarsave():
#     car_id = request.form['carId']
#     fName = request.form['carName']
#     fBrand = request.form['carBrand']
#     fModel = request.form['carModel']
#     fPrice = request.form['carPrice']

#     car = TBCars.get_or_none(TBCars.id == car_id)
#     if car:
#         car.carname = fName
#         car.carbrand = fBrand
#         car.carmodel = fModel
#         car.carprice = fPrice
#         car.save()
#         return redirect(url_for('readcar'))
#     else:
#         return "Car not found", 404

# @app.route('/deletecar')
# def deletecar():
#     return render_template('deletecar.html', appType=appType)

# @app.route('/deletecarsave', methods=['GET','POST'])
# def deletecarsave():
#     fName = request.form['carName']
#     car_delete = TBCars.delete().where(TBCars.carname==fName)
#     car_delete.execute()
#     return redirect(url_for('readcar'))

# @app.route('/searchcar', methods=['GET', 'POST'])
# def searchcar():
#     if request.method == 'POST':
#         search_query = request.form['searchQuery']
#         # Lakukan pencarian di database berdasarkan carname atau carbrand
#         rows = TBCars.select().where(
#             (TBCars.carname.contains(search_query)) | (TBCars.carbrand.contains(search_query))
#         )
#         return render_template('searchcar.html', rows=rows, appType=appType)
    
#     return render_template('searchcar.html', appType=appType)

# @app.route('/help')
# def help():
#     return "ini halaman Helps"


# if __name__ == '__main__':
#     create_tables()
#     app.run(
#         port =5010,
#         host='0.0.0.0',
#         debug = True
#         )


from peewee import *
from flask import Flask, render_template, request, url_for, redirect
import pandas as pd

app = Flask(__name__)

global appType 
appType = 'Monolith'

database = SqliteDatabase('carsweb.db')

class BaseModel(Model):
    class Meta:
        database = database

class TBCars(BaseModel):
    carname = TextField()
    carbrand = TextField()
    carmodel = TextField()
    carprice = TextField()

def create_tables():
    with database:
        database.create_tables([TBCars])

@app.route('/')
def indeks():
    return render_template('index.html', appType=appType)

@app.route('/createcar')
def createcar():
    return render_template('createcar.html', appType=appType)

@app.route('/createcarsave', methods=['POST'])
def createcarsave():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']

    # Simpan data ke database
    TBCars.create(
        carname=fName,
        carbrand=fBrand,
        carmodel=fModel,
        carprice=fPrice
    )
    return redirect(url_for('readcar'))

@app.route('/readcar')
def readcar():
    rows = TBCars.select()
    return render_template('readcar.html', rows=rows, appType=appType)

@app.route('/open_file', methods=['POST'])
def open_file():
    if 'file' not in request.files:
        return redirect(url_for('readcar'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('readcar'))

    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            TBCars.create(
                carname=row['Name'],
                carbrand=row['Brand'],
                carmodel=row['Model'],
                carprice=row['Price (USD)']
            )
    return redirect(url_for('readcar'))

@app.route('/updatecar')
def updatecar():
    return render_template('updatecar.html', appType=appType)

@app.route('/updatecarform', methods=['POST'])
def updatecarform():
    car_id = request.form['carId']
    car = TBCars.get_or_none(TBCars.id == car_id)
    if car:
        return render_template('updatecarform.html', car=car, appType=appType)
    else:
        return "Car not found", 404

@app.route('/updatecarsave', methods=['POST'])
def updatecarsave():
    car_id = request.form['carId']
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']

    car = TBCars.get_or_none(TBCars.id == car_id)
    if car:
        car.carname = fName
        car.carbrand = fBrand
        car.carmodel = fModel
        car.carprice = fPrice
        car.save()
        return redirect(url_for('readcar'))
    else:
        return "Car not found", 404

@app.route('/deletecar')
def deletecar():
    return render_template('deletecar.html', appType=appType)

@app.route('/deletecarsave', methods=['POST'])
def deletecarsave():
    fName = request.form['carName']
    car_delete = TBCars.delete().where(TBCars.carname == fName)
    car_delete.execute()
    return redirect(url_for('readcar'))

@app.route('/searchcar', methods=['GET', 'POST'])
def searchcar():
    if request.method == 'POST':
        search_query = request.form['searchQuery']
        rows = TBCars.select().where(
            (TBCars.carname.contains(search_query)) | (TBCars.carbrand.contains(search_query))
        )
        return render_template('searchcar.html', rows=rows, appType=appType)
    
    return render_template('searchcar.html', appType=appType)

@app.route('/help')
def help():
    return "ini halaman Helps"

if __name__ == '__main__':
    create_tables()
    app.run(
        port=5010,
        host='0.0.0.0',
        debug=True
    )
