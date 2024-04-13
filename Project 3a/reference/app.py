import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'

# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

#Function to get a post from the database
def get_post(post_id):
    #get database connection
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)
    
    return post

# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    #use the get_db_connection() function to open a database connection
    conn = get_db_connection()

    #execute an SQL queryto select all entries from the posts table.
    #use the fetchall() method to fetch all the rows of the query result
    posts = conn.execute('SELECT * FROM posts').fetchall()

    #close the connection
    conn.close()
    
    return render_template('index.html', posts=posts)


# route to create a post
#pass the list of 'GET' and 'POST' to the methods parameter to allow GET and POST request
@app.route('/create/', methods=('GET', 'POST'))
def create():
    #determine request method for the page. If GET then load the page. If POST, process the form data
    if request.method == 'POST':
        #get the title and content
        title = request.form['title']
        content = request.form['content']

        #display and error if title or content not submitted
        #else make a dtatbase connection and insert content
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            #insert the data to the database
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

#create a route to edit a post
#load page with get or post method
#pass the post id as a url parameter
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    #id is sent as a url parameter get the post id
    post = get_post(id)

    #Determine if page loaded with GET or POST. If GET then load page with data from the query
    #If post, process the form data. Get the data nad validate it. Update the post and redirect to the home page
    if request.method == 'POST':
        #get the title and content
        title = request.form['title']
        content = request.form['content']

        # if no title or content the flash an error message
        if not title:
            flash('Title is required')
        elif not content:
            flash('Contentent is required')
        else:
            #otherwise: connect to the db, update the post and close the connection, and redirext to the home page
            conn = get_db_connection()

            #execute an update query
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()

            #redirect to the index page
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

#Route to delete a post
#Delete page will only be accessed with the POST method
#The post id is passed as a url parameter
@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    #get the post
    post = get_post(id)

    #connect to the database
    conn = get_db_connection()

    #execute the delete query
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))

    #commit and close the connection to the database
    conn.commit()
    conn.close()

    #flash a success message to the user
    flash('"{}" was successfully deleted!'.format(post['title']))

    #redirect to the index page
    return redirect(url_for('index'))


app.run(port=5010)