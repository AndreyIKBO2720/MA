import dash
from dash import html, dcc, Input, Output
import plotly.graph_objs as go
from sqlalchemy import func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Date

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'
engine = create_engine(URL)
session_local = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


class Purchase(Base):
    __tablename__ = 'purchase_bashkirov'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    text = Column(String, nullable=False)
    price = Column(Float, nullable=False)


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='daily-expenses-graph'),
    html.Button('Обновить данные', id='refresh-data', n_clicks=0)
])


@app.callback(
    Output('daily-expenses-graph', 'figure'),
    Input('refresh-data', 'n_clicks')
)
def update_graph(n_clicks):
    results = session_local.query(
        Purchase.date,
        func.sum(Purchase.price).label('total_price')
    ).group_by(Purchase.date).order_by(Purchase.date).all()

    dates = [result.date for result in results]
    totals = [float(result.total_price) for result in results]

    figure = go.Figure(data=[go.Bar(x=dates, y=totals)])
    figure.update_layout(
        title='Сумма трат по дням',
        xaxis_title='Дата',
        yaxis_title='Сумма трат',
        margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
        hovermode='closest'
    )
    return figure


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8000)
