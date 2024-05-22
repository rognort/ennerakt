from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import yaml
import os


app = Flask(__name__)
app.secret_key = 'tajne-heslo'

i = 0

#file_path = os.path.join("/home/ennerakt/web", "kultury.yaml")
file_path = os.path.join("C:\MSI\web", "kultury.yaml")


seznam_kultur = []
with open(file_path, "r", encoding='utf-8') as file:
    for dokument in yaml.safe_load_all(file):
        # Zpracování každého dokumentu
        seznam_kultur.append(dokument[i])

kosik = {'kultura':'','podkultura':'','xperku':[]}

kulist = [ 'Lavra','Měšťan','Císařský',
          'Lostorvan','Seveřan','Tajanec',
           'Jižan','Bránijec','Mura',
           'Vran','Starší']

kulist_en = ['lavra','mestan','cisarsky',
    'lostorvan','severan','tajanec','jizan',
    'branijec','mura','vran','starsi']

kuzip = list(zip(kulist_en,kulist))


#hlavnistrany
#_________________________________________________________

@app.route('/')
@app.route('/uvod')
def uvod():
    return render_template('uvod.html') #kuzip=kuzip")

@app.route('/kultury')
def kultury():
    return render_template('kultury.html', kulist = kulist, kulist_en = kulist_en, kuzip=kuzip)

@app.route('/mapa')
def mapa():
    return render_template('mapa.html',kuzip=kuzip)

@app.route('/postava/')
def postava():
    if 'title1' not in session:
        session['content_changed'] = 'false'
    if 'title1' not in session:
        session['title1'] = 'Tvoje postava'
    if 'title2' not in session:
        session['title2'] = '...'
    if 'title3' not in session:
        session['title3'] = '...'
    if 'title4' not in session:
        session['title4'] = '...'
    if 'title5' not in session:
        session['title5'] = '...'
    if 'title6' not in session:
        session['title6'] = '...'
    kosik = session.get('kosik', {})
    return render_template('postava.html', kosik = kosik,kuzip =  kuzip)

@app.route('/zkouska')
def zkouska():
    return render_template('zkouska.html')

#metody
#___________________

@app.route('/uloz', methods=['POST'])
def uloz():
    # Initialize or retrieve the shopping cart from the session
    kosik = session.get('kosik', {})

    # Assuming the form sends multiple key-value pairs with unique identifiers
    for i in range(1, 3):  # Adjust the range based on the number of key-value pairs
        key = request.form.get(f'key{i}')
        value = request.form.get(f'value{i}')


        kosik[key] = value

    # Save the cart back to the session
    session['kosik'] = kosik

    # Respond with a success status
    return '', 204  # No content to send back

@app.route('/smaz', methods=['POST'])
def smaz():
    session['kosik'] = {'kultura': '', 'podkultura': '', 'xperku': []}
    # Reset each contenteditable field with its own specific placeholder
    session['title1'] = 'Tvoje postava'
    session['title2'] = '...'
    session['title3'] = '...'
    session['title4'] = '...'
    session['title5'] = '...'
    session['title6'] = '...'
    # Redirect to the URL for the 'postava' route
    return redirect(url_for('postava'))

@app.route('/smazperky', methods=['POST'])
def smazperky():
    session['kosik']['xperku'] = []
    session.modified = True
    return redirect(url_for('postava'))

@app.route("/perks", methods=["POST"])
def perks():
    key = 'xperku'
    vybrane_perks = request.form.getlist('perks')  # Získá seznam všech vybraných perků
    kosik = session.get('kosik', {})
    kosik.setdefault(key, [])  # Přidá seznam, pokud ještě neexistuje
    kosik[key].extend(vybrane_perks)  # Přidá všechny vybrané perků do seznamu
    kosik[key] = list(set(kosik[key]))
    session['kosik'] = kosik
    return '', 204

@app.route('/save-title', methods=['POST'])
def save_title():
    data = request.get_json()
    if not data:
        print("No data received")
        return jsonify({"error": "No data received"}), 400

    session[data['key']] = data['title']
    print(f"Data received for {data['key']}: {data['title']}")
    return jsonify({"key": data['key'], "status": "saved successfully"})

@app.route('/get-title', methods=['GET'])
def get_title():
    key = request.args.get('key', '')  # Get the key from the query parameter
    return session.get(key, '')  # Return the value associated with the key or empty if not found

#kultury všecky
#___________________________________
@app.route(f'/kultury/lavra')
def lavra():
    return render_template(f'kult_temp/lavra.html', culture_dict = seznam_kultur[0]['lavra_dict'], kuzip =  kuzip)


@app.route(f'/kultury/mestan')
def mestan():
    return render_template(f'kult_temp/mestan.html', culture_dict = seznam_kultur[1]['mestan_dict'], kuzip =  kuzip)

@app.route(f'/kultury/cisarsky')
def cisarsky():
    return render_template(f'kult_temp/cisarsky.html', culture_dict = seznam_kultur[2]['cisarsky_dict'], kuzip =  kuzip)

@app.route(f'/kultury/severan')
def severan():
    return render_template(f'kult_temp/severan.html', culture_dict = seznam_kultur[3]['severan_dict'], kuzip =  kuzip)

@app.route(f'/kultury/tajanec')
def tajanec():
    return render_template(f'kult_temp/tajanec.html', culture_dict = seznam_kultur[4]['tajanec_dict'], kuzip =  kuzip)

@app.route(f'/kultury/jizan')
def jizan():
    return render_template(f'kult_temp/jizan.html', culture_dict = seznam_kultur[5]['jizan_dict'], kuzip =  kuzip)

@app.route(f'/kultury/branijec')
def branijec():
    return render_template(f'kult_temp/branijec.html', culture_dict = seznam_kultur[6]['branijec_dict'], kuzip =  kuzip)

@app.route(f'/kultury/mura')
def mura():
    return render_template(f'kult_temp/mura.html', culture_dict = seznam_kultur[7]['mura_dict'], kuzip =  kuzip)

@app.route(f'/kultury/starsi')
def starsi():
    return render_template(f'kult_temp/starsi.html', culture_dict = seznam_kultur[8]['starsi_dict'], kuzip =  kuzip)

@app.route(f'/kultury/vran')
def vran():
    return render_template(f'kult_temp/vran.html', culture_dict = seznam_kultur[9]['vran_dict'], kuzip =  kuzip)

@app.route(f'/kultury/lostorvan')
def lostorvan():
    return render_template(f'kult_temp/lostorvan.html', culture_dict = seznam_kultur[10]['lostorvan_dict'], kuzip =  kuzip)


#___________________________________
#konec kultur



if __name__ == '__main__':
    app.run(port=5000, debug=True)
