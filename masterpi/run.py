from app import app

"""
This file run the flask application
"""

app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
# app.run(debug=True)
