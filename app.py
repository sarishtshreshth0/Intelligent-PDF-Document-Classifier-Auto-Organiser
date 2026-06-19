import pickle, os, pdfplumber
from flask import Flask, redirect , render_template , request

app = Flask(__name__)

path_name = 'Upload'
app.config["UPLOAD_FOLDER"] = path_name
os.makedirs(path_name , exist_ok = True)




with open('model.pkl' , 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl' , 'rb') as f:
    vectorizer = pickle.load(f)

@app.route("/")
def home():
    return render_template(
        "index.html",
        folders=final_list
    )

final_list = {}
@app.route("/upload" , methods = ['GET' , 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if "file" not in request.files:
            return "No file selected"
        if file.filename == "":
            return "No file selected"
        filepath = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    file.filename
                )
        data = ''
        file.save(filepath)
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages[:30]:
                text = page.extract_text()
                if text:
                    data = data + ' ' + text
        vectorized_file = vectorizer.transform([data])
        model_file = model.predict(vectorized_file)[0]
        if model_file not in final_list:
            final_list[model_file] = [file.filename]
        else:
            final_list[model_file].append(file.filename)
        print(final_list)
        return redirect('/')
    return render_template("index.html", folders = final_list)
  


if __name__ == '__main__':
    app.run(host = '0.0.0.0' , port = 5000 , debug = True)
