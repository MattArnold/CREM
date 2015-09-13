from app import app

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/admin')
def adminPage():
	return app.send_static_file('admin.html')
