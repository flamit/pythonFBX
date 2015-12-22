from flask import Flask, render_template, url_for, send_from_directory
from FBX import *
import json


BOOSTRAP_LAYOUT_COLUMNS = 12

class TableView(object):
	def __init__(self, data, width=4):
		assert(isinstance(data, list))
		assert((BOOSTRAP_LAYOUT_COLUMNS % width) == 0, "[TableView] BOOSTRAP_LAYOUT_COLUMNS must by divisible by width: %s" % width)
		self.data = data
		self.rows = []

		self.width = width
		height = len(self.data) / self.width
		self.height = height+1 if len(data) % width else height
		self.cellsize = BOOSTRAP_LAYOUT_COLUMNS / width

		self.load()

	def load(self):
		for row in xrange(self.height):
			slice_from = row * self.width
			slice_to = slice_from + self.width
			self.rows.append(self.data[slice_from:slice_to])


class Actions(object):
    ALL = LEFT, RIGHT, UP, DOWN, FORWARDS, BACKWARDS = 'left', 'right', 'up', 'down', 'forwrd', 'backwrd'


app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
	fbx_views = []
	for fbx_path in fbx_files():
		name = fbx_name(fbx_path)
		viewname = fbx_view_name(name)
		is_view_exists = os.path.exists(os.path.join(IMG_FOLDER_PATH, viewname))

		fbxview = {
			'name': name,
			'file': fbx_path,
			'is_view_exists': is_view_exists,
			'view_url': url_for('view_file', filename=viewname),
            'details_url': url_for('details', name=name),
		}
		fbx_views.append(fbxview)
        print('[home]', json.dumps(fbxview, indent=4))

	table = TableView(fbx_views)
	return render_template('index.html', table=table, fbx_views=fbx_views, FBX_FOLDER_PATH=FBX_FOLDER_PATH, IMG_FOLDER_PATH=IMG_FOLDER_PATH)

@app.route('/details/<string:name>')
def details(name):
    viewname = fbx_view_name(name)
    if not os.path.exists(os.path.join(IMG_FOLDER_PATH, viewname)):
        control(name, None) # process file without any action

    fbxview = {
		'name': name,
		'view_url': url_for('view_file', filename=viewname)
	}
    control_urls = {}
    for action in Actions.ALL:
        control_urls[action] = url_for('control', action=action, name=name)

    return render_template('details.html', fbxview=fbxview, control_urls=control_urls, Actions=Actions)

@app.route('/control/<string:name>/<string:action>')

