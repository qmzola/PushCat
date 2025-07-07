from flask import Flask,request

app = Flask(__name__)

@app.route('/webhook')
def hello_world():
    return 'Hello, World!'
@app.route('/')
def home() :
    return '<p>This a home page</p>'

#webHook客户端入口
@app.post('/test/webhook')
def webHookcCient():
    data=request.json
    print("Received webhook data:",data)
    return 'Created',201




if __name__ == '__main__':
    app.run(debug=True)