# Welcome to my website!

This is my personal website built using Flask.

### How to add a new post?
export FLASK_APP=microblog.py
flask shell

p = Post(body='What are the effects on runtime, clustering performance, and numerical stability, if a randomized singular value decomposition is used to approximate the transformation matrix in a subspace k-means algorithm?', link='svd.html', title='The Influence of a Randomized SVD on the Subspace K-Means Algorithm')

db.session.add(p)
db.session.commit()

