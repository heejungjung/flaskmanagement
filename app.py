# app.py
from flask import Flask, render_template, redirect, request
import pymysql
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student')
def student():
    db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                         passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
    cursor = db.cursor()

    # 페이지 값 (디폴트값 = 1)
    page = request.args.get("page", 1, type=int)
    # 한 페이지당 개수
    per_page = 5
    # 전체 페이지 구하기
    cursor.execute("SELECT COUNT(*) from student")
    tot_count = cursor.fetchone()[0]
    total_page = int(tot_count / per_page) + 1

    query = "SELECT * FROM student LIMIT %s OFFSET %s;"
    cursor.execute(query, (per_page, (page-1) * per_page))
    data_list = cursor.fetchall()
    print(data_list)

    # 페이지 블럭을 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_start = (block_size * block_num) + 1
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)

    db.close()
    return render_template("student.html",data_list=data_list,per_page=per_page,page=page,
                           block_start=block_start,block_end=block_end,total_page=total_page,tot_count=tot_count)


@app.route('/stdinsertform')
def stdinsertform():
    return render_template('stdinsertform.html')

@app.route('/stdinsert', methods=['POST', 'GET'])
def stdinsert():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        ## 넘겨받은 stdname
        stdname = request.form.get('stdname')
        ## 넘겨받은 stdgender
        stdgender = request.form.get('stdgender')
        ## 넘겨받은 stdphone
        stdphone = request.form.get('stdphone')
        ## 넘겨받은 stdbirth
        stdbirth = request.form.get('stdbirth')
        print(stdname)
        print(stdgender)
        print(stdphone)
        print(stdbirth)

        sql = "INSERT INTO student (std_name,std_gender,std_phone,std_birth,std_register) VALUES (%s,%s,%s,%s,%s)"

        db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                             passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql,(stdname, stdgender, stdphone, stdbirth, time.strftime('%y-%m-%d %H:%M:%S')))
        db.commit()
        db.close()

        return redirect('/student')

@app.route("/stddelete/<id>")
def stddelete(id):
    sql = "DELETE FROM student WHERE std_id = "+id
    db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                         passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect('/student')

@app.route("/stdupdate/<id>", methods=["GET", "POST"])
def stdupdate(id):
    sql = "SELECT * FROM student WHERE std_id = "+id
    db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                         passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()

    if request.method == "GET":
        db.close()
        return render_template("stdupdateform.html", data_list=data_list)
    elif request.method == 'POST':
        ## 넘겨받은 stdname
        stdname = request.form.get('stdname')
        ## 넘겨받은 stdgender
        stdgender = request.form.get('stdgender')
        ## 넘겨받은 stdphone
        stdphone = request.form.get('stdphone')
        ## 넘겨받은 stdbirth
        stdbirth = request.form.get('stdbirth')

        sql = "UPDATE student SET std_name=%s,std_gender=%s,std_phone=%s,std_birth=%s WHERE std_id = "+id
        cursor.execute(sql,(stdname, stdgender, stdphone, stdbirth))
        db.commit()
        db.close()

        return redirect('/student')

@app.route('/lecture')
def lecture():
    db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                         passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
    cursor = db.cursor()

    # 페이지 값 (디폴트값 = 1)
    page = request.args.get("page", 1, type=int)
    # 한 페이지당 개수
    per_page = 5
    # 전체 페이지 구하기
    cursor.execute("SELECT COUNT(*) from lecture")
    tot_count = cursor.fetchone()[0]
    total_page = int(tot_count / per_page) + 1

    query = "SELECT * FROM lecture l JOIN teacher t ON l.lecture_teacher = t.teacher_id ORDER BY l.lecture_id LIMIT %s OFFSET %s;"
    cursor.execute(query, (per_page, (page-1) * per_page))
    data_list = cursor.fetchall()
    print(data_list)

    # 페이지 블럭을 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_start = (block_size * block_num) + 1
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)

    db.close()
    return render_template("lecture.html",data_list=data_list,per_page=per_page,page=page,
                           block_start=block_start,block_end=block_end,total_page=total_page,tot_count=tot_count)

@app.route('/lectureinsertform')
def lectureinsertform():
    db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                         passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM teacher")
    data_list = cursor.fetchall()
    db.close()
    return render_template('lectureinsertform.html',data_list=data_list)

