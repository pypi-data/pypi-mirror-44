import numpy as np
import plotly.graph_objs as go
from plotly.tools import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from deepreplay.plot import build_2d_grid
from ipywidgets import VBox, interactive, IntSlider, Checkbox, FloatLogSlider, Button, FloatSlider, HBox, Dropdown
import warnings
warnings.filterwarnings("ignore")

class plotGradientDescent(object):
    def __init__(self, x1, x2, y):
        self.orig_x1 = x1
        self.orig_x2 = x2
        self.orig_y = y
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.stdsc = StandardScaler(with_mean=True, with_std=True)
        self.linr, self.losses, self.scaled_linr, self.scaled_losses = self.fit()

    def fit(self):
        linr = LinearRegression(fit_intercept=False)
        linr.fit(np.concatenate([np.ones_like(self.x1), self.x1, self.x2], axis=1), self.y)

        scaled_linr = LinearRegression(fit_intercept=False)
        self.scaled_x1, self.scaled_x2 = self.scale()
        scaled_linr.fit(np.concatenate([np.ones_like(self.scaled_x1), self.scaled_x1, self.scaled_x2], axis=1), self.y)

        self.grid = build_2d_grid(np.array([-3, 3]) + linr.coef_[1],
                                  np.array([3, -3]) + linr.coef_[2],
                                  n_lines=200, n_points=200)

        self.scaled_grid = build_2d_grid(np.array([-3, 3]) + scaled_linr.coef_[1],
                                  np.array([3, -3]) + scaled_linr.coef_[2],
                                  n_lines=200, n_points=200)

        losses = self.loss_surface(self.grid, self.x1, self.x2, self.y)
        scaled_losses = self.loss_surface(self.scaled_grid, self.scaled_x1, self.scaled_x2, self.y)

        return linr, losses, scaled_linr, scaled_losses

    def scale(self):
        scaled = self.stdsc.fit_transform(np.concatenate([self.orig_x1, self.orig_x2], axis=1))
        x1 = scaled[:, 0, np.newaxis]
        x2 = scaled[:, 1, np.newaxis]
        return x1, x2

    def sort(self):
        xy = np.array([np.array([x1, x2, y]) for x1, x2, y in sorted(zip(self.x1.ravel(),
                                                                         self.x2.ravel(),
                                                                         self.y.ravel()))])
        self.x1 = xy[:, 0]
        self.x2 = xy[:, 1]
        self.y = xy[:, 2].ravel()

        x = np.array([np.array([x1, x2]) for x1, x2 in sorted(zip(self.scaled_x1.ravel(),
                                                                  self.scaled_x2.ravel()))])
        self.scaled_x1 = x[:, 0]
        self.scaled_x2 = x[:, 1]

    def reset_X(self):
        self.x1 = self.orig_x1
        self.x2 = self.orig_x2
        self.y = self.orig_y
        self.scaled_x1, self.scaled_x2 = self.scale()

    def loss_surface(self, grid, x1, x2, y):
        predictions = np.dot(grid, np.concatenate([x1, x2], axis=1).T)
        losses = np.apply_along_axis(func1d=lambda v: mean_squared_error(y, v), axis=2, arr=predictions)
        return losses

    def step(self, x1, x2, y, m1, m2, b, lr=0.0001):
        N = len(y)
        y_current = (m1 * x1 + m2 * x2) + b
        error = np.array(y - y_current)
        cost = (error ** 2).mean()
        m1_gradient = -(2/N) * sum(x1 * error)
        m2_gradient = -(2/N) * sum(x2 * error)
        b_gradient = -(2/N) * sum(error)
        m1 = m1 - (lr * m1_gradient)
        m2 = m2 - (lr * m2_gradient)
        b = b - (lr * b_gradient)
        return m1, m2, b, cost

    def train(self, m1=0, m2=0, b=0, batch_size=None, epochs=1000, lr=0.0001, scaled=True):
        if scaled:
            grid = self.scaled_grid
            losses = self.scaled_losses
            x1 = self.scaled_x1.ravel()
            x2 = self.scaled_x2.ravel()
            m1min = self.scaled_linr.coef_[1]
            m2min = self.scaled_linr.coef_[2]
        else:
            grid = self.grid
            losses = self.losses
            x1 = self.x1.ravel()
            x2 = self.x2.ravel()
            m1min = self.linr.coef_[1]
            m2min = self.linr.coef_[2]
        y = self.y.ravel()

        N = len(y)
        if (batch_size is None) or (batch_size > N):
            batch_size = N
        n_batches = int(N // batch_size)

        m1_history = [m1]
        m2_history = [m2]
        b_history = [b]
        y_current = (m1 * x1 + m2 * x2) + b
        error = np.array(y - y_current)
        cost = (error ** 2).mean()
        cost_history = [cost]
        for i in range(epochs):
            for j in range(n_batches):
                clause = slice(j * batch_size, (j + 1) * batch_size)
                m1, m2, b, cost = self.step(x1[clause],
                                            x2[clause],
                                            y[clause],
                                            m1, m2, b, lr)
                m1_history.append(m1)
                m2_history.append(m2)
                b_history.append(b)
                cost_history.append(cost)

        self.contour = self.plot_contour(grid, losses.T)
        self.path = self.plot_path(m1_history, m2_history)
        self.minimum = self.plot_minimum(m1min, m2min)

    @property
    def traces(self):
        return dict(contour=self.contour, path=self.path, minimum=self.minimum)

    def plot_contour(self, grid, losses):
        contour = go.Contour(x=grid[:, 0, 0],
                             y=grid[0, :, 1],
                             z=losses)
        return contour

    def plot_path(self, m1, m2):
        path = go.Scatter(x=m1, y=m2, mode='lines')
        return path

    def plot_minimum(self, m1, m2):
        minimum = go.Scatter(x=[m1], y=[m2], mode='markers', marker={'symbol': 'star'})
        return minimum

def data():
    np.random.seed(42)
    orig_x1 = np.linspace(-1, 3, 1000) + np.random.randn(1000)
    orig_x2 = np.linspace(20, 50, 1000) + np.random.randn(1000)
    orig_y = 1 + 2 * orig_x1 + 0.05 * orig_x2 + 2 * np.random.randn(1000)

    shuffled = list(range(1000))
    np.random.shuffle(shuffled)
    x1 = orig_x1[shuffled[:50]].reshape(-1, 1)
    x2 = orig_x2[shuffled[:50]].reshape(-1, 1)
    y = orig_y[shuffled[:50]]
    return x1, x2, y

def build_figure(gd_obj):
    fig = make_subplots(1, 1, print_grid=False)
    fig.append_trace(go.Contour(x=gd_obj.scaled_grid[:, 0, 0],
                                 y=gd_obj.scaled_grid[0, :, 1],
                                 z=gd_obj.scaled_losses), 1, 1)
    fig.append_trace(go.Scatter(x=[], y=[], mode='lines'), 1, 1)
    fig.append_trace(go.Scatter(x=[gd_obj.scaled_linr.coef_[1]],
                                y=[gd_obj.scaled_linr.coef_[2]],
                                mode='markers', marker={'symbol': 'star'}), 1, 1)

    f = go.FigureWidget(fig)

    f['layout'].update(title='Gradient Descent')
    f['layout']['xaxis'].update(range=np.array([-3, 3]) + gd_obj.scaled_linr.coef_[1])
    f['layout']['yaxis'].update(range=np.array([-3, 3]) + gd_obj.scaled_linr.coef_[2])
    f['layout']['autosize'] = False
    f['layout']['width'] = 600
    f['layout']['height'] = 600
    f['layout']['showlegend'] = False

    names = ['contour', 'path', 'minimum']

    m1range = (np.array([-3, 3]) + gd_obj.scaled_linr.coef_[1])
    m2range = (np.array([-3, 3]) + gd_obj.scaled_linr.coef_[2])
    m1range = [np.ceil(m1range[0]), np.floor(m1range[1])]
    m2range = [np.ceil(m2range[0]), np.floor(m2range[1])]

    def update(lr, scaled, epochs, batch_size, m1, m2):
        gd_obj.train(m1, m2, 0, batch_size=int(batch_size), epochs=epochs, lr=lr, scaled=scaled)
        values = {'contour': {'x': None, 'y': None, 'z': gd_obj.contour.z},
                  'path': {'x': gd_obj.path.x, 'y': gd_obj.path.y},
                  'minimum': {'x': gd_obj.minimum.x, 'y': gd_obj.minimum.y}}
        with f.batch_update():
            for i, data in enumerate(f.data):
                try:
                    if values[names[i]]['z'] is not None:
                        data.z = values[names[i]]['z']
                except KeyError:
                    pass
                if values[names[i]]['y'] is not None:
                    data.y = values[names[i]]['y']
                if values[names[i]]['x'] is not None:
                    data.x = values[names[i]]['x']

    lr = FloatLogSlider(description='Learning Rate', value=0.0001, base=10, min=-4, max=-.5, step=.25)
    scaled = Checkbox(description='Scale Features', value=False)
    epochs = IntSlider(description='Epochs', value=100, min=100, max=500, step=100)
    batch_size = FloatLogSlider(description='Batch Size', value=16, base=2, min=0, max=6, step=1)
    m1 = IntSlider(description='x1', value=1, min=m1range[0], max=m1range[1], step=1)
    m2 = IntSlider(description='x2', value=1, min=m2range[0], max=m2range[1], step=1)

    return (f, interactive(update, lr=lr, scaled=scaled, epochs=epochs, batch_size=batch_size, m1=m1, m2=m2))

def build_figure_deriv():
    w = np.linspace(-2, 2, 100)

    def convex_j(w):
        return w ** 2

    def convex_djdw(w):
        return 2 * w

    def nonconvex_j(w):
        return np.sin(w*3) + w**2

    def nonconvex_djdw(w):
        return 3*np.cos(w*3) + 2*w

    j = convex_j
    djdw = convex_djdw

    w0 = -2
    lr = .2
    delta = lr * djdw(w0)

    traces = [go.Scatter(x=w, y=j(w), mode='lines', line={'color': 'black'}, showlegend=False),
             go.Scatter(x=[w0], y=[j(w0)], marker={'color': 'black'}, name='w before'),
             go.Scatter(x=[w0-delta], y=[j(w0-delta)], marker={'color': 'red'}, name='w after'),
             go.Scatter(x=[w0-delta, w0-delta], y=[j(w0), j(w0-delta)], showlegend=False, mode='lines', line={'color': 'gray', 'dash': 'dot'}),
             go.Scatter(x=[w0, w0-delta], y=[j(w0-delta), j(w0-delta)], showlegend=False, mode='lines', line={'color': 'gray', 'dash': 'dot'}),
             go.Scatter(x=[w0, w0-delta], y=[j(w0), j(w0-delta)], showlegend=False, mode='lines', line={'color': 'red', 'width': 2, 'dash': 'dash'}),
             go.Scatter(x=[w0, w0-delta], y=[j(w0), j(w0)], mode='lines', line={'color': 'red'}, name='- lr * dJ/dw(w)'),
             go.Scatter(x=[w0, w0], y=[j(w0), j(w0-delta)], showlegend=False, mode='lines', line={'color': 'gray'})]

    fig = go.Figure(traces, layout={'title': 'Gradient Descent', 'width': 600, 'height': 600, 'xaxis': {'zeroline': False}})
    f = go.FigureWidget(fig)

    functype = Dropdown(description='Function', options=['Convex', 'Non-convex'], value='Convex')
    bt_reset = Button(description='Reset')
    bt_step = Button(description='Step')
    lrate = FloatSlider(description='Learning Rate', value=.05, min=.05, max=1.1, step=.05)

    def update2(functype):
        if functype == 'Convex':
            j = convex_j
        else:
            j = nonconvex_j

        w0 = np.random.rand() * 4 - 2
        j0 = j(w0)
        with f.batch_update():
            f.data[0].y = j(f.data[0].x)
            for i in range(2, 8):
                f.data[i].visible = False
            f.data[1].x = [w0]
            f.data[1].y = [j0]
            f.data[2].x = [w0]
            f.data[2].y = [j0]

    def update(b):
        if functype.value == 'Convex':
            j = convex_j
            djdw = convex_djdw
        else:
            j = nonconvex_j
            djdw = nonconvex_djdw

        if b == bt_reset:
            w0 = np.random.rand() * 4 - 2
            j0 = j(w0)
            with f.batch_update():
                f.data[0].y = j(f.data[0].x)
                for i in range(2, 8):
                    f.data[i].visible = False
                f.data[1].x = [w0]
                f.data[1].y = [j0]
                f.data[2].x = [w0]
                f.data[2].y = [j0]
        else:
            w0, j0 = f.data[2].x[0], f.data[2].y[0]
            lr = lrate.value
            delta = lr * djdw(w0)
            w1 = w0-delta
            j1 = j(w1)
            with f.batch_update():
                for i in range(2, 8):
                    f.data[i].visible = True
                f.data[1].x = [w0]
                f.data[1].y = [j0]
                f.data[2].x = [w1]
                f.data[2].y = [j1]
                f.data[3].x = [w1, w1]
                f.data[3].y = [j0, j1]
                f.data[4].x = [w0, w1]
                f.data[4].y = [j1, j1]
                f.data[5].x = [w0, w1]
                f.data[5].y = [j0, j1]
                f.data[6].x = [w0, w1]
                f.data[6].y = [j0, j0]
                f.data[7].x = [w0, w0]
                f.data[7].y = [j0, j1]

    bt_step.on_click(update)
    bt_reset.on_click(update)

    update(bt_reset)
    return (f, interactive(update2, functype=functype), HBox((bt_reset, bt_step)), lrate)

if __name__ == '__main__':
    x1, x2, y = data()
    mygd = plotGradientDescent(x1, x2, y)
    vb = VBox(build_figure(mygd))
    vb.layout.align_items = 'center'
