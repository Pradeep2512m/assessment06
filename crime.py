from werkzeug.utils import redirect
from datetime import date

folder = sqlite3.connect("CrimeReport.db",check_same_thread=False)
table1 = folder.execute("select * from sqlite_master where type = 'table' and name = 'crime'").fetchall()
table2 = folder.execute("select * from sqlite_master where type = 'table' and name = 'user'").fetchall()
connection = sqlite3.connect("CrimeReport.db",check_same_thread=False)
table1 = connection.execute("select * from sqlite_master where type = 'table' and name = 'crime'").fetchall()
table2 = connection.execute("select * from sqlite_master where type = 'table' and name = 'user'").fetchall()

if table1 !=[]:
    print("Crime table already exists")
else:
    folder.execute('''create table crime(
    connection.execute('''create table crime(
                            id integer primary key autoincrement,
                            description text,
                            remarks text,
@@ -21,7 +21,7 @@
if table2 !=[]:
    print("user table already exists")
else:
    folder.execute('''create table user(
    connection.execute('''create table user(
                            id integer primary key autoincrement,
                            name text,
                            address text,
@@ -56,7 +56,7 @@ def Admin_dashboard():

@crime.route('/view')
def View_report():
    cursor = folder.cursor()
    cursor = connection.cursor()
    cursor.execute("select * from crime")

    result = cursor.fetchall()
@@ -67,8 +67,8 @@ def View_report():
def Search_crime():
    if request.method == 'POST':
        getDate = str(request.form["date"])
        cursor = folder.cursor()
        cursor.execute("select * from crime where date='"+getDate+"' ")
        cursor = connection.cursor()
        cursor.execute("select * from crime where date='"+getDate+"'")
        result = cursor.fetchall()
        if result is None:
            print("There is no Crime on",getDate)
@@ -77,8 +77,6 @@ def Search_crime():
    else:
        return render_template("datesort.html",crime=[],status=False)



@crime.route('/register',methods=['GET','POST'])
def User_register():
    if request.method == 'POST':
@@ -89,9 +87,9 @@ def User_register():
        getPass = request.form["userpass"]
        print(getName,getAddress,getEmail,getPhone)
        try:
            folder.execute("insert into user(name,address,email,phone,password) \
            connection.execute("insert into user(name,address,email,phone,password) \
            values('"+getName+"','"+getAddress+"','"+getEmail+"',"+getPhone+",'"+getPass+"')")
            folder.commit()
            connection.commit()
            print("Inserted Successfully")
            return redirect('/complaint')
        except Exception as err:
@@ -103,8 +101,8 @@ def Login_user():
    if request.method == 'POST':
        getEmail = request.form["useremail"]
        getPass = request.form["userpass"]
        cursor = folder.cursor()
        query = "select * from user where email='"+getEmail+"' and password='"+getPass+"' "
        cursor = connection.cursor()
        query = ("select * from user where email='"+getEmail+"' and password='"+getPass+"'")
        result = cursor.execute(query).fetchall()
        if len(result)>0:
            for i in result:
@@ -115,7 +113,6 @@ def Login_user():
                if (getEmail == i[3] and getPass == i[5]):
                    print("password correct")
                    return redirect('/usersession')

                else:
                    return render_template("userlogin.html",status=True)
    else:
@@ -141,10 +138,10 @@ def Report_crime():
        print(getDescription)
        print(getRemark)
        getDate = str(date.today())
        cursor = folder.cursor()
        query = "insert into crime(description,remarks,date) values('"+getDescription+"','"+getRemark+"','"+getDate+"')"
        cursor = connection.cursor()
        query = ("insert into crime(description,remarks,date) values('"+getDescription+"','"+getRemark+"','"+getDate+"')")
        cursor.execute(query)
        folder.commit()
        connection.commit()
        print(query)
        print("Inserted Successfully")
        return redirect('/user')
@@ -156,8 +153,8 @@ def Update_user():
        if request.method == 'POST':
            getname = request.form["newname"]
            print(getname)
            cursor = folder.cursor()
            count = cursor.execute("select * from user where name='" + getname + "' ")
            cursor = connection.cursor()
            count = cursor.execute("select * from user where name='"+getname+"'")
            result = cursor.fetchall()
            print(len(result))
            return render_template("profileedit.html", searchname = result)
@@ -175,10 +172,10 @@ def User_edit():
        getPhone = request.form["newphone"]
        getPass = request.form["newpass"]
        try:
            query = "update user set address='" + getAddress + "',email='" + getEmail + "',phone=" + getPhone + ",password='" + getPass + "' where name='" + getName + "'"
            query = ("update user set address='"+getAddress+"',email='"+getEmail+"',phone="+getPhone+",password='"+getPass+"' where name='"+getName+"'")
            print(query)
            folder.execute(query)
            folder.commit()
            connection.execute(query)
            connection.commit()
            print("Edited Successfully")
            return redirect('/view')
        except Exception as error:
@@ -191,7 +188,5 @@ def Logout():
    session["name"] = None
    return redirect('/')



if __name__=="__main__":
    crime.run()