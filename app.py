# app.py
import os
from flask import Flask, render_template, redirect, request
import MySQLdb
import time

app = Flask(__name__)

# MySQL 연결 설정
conn = MySQLdb.connect(host='AmyJeong.mysql.pythonanywhere-services.com', user='AmyJeong', passwd='flaskmanagement', db='AmyJeong$Flask_management')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rqt')
def rqt():
    cursor = conn.cursor()

    # 페이지 값 (디폴트값 = 1)
    page = request.args.get("page", 1, type=int)
    # 한 페이지당 개수
    per_page = 5
    # 전체 페이지 구하기
    cursor.execute("SELECT COUNT(*) from request")
    tot_count = cursor.fetchone()[0]
    total_page = int(tot_count / per_page) + 1

    query = "SELECT * FROM request LIMIT %s OFFSET %s;"
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
    cursor.close()
    return render_template("rqt.html",data_list=data_list,per_page=per_page,page=page,
                           block_start=block_start,block_end=block_end,total_page=total_page,tot_count=tot_count)


@app.route('/rqtinsertform')
def rqtinsertform():
    return render_template('rqtinsertform.html')

@app.route('/rqtinsert', methods=['POST', 'GET'])
def rqtinsert():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        ## 넘겨받은 request_delivery_date
        request_delivery_date = request.form.get('request_delivery_date')
        ## 넘겨받은 request_title
        request_title = request.form.get('request_title')
        ## 넘겨받은 request_purpose
        request_purpose = request.form.get('request_purpose')
        ## 넘겨받은 request_team
        request_team = request.form.get('request_team')
        ## 넘겨받은 request_member
        request_member = request.form.get('request_member')

        sql = "INSERT INTO REQUEST (BASE_DATE, REQUEST_DELIVERY_DATE, REQUEST_TITLE, REQUEST_PURPOSE, REQUEST_TEAM, REQUEST_MEMBER, REQUEST_DATE) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        cursor = conn.cursor()
        cursor.execute(sql,(time.strftime('%Y-%m-%d'), request_delivery_date, request_title, request_purpose, request_team, request_member, time.strftime('%Y-%m-%d %H:%M:%S')))
        cursor.commit()
        cursor.close()

        return redirect('/rqt')

@app.route("/rqtdelete/<id>")
def rqtdelete(id):
    sql = "DELETE FROM REQUEST WHERE request_id = "+id
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.commit()
    cursor.close()
    return redirect('/rqt')

@app.route("/rqtupdate/<id>", methods=["GET", "POST"])
def rqtupdate(id):
    sql = "SELECT * FROM request WHERE request_id = "+id
    cursor = conn.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()

    if request.method == "GET":
        cursor.close()
        return render_template("rqtupdateform.html", data_list=data_list)
    elif request.method == 'POST':
        ## 넘겨받은 request_delivery_date
        request_delivery_date = request.form.get('request_delivery_date')
        ## 넘겨받은 request_title
        request_title = request.form.get('request_title')
        ## 넘겨받은 request_purpose
        request_purpose = request.form.get('request_purpose')
        ## 넘겨받은 request_team
        request_team = request.form.get('request_team')
        ## 넘겨받은 request_member
        request_member = request.form.get('request_member')
        ## 넘겨받은 request_executor
        request_executor = request.form.get('request_executor')
        ## 넘겨받은 file_link
        file_link = request.form.get('file_link')

        sql = "UPDATE request SET request_delivery_date=%s,request_title=%s,request_purpose=%s,request_team=%s,request_member=%s,request_executor=%s,file_link=%s WHERE request_id = "+id
        cursor.execute(sql,(request_delivery_date, request_title, request_purpose, request_team, request_member, request_executor, file_link))
        cursor.commit()
        cursor.close()

        return redirect('/rqt')

@app.route('/lecture')
def lecture():
    cursor = conn.cursor()

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

    cursor.close()
    return render_template("lecture.html",data_list=data_list,per_page=per_page,page=page,
                           block_start=block_start,block_end=block_end,total_page=total_page,tot_count=tot_count)

@app.route('/lectureinsertform')
def lectureinsertform():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teacher")
    data_list = cursor.fetchall()
    cursor.close()
    return render_template('lectureinsertform.html',data_list=data_list)

@app.route('/lectureinsert', methods=['POST', 'GET'])
def lectureinsert():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        cursor = conn.cursor()

        ## 넘겨받은 lecturename
        lecturename = request.form.get('lecturename')
        ## 넘겨받은 lectureteacher
        cursor.execute("SELECT teacher_id from teacher WHERE teacher_name='"+request.form.get('lectureteacher')+"';")
        lectureteacher = cursor.fetchone()[0]
        print(lecturename)
        print(lectureteacher)

        sql = "INSERT INTO lecture (lecture_name,lecture_teacher) VALUES (%s,%s)"

        cursor.execute(sql,(lecturename, lectureteacher))
        cursor.commit()
        cursor.close()

        return redirect('/lecture')

@app.route("/lecturedelete/<id>")
def lecturedelete(id):
    sql = "DELETE FROM lecture WHERE lecture_id = "+id
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.commit()
    cursor.close()
    return redirect('/lecture')

@app.route("/lectureupdate/<id>", methods=["GET", "POST"])
def lectureupdate(id):
    sql = "SELECT * FROM lecture WHERE lecture_id = "+id
    cursor = conn.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()
    cursor.execute("SELECT * FROM teacher")
    teacher_list = cursor.fetchall()

    if request.method == "GET":
        cursor.close()
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
        cursor.commit()
        cursor.close()

        return redirect('/lecture')

@app.route('/teacher')
def teacher():
    cursor = conn.cursor()

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

    cursor.close()
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

        cursor = conn.cursor()
        cursor.execute(sql,(teachername))
        cursor.commit()
        cursor.close()

        return redirect('/teacher')

@app.route("/teacherdelete/<id>")
def teacherdelete(id):
    sql = "DELETE FROM teacher WHERE teacher_id = "+id
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.commit()
    cursor.close()
    return redirect('/teacher')

@app.route("/teacherupdate/<id>", methods=["GET", "POST"])
def teacherupdate(id):
    sql = "SELECT * FROM teacher WHERE teacher_id = "+id
    cursor = conn.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()

    if request.method == "GET":
        cursor.close()
        return render_template("teacherupdateform.html", data_list=data_list)
    elif request.method == 'POST':
        ## 넘겨받은 teachername
        teachername = request.form.get('teachername')
        print(teachername)

        sql = "UPDATE teacher SET teacher_name=%s WHERE teacher_id = "+id
        cursor.execute(sql,(teachername))
        cursor.commit()
        cursor.close()

        return redirect('/teacher')

if __name__ == '__main__':
    app.run(debug=True)
