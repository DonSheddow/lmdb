from lmdb import app

if app.debug:
    app.run(host='127.0.0.1')
else:
    app.run(host='0.0.0.0')