@app.route('/lectureinsert', methods=['POST', 'GET'])
def lectureinsert():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                             passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
        cursor = db.cursor()

        ## 넘겨받은 lecturename
        lecturename = request.form.get('lecturename')
        ## 넘겨받은 lectureteacher
        cursor.execute("SELECT teacher_id from teacher WHERE teacher_name='"+request.form.get('lectureteacher')+"';")
        lectureteacher = cursor.fetchone()[0]
        print(lecturename)
        print(lectureteacher)

        sql = "INSERT INTO lecture (lecture_name,lecture_teacher) VALUES (%s,%s)"

        cursor.execute(sql,(lecturename, lectureteacher))
        db.commit()
        db.close()

        return redirect('/lecture')

@app.route("/lecturedelete/<id>")
def lecturedelete(id):
    sql = "DELETE FROM lecture WHERE lecture_id = "+id
    db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                         passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect('/lecture')

@app.route("/lectureupdate/<id>", methods=["GET", "POST"])
def lectureupdate(id):
    sql = "SELECT * FROM lecture WHERE lecture_id = "+id
    db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                         passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()
    cursor.execute("SELECT * FROM teacher")
    teacher_list = cursor.fetchall()

    if request.method == "GET":
        db.close()
        return render_template("lectureupdateform.html", data_list=data_list, teacher_list=teacher_list)
    elif request.method == 'POST':
        ## 넘겨받은 lecturename
        lecturename = request.form.get('lecturename')
        ## 넘겨받은 lectureteacher
        cursor.execute("SELECT teacher_id from teacher WHERE teacher_name='"+request.form.get('lectureteacher')+"';")
        lectureteacher = cursor.fetchone()[0]
        print(lecturename)
        print(lectureteacher)

        sql = "UPDATE lecture SET lecture_name=%s,lecture_teacher=%s WHERE lecture_id = "+id
        cursor.execute(sql,(lecturename, lectureteacher))
        db.commit()
        db.close()

        return redirect('/lecture')

@app.route('/teacher')
def teacher():
    db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                         passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
    cursor = db.cursor()

    # 페이지 값 (디폴트값 = 1)
    page = request.args.get("page", 1, type=int)
    # 한 페이지당 개수
    per_page = 5
    # 전체 페이지 구하기
    cursor.execute("SELECT COUNT(*) from teacher")
    tot_count = cursor.fetchone()[0]
    total_page = int(tot_count / per_page) + 1

    query = "SELECT * FROM teacher LIMIT %s OFFSET %s;"
    cursor.execute(query, (per_page, (page-1) * per_page))
    data_list = cursor.fetchall()
    print(data_list)

    # 페이지 블럭을 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_start = (block_size * block_num) + 1
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)

    db.close()
    return render_template("teacher.html",data_list=data_list,per_page=per_page,page=page,
                           block_start=block_start,block_end=block_end,total_page=total_page,tot_count=tot_count)

@app.route('/teacherinsertform')
def teacherinsertform():
    return render_template('teacherinsertform.html')

@app.route('/teacherinsert', methods=['POST', 'GET'])
def teacherinsert():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        ## 넘겨받은 teachername
        teachername = request.form.get('teachername')
        print(teachername)

        sql = "INSERT INTO teacher (teacher_name) VALUES (%s)"

        db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                             passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
        cursor = db.cursor()
        cursor.execute(sql,(teachername))
        db.commit()
        db.close()

        return redirect('/teacher')

@app.route("/teacherdelete/<id>")
def teacherdelete(id):
    sql = "DELETE FROM teacher WHERE teacher_id = "+id
    db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                         passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect('/teacher')

@app.route("/teacherupdate/<id>", methods=["GET", "POST"])
def teacherupdate(id):
    sql = "SELECT * FROM teacher WHERE teacher_id = "+id
    db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="bbdaa9fadb155b",
                         passwd="a8612018", db="heroku_77fc15d70b36c03", charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()

    if request.method == "GET":
        db.close()
        return render_template("teacherupdateform.html", data_list=data_list)
    elif request.method == 'POST':
        ## 넘겨받은 teachername
        teachername = request.form.get('teachername')
        print(teachername)

        sql = "UPDATE teacher SET teacher_name=%s WHERE teacher_id = "+id
        cursor.execute(sql,(teachername))
        db.commit()
        db.close()

        return redirect('/teacher')

if __name__ == '__main__':
    app.run(debug=True)