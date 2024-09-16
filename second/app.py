from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from midline_to_obj import process_single_file
from fb_avg_3d_instance_to_midline_volume import process_directory

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/thin')
def socket():
    socketio.start_background_task(target=thin_mask)
    return 'task started!', 202

def thin_mask():
    test = False
    replace = False
    time = False
    filter_labels = False
    front = False
    back = False

    # If neither front nor back is specified, use both and average
    if not front and not back:
        front = True
        back = True

    input_directory = '../data'
    label_values = None  # List of label values to process, pass None to process all labels
    process_directory(input_directory, pad_amount=0, label_values=label_values, test_mode=test, 
                      replace=replace, show_time=time, filter_labels=filter_labels, front=front, back=back, mask_out=True)

    socketio.emit('task_done', {'message': 'task finished!'})

@socketio.on('task_done')
def handle_task_done(data):
    print('hi')

@app.route('/obj')
def mask_to_obj():
    vis = False
    replace = False
    should_print_timing = False
    should_fix_normals = True
    reconnection_mult = 50
    
    path = '../data/01744_02256_02768/01744_02256_02768_fb_avg_mask_thinned.nrrd'
    process_single_file((path, 1.5, 500, vis, False, reconnection_mult, should_print_timing, should_fix_normals, replace))

    return 'Hello, World!'

@socketio.on('connect')
def handle_connect():
    print('socket connected!')

if __name__ == '__main__':
    # http://127.0.0.1:1235
    socketio.run(app, host="0.0.0.0", port=1235, debug=True)

