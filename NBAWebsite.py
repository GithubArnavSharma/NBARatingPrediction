from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
from scipy import stats

model_rating = pickle.load(open('C:/Users/14086/Desktop/WebsiteNBA/model_rating.sav', 'rb'))
model_salary = pickle.load(open('C:/Users/14086/Desktop/WebsiteNBA/model_salary.sav', 'rb'))
all_stats = pd.read_csv('C:/Users/14086/Desktop/WebsiteNBA/all_stats.csv')

def predict2kRating(data):
  pred = np.array(model_rating.predict(data)).reshape(-1,)
  return int(pred[0])

def predictSalary(data):
  pred = np.array(model_salary.predict(data)).reshape(-1,)
  return int(pred[0])

def rating2percentile(rating):
  all_ratings = np.array(all_stats['Rating'])
  percentile = stats.percentileofscore(all_ratings, rating)
  if percentile > 99 and percentile < 100: percentile = 99

  return int(percentile)

def salary2percentile(salary):
  all_salaries = np.array(all_stats['Salary'])
  percentile = stats.percentileofscore(all_salaries, salary)
  if percentile > 99 and percentile < 100: percentile = 99

  return int(percentile)

app = Flask(__name__)


@app.route('/')
def man():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def home():
    data = []
    for letter in 'abcdefghijk':
        data.append(request.form[letter])
    arr = np.array([[float(d) for d in data]])
   
    rating = predict2kRating(arr)
    ratingPercentile = rating2percentile(rating)
    salary = predictSalary(arr)
    salaryStr = '{:,}'.format(salary)
    salaryPercentile = salary2percentile(salary) 

    return render_template('after.html', r=rating, rp=ratingPercentile, s=salaryStr, sp=salaryPercentile)


if __name__ == "__main__":
    app.run(debug=True)
