import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import squarify
import pandas as pd
app = dash.Dash()
server = app.server
app.config.supress_callback_exceptions = True
rfm = pd.read_csv('rfm.csv')



app.layout = html.Div([
    html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns",
                children=[
                    html.Div(
                        children=dcc.Graph(
                            id='treemap'   
                        )
                    )
                ]
            ),
            html.Div(
                className="six columns",
                children=html.Div([
                    dcc.Graph(
                        id='my-graph'
                    ),
                    dcc.Graph(
                        id='explore'
                    ),

                ])
            )
        ]
    )
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

@app.callback(
    Output('treemap', 'figure'),
    [Input('treemap', 'value')])
def treemap(value):
    
    x = 0.
    y = 0.
    width = 100.
    height = 100.
    
    #values = [500, 433, 78, 25, 25, 7]
    values = rfm['Segment'].value_counts().values
    index = rfm['Segment'].value_counts().index

    normed = squarify.normalize_sizes(values, width, height)
    rects = squarify.squarify(normed, x, y, width, height)

    # Choose colors from http://colorbrewer2.org/ under "Export"
    color_brewer = ['rgb(166,206,227)','rgb(31,120,180)','rgb(178,223,138)',
                    'rgb(51,160,44)','rgb(251,154,153)','rgb(227,26,28)',
                    'rgb(151,160,44)','rgb(51,130,144)','rgb(51,100,100)',
                    'rgb(251,160,144)']
    shapes = []
    annotations = []
    counter = 0

    for r in rects:
        shapes.append( 
            dict(
                type = 'rect', 
                x0 = r['x'], 
                y0 = r['y'], 
                x1 = r['x']+r['dx'], 
                y1 = r['y']+r['dy'],
                line = dict( width = 2 ),
                fillcolor = color_brewer[counter]
            ) 
        )
        annotations.append(
            dict(
                x = r['x']+(r['dx']/2),
                y = r['y']+(r['dy']/2),
                text = index[counter],
                showarrow = False
            )
        )
        counter = counter + 1
        if counter >= len(color_brewer):
            counter = 0

    figure = {
    'data': [go.Scatter(
        x = [ r['x']+(r['dx']/2) for r in rects ], 
        y = [ r['y']+(r['dy']/2) for r in rects ],
        text = [ str(v) for v in values ], 
        mode = 'text',
        )
    ],
    'layout': go.Layout(
        height=700, 
        width=700,
        xaxis={'showgrid':False, 'zeroline':False, 'showticklabels': False},
        yaxis={'showgrid':False, 'zeroline':False, 'showticklabels': False},
        shapes=shapes,
        annotations=annotations,
        hovermode='closest',
        )
    }
    return figure

@app.callback(
    Output("my-graph", "figure"),
    [Input('my-graph', 'value')])

def ugdate_figure(value):
    z = rfm['Frequency']
    trace = [go.Scatter3d(
        x=rfm['Recency'], y=rfm['Frequency'], z=rfm['Monetary'],
        mode='markers', marker={'size': 8 })]
    return {"data": trace,
            "layout": go.Layout(
                height=700, title="Recency Frequency Monetary",
                paper_bgcolor="#f3f3f3",
                scene={"aspectmode": "cube", "xaxis": {"title": "Recency" },
                       "yaxis": {"title": "Frequency" },
                       "zaxis": {"title": "Monetary" }})
            }

@app.callback(
    Output('explore', 'figure'),
    [Input('explore', 'value')])
def explor(value):
    data=pd.read_csv("customer.csv")
    Annual_Income=data.iloc[:,3]
    Spending_Score=data.iloc[:,4]
    Age=data.iloc[:,2]
    Gender=data.iloc[:,1]
    Index=data.iloc[:,0]

    trace1 = go.Scatter(
        x=Spending_Score,
        y=Gender,
        name = "Gender",
        mode = "markers"
    )
    trace2 = go.Scatter(
        x=Spending_Score,
        y=Age,
        xaxis='x2',
        yaxis='y2',
        name = "Age",
        mode = "markers"
    )
    trace3 = go.Scatter(
        x=Spending_Score,
        y=Annual_Income,
        xaxis='x3',
        yaxis='y3',
        name = "income",
        mode = "markers"
    )
    trace4 = go.Scatter(
        x=Spending_Score,
        y=Index,
        xaxis='x4',
        yaxis='y4',
        name = "total_score",
        mode = "markers"
    )
    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        xaxis=dict(
            domain=[0, 0.45]
        ),
        yaxis=dict(
            domain=[0, 0.45]
        ),
        xaxis2=dict(
            domain=[0.55, 1]
        ),
        xaxis3=dict(
            domain=[0, 0.45],
            anchor='y3'
        ),
        xaxis4=dict(
            domain=[0.55, 1],
            anchor='y4'
        ),
        yaxis2=dict(
            domain=[0, 0.45],
            anchor='x2'
        ),
        yaxis3=dict(
            domain=[0.55, 1]
        ),
        yaxis4=dict(
            domain=[0.55, 1],
            anchor='x4'
        ),
        title = 'Spending_Score'
    )
    fig = go.Figure(data=data, layout=layout)

    return fig






if __name__ == '__main__':
    app.run_server(debug=True)
