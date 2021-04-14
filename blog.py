from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,validators,PasswordField,BooleanField,RadioField
app = Flask(__name__)
app.secret_key="eellidokuz"
app.config["MYSQL_HOST"] ="localhost"
app.config["MYSQL_USER"] ="root"
app.config["MYSQL_PASSWORD"] =""
app.config["MYSQL_DB"]="hastalar"
app.config["MYSQL_CURSORCLASS"] ="DictCursor"
mysql=MySQL(app)
class hastaform(Form):
    yas=StringField("Yaşınızı Girin",validators=(validators.DataRequired(),))
    cinsiyet=RadioField("Cinsiyetinizi Seçin", choices=["Kadın","Erkek"],validators=(validators.DataRequired(),))
    alkol=BooleanField('Alkol Kullanıyorum')
    kahve=BooleanField('Kahve Kullanıyorum')
    sut=BooleanField('Süt ve Süt Ürünleri Tüketiyorum')
    mvit=BooleanField('Multivitamin Takviyesi Alıyorum')
    lif=BooleanField('Lifli Gıdaları Bol Tüketiyorum')
    balik=BooleanField('Balık Tüketiyorum')
    et=BooleanField('İşlenmiş Et (sucuk,sosis) Tüketiyorum')
    diyabet=BooleanField('Diyabet Hastasıyım')
    demir=BooleanField('Demir İçeren (yumurta,kuru üzüm,kırmızı et) Öaddeler Tüketiyorum')
    zinco=BooleanField('Çinko Takviyesi Alıyorum')
    sigara=BooleanField('Sigara İçiyorum')

@app.route("/")
def index():
    return render_template("anasayfa.html")
@app.route("/iletisim")
def iletisim():
    return render_template("iletisim.html")
@app.route("/akademik")
def akademik():
    return render_template("akademik.html")
@app.route("/tarama_testi",methods=["GET","POST"])
def tarama_testi():
    form=hastaform(request.form)
    if request.method=="POST" and form.validate():
        a=1
        yas=form.yas.data
        cinsiyet=form.cinsiyet.data
        if form.alkol.data:
            a*=1.36
        if form.kahve.data:
            a*=0.95
        if form.sut.data:
            a*=0.4
        if form.mvit.data:
            a*=0.7
        if form.lif.data:
            a*=0.53
        if form.balik.data:
            a*=0.69
        if form.et.data:
            a*=1.24
        if form.diyabet.data:
            a*=1.38
        if form.demir.data:
            a*=0.24
        if form.zinco.data:
            a*=0.4
        if form.sigara.data:
            a*=1.18
        a=round(a,3)
        cursor=mysql.connection.cursor()
        yazdır=("INSERT INTO hastalar(cinsiyet,yas,risk) VALUES (%s,%s,%s)")
        cursor.execute(yazdır,(cinsiyet,yas,a))
        mysql.connection.commit()
        flash("Risk Değeriniz:  "+str(a),"success")
        return redirect(url_for("index"))
    else:
        return render_template("tarama.html",form=form)
if __name__ =="__main__":
    app.run(debug=True)

