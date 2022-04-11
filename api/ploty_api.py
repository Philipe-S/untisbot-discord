from api.models.theme_data import ThemeData
import plotly.graph_objects as go

class PlotyApi:
    def __init__(self, themeData: ThemeData):
        self.themeData = themeData
        self.layout = go.Layout(
            margin=go.layout.Margin(
                l=8,
                b=8,
                r=8,
                t=8
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            # width=900,
        )
    def getTheme(self) -> ThemeData:
        return self.themeData
    def build(self, headers: [str], cellData: [[str]], colColors: [[str]]):
        cells = go.table.Cells(values=cellData,
                          line_color='darkslategray',
                          fill_color=colColors,
                          align=['center'],
                          font=dict(color='black', size=14))
        header = go.table.Header(values=headers,
                           line_color='darkslategray',

                           align='center',
                           font=dict(color='black', size=16)
                      )
        table = go.Table(header=header, cells=cells)
        self.figure = go.Figure(data=[table], layout=self.layout)

    def export(self):
        self.figure.write_image("images\\timetable.png", width=5*175,height=4*200, scale=1)


