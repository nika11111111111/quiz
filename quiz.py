from flask import Flask, redirect, url_for, session, request, render_template
from db_scripts import get_question_after, get_from_quiz, show, check_answer
import random
import os


show('quiz_content')

def index():
    if request.method == 'GET':
        session['index_quiz'] = -1
        session['index_question'] = 1
        session['total'] = 0 
        session['answers'] =0
        return quiz_form()
    if request.method == 'POST':
        session['index_quiz']= request.form.get('quiz')
        session['index_question'] = 1
        return redirect(url_for('test'))
def quiz_form():        
    quizes = get_from_quiz()
    return render_template('start.html',quizes = quizes)
def test():
    if not ('index_quiz' in session) or int(session['index_quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        next_question = get_question_after(session['index_question'], session['index_quiz'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)
def question_form(question):
    answers_list = [question[2],question[3],question[4],question[5]]    
    random.shuffle(answers_list)
    return render_template('test.html',question = question[1], quest_id = question[0], answers_list = answers_list)
def save_answers():
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    session['index_question'] = quest_id
    session['total'] += 1
    if check_answer(quest_id, answer):
        session['answers'] +=1

def result():
    return render_template('result.html',text ="Конец викторины" , question = session['total'], answer=session['answers']) 
# Создаём объект веб-приложения:
folder = os.getcwd()
app = Flask(__name__,template_folder= folder, static_folder = folder) 
app.config['SECRET_KEY'] = 'GoodKey'
                        # параметр - имя модуля для веб-приложения
                        # значение __name__ содержит корректное имя модуля для текущего файла 
                        # в нём будет значение "__main__", если модуль запускается непосредственно
                        # и другое имя, если модуль подключается
app.add_url_rule('/', 'index', index)
app.add_url_rule('/', 'index', index, methods=['POST','GET'])
app.add_url_rule('/test', 'test', test, methods=['POST','GET'])
app.add_url_rule('/result', 'result',result, methods=['POST','GET'])
   # создаёт правило для URL: 
                                        # при получении GET-запроса на адрес '/' на этом сайте
                                        # будет запускаться функция index (указана третьим параметром)
                                        # и её значение будет ответом на запрос.
                                        # Второй параметр - endpoint, "конечная точка", -
                                        # это строка, которая содержит имя данного правила. 
                                        # Обычно endpoint рекомендуют делать идентичным имени функции, 
                                        # но в сложных приложениях может быть несколько функций с одним именем в разных модулях, 
                                        # и для различения их в пределах всего сайта можно указывать разные endpoint.

if __name__ == "__main__":
    # Запускаем веб-сервер:
    app.run() 