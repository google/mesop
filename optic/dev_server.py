from optic.server import app

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)