from flask import Flask, request, render_template, url_for
app = Flask(__name__)


@app.route('/dktt')
def hello_world():
    bg = url_for('static', filename='images/bg.jpg')
    page_title= 'Hệ thống điều khiển Robot'
    logo = url_for('static', filename='images/logo.png')
    message = 'Chế độ điều khiển bằng tay'
    return render_template('endpoint.html', logo=logo, message=message, page_title=page_title, bg=bg
                           )

@app.route('/')
def run():
    return 'hello world'

@app.route('/endpoint')
def endpoint():
    bg = url_for('static', filename='images/bg.jpg')
    page_title = 'Hệ thống điều khiển Robot'
    logo = url_for('static', filename='images/logo.png')
    msg_robot_status = request.args.get('status') if request.args.get('status') else 2
    if msg_robot_status == 2:
        message = 'Chế độ điều khiển bằng tay'
    elif msg_robot_status == 3:
        message = 'Chế độ tự động'
    else:
        message = 'Chế độ tự động bấm vạch từ'

    return render_template('base.html', logo=logo, message=message, page_title=page_title, bg=bg)


if __name__ == '__main__':
    app.run(debug=True, port=5000)