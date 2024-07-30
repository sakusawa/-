import os
from flask import Flask, request, redirect, render_template, flash # type: ignore
from werkzeug.utils import secure_filename # type: ignore
from tensorflow.keras.models import Sequential, load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np # type: ignore

classes = ["りんご","バナナ","赤かぶ","ピーマン","キャベツ","パプリカ（トウガラシっぽい）",
            "にんじん","カリフラワー","とうがらし","とうもろこし","きゅうり","なす",
            "にんにく","しょうが","ぶどう","青とうがらし","キウイ","レモン",
            "レタス","マンゴー","玉ねぎ","オレンジ","パプリカ","なし",
            "えんどう豆","パイナップル","ザクロ","じゃがいも","ラディッシュ","大豆",
            "ほうれん草","スイートコーン","さつまいも","とまと","かぶ","すいか"]
image_size = 50

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png", "gif"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "v_f_app.secrer_key"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

model = load_model("./model.h5")

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("ファイルがありません")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("ファイルがありません")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            img = image.load_img(filepath, target_size=(image_size, image_size))
            img = image.img_to_array(img)
            data = np.array([img])
            result = model.predict(data)[0]
            predicted = result.argmax()
            pred_answer = "これは『 " + classes[predicted] + " 』です。"
            return render_template("index.html", answer=pred_answer)

    return render_template("index.html", answer="")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)


        
