import sqlite3
db_name = 'quiz.sqlite'
conn = None
curor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()
def check_answer(quest_id,answer):
    query='''SELECT question.answer 
    FROM quiz_content,question 
    WHERE quiz_content.id = ? 
    AND quiz_content.question_id = question.id'''
    open()
    cursor.execute(query, [str(quest_id)])
    result = cursor.fetchone()
    close()
    print(answer)
    print(result)
    if answer == result[0]:
        return True
    return False
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    do('''CREATE TABLE IF NOT EXISTS quizes (id INTEGER PRIMARY KEY,name VARCHAR)''')
    do('''CREATE TABLE IF NOT EXISTS question(
    id INTEGER PRIMARY KEY,
    question VARCHAR, 
    answer VARCHAR, 
    wrong1 VARCHAR,
    wrong2 VARCHAR,
    wrong3 VARCHAR)''')
    do('''CREATE TABLE IF NOT EXISTS quiz_content(
    id INTEGER PRIMARY KEY, 
    quiz_id INTEGER, 
    question_id INTEGER, 
    FOREIGN KEY(quiz_id) REFERENCES quizes (id),FOREIGN KEY(question_id) REFERENCES question (id))''')
    close()

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quizes')
    show('quiz_content')

def add_quiz():
    open()
    quizes = [
        ('Своя игра', ),
        ('Кто хочет стать миллионером?', ),
        ('Самый умный', )]
    cursor.executemany('''INSERT INTO quizes(name)VALUES (?)''',quizes)
    conn.commit()
    close()

def question():
    open()
    list_q = [('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        ('Каким станет зеленый утес, если упадет в Красное море?', 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
        ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
        ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако')]
    cursor.executemany('''INSERT INTO question(question,answer,wrong1,wrong2,wrong3) VALUES (?,?,?,?,?)''',list_q)
    conn.commit()
    close()

def quiz_content():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    answer = input('Добавить связь да/нет')
    while answer != 'нет':
        quiz_id = int(input('Введите айди викторины'))
        question_id= int(input('Введите айди вопроса'))
        cursor.execute('''INSERT INTO quiz_content(quiz_id,question_id) VALUES (?,?)''',[quiz_id, question_id])
        conn.commit()
        answer = input('Добавить связь да/нет')
    close()

def get_question_after(question_id = 0, quiz_id = 1):
    open()
    cursor.execute('''SELECT quiz_content.id,question.question , question.answer, question.wrong1, question.wrong2, question.wrong3 FROM quiz_content , question WHERE quiz_content.question_id = question.id AND quiz_content.id > ? AND quiz_content.quiz_id = ? Order By quiz_content.id''', [question_id , quiz_id])
    result = cursor.fetchone()
    close()
    return result
def get_from_quiz():
    open()
    cursor.execute('''SELECT * FROM quizes ORDER BY id''')
    quiz = cursor.fetchall()
    close()
    return quiz
    
def main():
    clear_db()
    create()
    question()
    add_quiz()
    show_tables()
    quiz_content()
    show_tables()

if __name__ == "__main__":
    main()



