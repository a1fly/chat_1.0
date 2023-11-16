from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import openpyxl
import time

user_number = list(range(0, 100))
point = 0
user_list = []

user_idcard = 0


# 定义一个用户类，每个用户连接时实例化

class user_for_chat():
    def __init__(self, idcard, account, password):
        self.idcard = idcard
        self.account = account
        self.password = password
    def show_user_account(self):
        return self.account


#  创立通信连接，渲染前端界面，前端界面存放在first.html中

# =====================================================================================================
# =====================================================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
history_messages = []

# ==========================================================
# 已经注册的用户
already_reg_user = {'zcy':'123'}

test=''
# ==========================================================

@app.route('/', methods=['GET', 'POST'])
def land():
    global test
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        action = request.form['action']
        # 检查账号和密码是否匹配
        # =========================================================================================================
        # =========================================================================================================
        if action == '登录':
            value1 = already_reg_user.get(account, -999)
            if (account in already_reg_user) and (already_reg_user[account] == password) and (value1 != -999):
                test=account
                return redirect(url_for('index',user_account=account))
            else:
                return render_template('land.html', warning='请输入正确的账号密码')
        # =========================================================================================================
        # =========================================================================================================
        if action == '注册':
            return redirect(url_for('reg'))
    return render_template('land.html')


# 注册界面渲染
# =========================================================================================================
# =========================================================================================================


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    global user_for_chat, already_reg_user
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        re_password = request.form['confirm_password']

        if account in already_reg_user:
            return render_template('reg.html', warnings='用户已存在')

        if account == '' or password == '':
            return render_template('reg.html', warnings='不能为空! ! ! ')

        if password == re_password and account != '':
            # 存入账户和密码
            already_reg_user[account] = str(password)

            return redirect(url_for('land'))
        else:
            return render_template('reg.html', warnings='密码两次不一致，请重新输入')
    return render_template('reg.html')


# =========================================================================================================
# =========================================================================================================
@app.route('/chat')
def index():
    user_account=request.args.get('user_account')
    return render_template('first.html',user_account=user_account)


@socketio.on('message')
def handle_message(message):
    history_messages.append(message)

    now_time = str(time.time())

    emit('update_messages', message, broadcast=True)



@socketio.on('connect')
def handle_connect():

        print(test)
        notice = f'欢迎用户{test}连接'
        emit('update_messages', notice, broadcast=True)


# =====================================================================================================
# =====================================================================================================

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
