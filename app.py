from flask import Flask, render_template, request, redirect
import pickle
import warnings
import re
import firebase_admin
from firebase_admin import credentials, db, auth
warnings.filterwarnings('ignore')


# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://healthanalyzer-ef20f-default-rtdb.firebaseio.com/'
})

# Create an instance of the Flask class
app = Flask(__name__)


#Login Page Route as Landing Page
@app.route('/')
def landing():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']

        try:
            # Authenticate the user and create a custom token
            user = auth.get_user_by_email(email)
            auth_token = auth.create_custom_token(user.uid)
            return redirect('/home')
        except auth.UserNotFoundError:
            return "<script>alert('User with the provided email does not exist.'); window.location.href='/login';</script>"
        except Exception as e:
             # Return a generic error message without exposing the specific error details
            return f"<script>alert('An error occurred: {str(e)}'); window.location.href='/login';</script>"


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if not re.match(r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*[\W_]).{8,}$', password):
            return "<script>alert('Password must be at least 8 characters long and contain at least one number, one letter, and one special character.'); window.location.href='/signup';</script>"

        try:
            user = auth.get_user_by_email(email)
            return "<script>alert('User with the provided email already exists.'); window.location.href='/signup';</script>"
        except auth.UserNotFoundError:
            # Create a new user if the email doesn't exist
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            return redirect('/')


# Home route        
@app.route('/home')
def home():
    return render_template('home.html',)


# Diabetes Psge Route
@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')

# Load Pickle File
with open('model/diabetes_model.pkl', 'rb') as file:
    model1 = pickle.load(file)

@app.route('/predict_diabetes', methods=['POST'])
def predict_diabetes():
    features = [float(x) for x in request.form.values()]
    prediction = model1.predict([features])
    if prediction[0] == 0:
        result = 'DOES NOT HAVE DIABETES'
    else:
        result = 'HAS DIABETES'
    return render_template('result.html', prediction=result)


# Heart_disease Page Route
@app.route('/heart_disease')
def heart_disease():
    return render_template('heart_disease.html')

# Load Pickle File
with open('model/heart_model.pkl', 'rb') as file:
    model3 = pickle.load(file)

@app.route('/predict_heart_disease', methods=['POST'])
def predict_heart_disease():
    features = [float(x) for x in request.form.values()]
    prediction = model3.predict([features])
    if prediction[0] == 0:
        result = 'DOES NOT HAVE HEART DISEASE'
    else:
        result = 'HAS HEART DISEASE'
    return render_template('result.html', prediction=result)


# Breast Cancer PAge Route
@app.route('/breast_cancer')
def breast_cancer():
    return render_template('breast_cancer.html')

# Load Pickle File
with open('model/breast_cancer_model.pkl', 'rb') as file:
    model2 = pickle.load(file)

@app.route('/predict_breast_cancer', methods=['POST'])
def predict_breast_cancer():
    features = [float(x) for x in request.form.values()]
    prediction = model2.predict([features])
    if prediction[0] == 0:
        result = 'DOES NOT HAVE BREAST CANCER'
    else:
        result = 'HAS BREAST CANCER'
    return render_template('result.html', prediction=result)


# Guide Page Route
@app.route('/guide')
def guide():
    return render_template('guide.html',)

@app.route('/guide_diabetes')
def guide_diabetes():
    return render_template('guide_diabetes.html',)

@app.route('/guide_heart')
def guide_heart():
    return render_template('guide_heart.html',)

@app.route('/guide_breast')
def guide_breast():
    return render_template('guide_breast.html',)


# Get a reference to the Firebase Realtime Database
ref = db.reference('contacts')

# Define a route for the contact form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save the form data to the Firebase Realtime Database
        new_contact = ref.push()
        new_contact.set({
            'name': name,
            'email': email,
            'message': message
        })

        return "<script>alert('Thank you for your message!'); window.location.href='/home';</script>"
    'Thank you for your message. If you heve any Quary we will Contact you soon'
    return render_template('contact.html')

        
if __name__ == '__main__':
    app.run(debug=True)