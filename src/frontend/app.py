import os
from flask import Flask, render_template, request, redirect, session, url_for, flash
import networkx as nx
from werkzeug.utils import secure_filename
import matplotlib
matplotlib.use('Agg')
import sys
sys.path.append('./src/backend')
import graph
from dijkstra import dijkstra

app = Flask(__name__)
app.secret_key = "thisissecret"
ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home(): 
    return render_template('index.html', init_filename='ex_init.jpg', final_filename='ex_fin.jpg')

@app.route('/', methods = ['GET', 'POST'])
def draw_graph():
  if request.method == 'POST':
      f = request.files['file']
      if allowed_file(f.filename):
        filename = secure_filename(f.filename)
        p = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        p = os.path.join(p, "test/"+filename)
        f.save(p)

        g = nx.DiGraph()
        graph.read_file(p, g)
        graph.save_init_img(g)
        session['filename'] = filename
        return redirect(url_for('display_img'))
      else:
        flash('Please submit a text file')
        return redirect(url_for('home'))
  return redirect(url_for('home'))

@app.route('/display-img')
def display_img():
  return render_template('index.html', init_filename='graph_init.jpg', final_filename='empty_img.jpg')

@app.route('/search-dijkstra', methods = ['GET', 'POST'])
def search_path():
  # file is valid
  if request.method == 'POST':
      filename = session.get('filename', None)
      p = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
      p = os.path.join(p, "test/"+filename)

      start_node = request.form.get("snode")
      dest_node = request.form.get("dnode")

      g = nx.DiGraph()
      graph.read_file(p, g)

      if not (start_node in g and dest_node in g):
        # either start node or dest node does not exist
        flash('Node does not exist')
        return redirect(url_for('display_img'))
      else:
        dijkstra_res = dijkstra(start_node, dest_node, g)
        graph.save_fin_img(g, dijkstra_res[0], dijkstra_res[1])
        session['dist_res'] = "Distance: "
        session['time_res'] = "Search time: "
        session['it_count'] = "Iteration: "
        if dijkstra_res[3] is None:
          session['path_res'] = "Nodes are not connected"
          session['dist_res'] += "INFINITE"
        else:
          session['path_res'] = "Path: "
          for i in range (len(dijkstra_res[0])-1):
            session['path_res'] += dijkstra_res[0][i]
            session['path_res'] += "->"
          session['path_res'] += dijkstra_res[0][i+1]
          session['dist_res'] += str(dijkstra_res[3])
        session['time_res'] += str(dijkstra_res[2]*10e3) + ' milliseconds'
        session['it_count'] += str(dijkstra_res[4])
        
        return redirect(url_for('display_res'))
        
  return redirect(url_for('home'))

@app.route('/result-dijkstra')
def display_res():
  return render_template('index.html', init_filename='graph_init.jpg', final_filename='graph_fin.jpg', path=session.get('path_res', None), distance=session.get('dist_res', None), elapsed_time=session.get('time_res', None), iteration=session.get('it_count', None))

if __name__ == '__main__':
    g = nx.DiGraph()
    app.run(debug=True)