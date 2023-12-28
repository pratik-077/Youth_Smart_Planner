from flask import Flask, request, render_template
import os
import re
os.environ['OPENAI_API_KEY'] = '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'
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain


app = Flask(__name__)

llm_resto = OpenAI(temperature=0.6)


prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height','step_count','heart_rate','caloric_expenditure', 'veg_or_nonveg', 'disease', 'region', 'allergics', 'foodtype'],
    template="Diet Recommendation System:\n"
             "I want you to recommend 6 healthy restaurants names, 6 healthy breakfast names, 6 healthy dinner names, and 6 more specific workout names, "
             "based on the following criteria:\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight}\n"
             "Person height: {height}\n"
             "Person daily step count: {step_count}\n"
             "Person heart rate: {heart_rate}\n"
             "Person caloric expenditure: {caloric_expenditure}\n"
             "Person veg_or_nonveg: {veg_or_nonveg}\n"
             "Person generic disease: {disease}\n"
             "Person region: {region}\n"
             "Person allergics: {allergics}\n"
             "Person foodtype: {foodtype}."
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods = ['POST', 'GET'])
def recommend():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        step_count = request.form['step_count']
        heart_rate = request.form.get('heart_rate',False)
        caloric_expenditure = request.form.get('caloric_expenditure',False)
        veg_or_noveg = request.form['veg_or_nonveg']
        disease = request.form['disease']
        region = request.form['region']
        allergics = request.form['allergics']
        foodtype = request.form['foodtype']

        chain_resto = LLMChain(llm=llm_resto, prompt=prompt_template_resto)

        # Define the input dictionary
        input_data = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'step_count': step_count,
            'heart_rate': heart_rate,
            'caloric_expenditure': caloric_expenditure,
            'veg_or_nonveg': veg_or_noveg,
            'disease': disease,
            'region': region,
            'allergics': allergics,
            'foodtype': foodtype
        }

        results = chain_resto.run(input_data)

        # Extracting the different recommendations using regular expressions
        restaurant_names = re.findall(r'Restaurants:(.*?)Breakfast:', results, re.DOTALL)
        breakfast_names = re.findall(r'Breakfast:(.*?)Dinner:', results, re.DOTALL)
        dinner_names = re.findall(r'Dinner:(.*?)Workout:', results, re.DOTALL)
        workout_names = re.findall(r'Workout:(.*?)$', results, re.DOTALL)

        # Cleaning up the extracted lists
        restaurant_names = [name.strip() for name in restaurant_names[0].strip().split('\n') if
                            name.strip()] if restaurant_names else []
        breakfast_names = [name.strip() for name in breakfast_names[0].strip().split('\n') if
                           name.strip()] if breakfast_names else []
        dinner_names = [name.strip() for name in dinner_names[0].strip().split('\n') if
                        name.strip()] if dinner_names else []
        workout_names = [name.strip() for name in workout_names[0].strip().split('\n') if
                         name.strip()] if workout_names else []

        return render_template('result.html', restaurant_names=restaurant_names, breakfast_names=breakfast_names,
                               dinner_names=dinner_names, workout_names=workout_names)

    return render_template('index.html')


if __name__=="__main__":
    app.run(debug = True)