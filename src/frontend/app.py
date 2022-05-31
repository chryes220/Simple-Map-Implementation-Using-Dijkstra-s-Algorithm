import os
from flask import Flask, render_template, request
import networkx as nx
from werkzeug.utils import secure_filename
import sys
sys.path.append('./src/backend')
import graph
from dijkstra import dijkstra

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt'}

@app.route('/')
def main(): 
    return render_template('index.html', init_filename='graph_init.jpg', final_filename='graph_fin.jpg')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      if allowed_file(f.filename):
        filename = secure_filename(f.filename)
        p = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        p = os.path.join(p, "test/"+filename)
        f.save(p)
        start_node = request.form.get("snode")
        dest_node = request.form.get("dnode")
      
        g = nx.DiGraph()
        graph.read_file(p, g)
        graph.save_init_img(g)
        if not (g.has_node(start_node) and g.has_node(dest_node)):
          # either start node or dest node does not exist
          msg = 'Node does not exist'
          return render_template('index.html', init_filename='graph_init.jpg', final_filename='graph_fin.jpg', invalid_node_msg=msg)
        else:
          dijkstra_res = dijkstra(start_node, dest_node, g)
          graph.save_fin_img(g, dijkstra_res[0])

          path_res = "Path: "
          for i in range (len(dijkstra_res[0])-1):
            path_res += dijkstra_res[0][i]
            path_res += "->"
          path_res += dijkstra_res[0][i+1]
          dist_res = "Distance: "
          dist_res += str(dijkstra_res[3])
          time_res = "Elapsed time: "
          time_res += str(dijkstra_res[2]) + ' seconds'
          it_count = str(dijkstra_res[4])
          return render_template('index.html', init_filename='graph_init.jpg', final_filename='graph_fin.jpg', path=path_res, distance=dist_res, elapsed_time=time_res, iteration=it_count)
      else:
        msg = 'Must be in txt format!'
        return render_template('index.html', init_filename='graph_init.jpg', final_filename='graph_fin.jpg', wrong_file_msg=msg)
    

if __name__ == '__main__':
    g = nx.DiGraph()
    app.run()