from app import create_app

app = create_app('app.config')

if __name__ == '__main__':
    app.run(debug=True, port=9999, host='0.0.0.0')