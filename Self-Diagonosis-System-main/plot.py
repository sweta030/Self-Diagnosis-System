import io
from flask import Flask,Response, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
app=Flask(__name__)

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    xs = [datetime(2021, 11, 18, 12), datetime(2021, 11, 18, 14), datetime(2021, 11, 18, 16),datetime(2021, 11, 18, 17),datetime(2021, 11, 18, 20)]
    ys = [1.0, 3.0, 2.0,4.5,1.7]
    ys2=[2.0,1.5,5.0,7.5,8.0]
    axis.plot(xs,ys,label="line 1")
    axis.plot(xs,ys2,label="line 2")
    axis.legend()
    axis.set_xticks(xs)
    axis.set_xticklabels(xs, rotation=15, ha='right')
    return fig

if __name__ == "__main__":
    app.run(debug=True)