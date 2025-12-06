import plotly.graph_objects as go
from ui.plotter.base.BasePlotter import BasePlotter

class BinomialTreePlotter(BasePlotter):
    NODE_WIDTH = 0.38
    NODE_HEIGHT = 0.28
    NODE_OFFSET = 0.15

    def __init__(self, n_steps, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asset_prices, self.option_prices = self.results
        self.n_steps = n_steps
        self._build_nodes_and_edges()

    def generate_plot(self):
        # Convert nodes to coordinates
        x = [i for (i, _, _) in self.asset_prices_nodes]
        y_asset_prices = [j - i / 2 + self.NODE_OFFSET for (i, j, _) in self.asset_prices_nodes]
        y_option_price = [j - i / 2 - self.NODE_OFFSET for (i, j, _) in self.asset_prices_nodes]
        text = [f"Step {i}<br>Up {j}<br>S={S:.4f}" for (i, j, S) in self.asset_prices_nodes]

        # Create edges for Plotly
        edge_x = []
        edge_y = []
        for ((i1, j1), (i2, j2)) in self.edges:
            edge_x += [i1 + self.NODE_WIDTH / 2, i2 - self.NODE_WIDTH / 2, None]
            edge_y += [j1 - i1 / 2, j2 - i2 / 2, None]

        # Create shapes where the prices are going to be displayed
        shapes = self._create_shapes()

        # Plot
        fig = go.Figure()

        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode='lines',
            line=dict(color='#615fff', width=2),
            text=[f"edge" for (i, j) in self.edges],
            hoverinfo='none'
        ))

        # Asset price values
        fig.add_trace(go.Scatter(
            x=x, y=y_asset_prices,
            mode='text',
            text=[f"{S:.4f}" for (_, _, S) in self.asset_prices_nodes],
            textposition='middle center',
            hovertext=text,
            hoverinfo='text',
            textfont=dict(color="white")
        ))

        # Option prices
        fig.add_trace(go.Scatter(
            x=x, y=y_option_price,
            mode='text',
            text=[f"{S:.4f}" for (_, _, S) in self.option_prices_nodes],
            textposition='middle center',
            hovertext=text,
            hoverinfo='text',
            textfont=dict(color="white", weight='bold')
        ))

        fig.update_layout(
            title='Binomial Tree for Option Pricing',
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor=None,
            margin=dict(l=0, r=0, t=50, b=0),
            height=max(60 * self.n_steps, 600),
            width=max(120 * self.n_steps, 1450),
            shapes=shapes,
        )
        return fig

    def _build_nodes_and_edges(self):
        self.asset_prices_nodes = []
        self.option_prices_nodes = []
        self.edges = []

        for i in range(self.n_steps + 1):
            for j in range(i + 1):
                self.asset_prices_nodes.append((i, j, self.asset_prices[i][i - j]))
                self.option_prices_nodes.append((i, j, self.option_prices[i][i - j]))
                if i > 0:
                    if j > 0:
                        self.edges.append(((i - 1, j - 1), (i, j)))
                    if j < i:
                        self.edges.append(((i - 1, j), (i, j)))

    def _create_shapes(self):
        shapes = []

        for (i, j, _) in self.asset_prices_nodes:
            x_center = i
            y_center = j - i/2 + self.NODE_OFFSET

            shapes.append(dict(
                type="rect",
                x0=x_center - self.NODE_WIDTH/2,
                x1=x_center + self.NODE_WIDTH/2,
                y0=y_center - self.NODE_HEIGHT/2,
                y1=y_center + self.NODE_HEIGHT/2,
                line=dict(color="#1d293d", width=2),
                fillcolor="#314158",
                layer="below"
            ))

        for (i, j, _) in self.option_prices_nodes:
            x_center = i
            y_center = j - i/2 - self.NODE_OFFSET

            shapes.append(dict(
                type="rect",
                x0=x_center - self.NODE_WIDTH/2,
                x1=x_center + self.NODE_WIDTH/2,
                y0=y_center - self.NODE_HEIGHT/2,
                y1=y_center + self.NODE_HEIGHT/2,
                line=dict(color="#1d293d", width=2),
                fillcolor="#0f172b",
                layer="below"
            ))
        return shapes
