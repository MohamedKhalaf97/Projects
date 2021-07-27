from flask import Flask, render_template, request
import joblib


app = Flask(__name__)

model = joblib.load('models/Model.h5')
scaler = joblib.load('models/scaler.h5')


Warehouse_blocks = ["B" , "C" , "D" ,"F"]
Mode_of_Shipments = ['Road' , "Ship"]
Product_importances = ["low" , "medium"]
Genders = ["M"]


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():

    inp_data = [
        request.args.get("Customer_care_calls") ,
        request.args.get("Customer_rating") ,
        request.args.get("Cost_of_the_Product") ,
        request.args.get("Prior_purchases") ,
        request.args.get("Discount_offered") ,
        request.args.get("Weight_in_gms") ]




    W_B  = [0 for i in range(4)]

    M_Sh  = [0 for i in range(2)]

    P_I  = [0 for i in range(2)]

    G    = [0]


    try :
        W_B[Warehouse_blocks.index(request.args.get("Warehouse_block"))] = 1
        
    except :
        pass


    try :
        M_Sh[Mode_of_Shipments.index(request.args.get("Mode_of_Shipment"))] = 1
        
    except :
        pass


    try :
        P_I[Product_importances.index(request.args.get("Product_importance"))] = 1
        
    except :
        pass


    try :
        G[Genders.index(request.args.get("Gender"))] = 1
        
    except :
        pass

    inp_data+=W_B
    inp_data+=M_Sh
    inp_data+=P_I
    inp_data+=G




    inp_data = [int(n) for n in inp_data]



    reachedOnTime = model.predict(scaler.transform([inp_data]))[0]



    return render_template("index.html" , reachedOnTime = reachedOnTime)
    




if __name__ == '__main__':
    app.run(debug=True , host="127.0.0.1")