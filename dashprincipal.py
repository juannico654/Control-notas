import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, Input, Output
from dash import dash_table
from database import obtenerestudiantes
from flask import session


def cargar_datos():
    """Carga siempre datos frescos desde la BD."""
    dataf = obtenerestudiantes()

    if dataf is None or not isinstance(dataf, pd.DataFrame):
        return pd.DataFrame(columns=['Nombre', 'Edad', 'Carrera', 'Promedio', 'Desempeño'])

    for col in ['Edad', 'Promedio']:
        if col in dataf.columns:
            dataf[col] = pd.to_numeric(dataf[col], errors='coerce')

    return dataf.dropna(subset=['Edad', 'Promedio']).copy()


def creartablero(server):

    dataf_inicial = cargar_datos()

    carreras = sorted(dataf_inicial['Carrera'].dropna().unique().tolist())
    edad_min = int(dataf_inicial['Edad'].min()) if not dataf_inicial.empty else 18
    edad_max = int(dataf_inicial['Edad'].max()) if not dataf_inicial.empty else 30

    appnotas = dash.Dash(
        __name__,
        server=server,
        url_base_pathname='/dashprincipal/',
        suppress_callback_exceptions=True
    )

    # ─── LAYOUT ───────────────────────────────────────────────────────────────
    appnotas.layout = html.Div([

        # Navbar con links y botón de cerrar sesión
        html.Div([
            html.H2("📊 TABLERO AVANZADO", style={
                'color': 'white',
                'fontSize': '20px',
                'fontWeight': '700',
                'margin': '0'
            }),
            html.Div([
                html.A("➕ Registrar",     href="/registrar",    style=navbar_link_style()),
                html.A("📂 Cargue masivo", href="/carguemasivo", style=navbar_link_style()),
                html.A("🚪 Cerrar sesión", href="/logout",       style={
                    'color': 'white', 'textDecoration': 'none',
                    'fontSize': '14px', 'fontWeight': '600',
                    'backgroundColor': 'rgba(255,255,255,0.18)',
                    'borderRadius': '6px', 'padding': '7px 16px',
                    'transition': 'background 0.2s'
                }),
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'backgroundColor': '#1E1BD2',
            'padding': '14px 32px',
            'margin': '0 0 20px 0'
        }),

        # Intervalo para refrescar tras cargue masivo (cada 2s, se desactiva solo)
        dcc.Interval(id='intervalo_refresco', interval=2000, n_intervals=0, max_intervals=1),

        # Filtros
        html.Div([
            html.Label("Seleccionar carrera"),
            dcc.Dropdown(
                id='filtro_carrera',
                options=[{'label': c, 'value': c} for c in carreras],
                value=None,
                clearable=True,
                placeholder="Todas las carreras",
                style={'width': '100%'}
            ),
            html.Br(),

            html.Label("Rango de edad"),
            dcc.RangeSlider(
                id='slider_edad',
                min=edad_min,
                max=edad_max,
                step=1,
                value=[edad_min, edad_max],
                tooltip={'placement': 'bottom', 'always_visible': True}
            ),
            html.Br(),

            html.Label("Rango promedio"),
            dcc.RangeSlider(
                id='slider_promedio',
                min=0, max=5, step=0.2,
                value=[0, 5],
                marks={i: str(i) for i in range(6)},
                tooltip={'placement': 'bottom', 'always_visible': True}
            ),

            html.Br(),

            # Botón para limpiar filtros manualmente
            html.Button("🔄 Quitar filtros", id='btn_limpiar', n_clicks=0, style={
                'backgroundColor': '#e0e0e0',
                'border': 'none',
                'borderRadius': '8px',
                'padding': '8px 18px',
                'cursor': 'pointer',
                'fontSize': '14px'
            })

        ], style={
            'width': '80%', 'margin': 'auto', 'padding': '20px',
            'background': '#f8f9fa', 'borderRadius': '10px'
        }),

        html.Br(),

        # Banner que aparece tras cargue masivo
        html.Div(id='banner_cargue', style={'width': '80%', 'margin': 'auto'}),

        html.Br(),

        # KPIs
        html.Div(id='kpis', style={
            'display': 'flex', 'justifyContent': 'space-around',
            'flexWrap': 'wrap', 'gap': '15px',
            'margin': '20px auto', 'maxWidth': '1200px'
        }),

        html.Br(),

        # Tabla
        dcc.Loading(
            dash_table.DataTable(
                id='tabla', page_size=10,
                filter_action='native', sort_action='native',
                row_selectable='multi',
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '10px'},
                style_header={
                    'backgroundColor': '#1E1BD2',
                    'color': 'white', 'fontWeight': 'bold'
                }
            ), type='circle'
        ),

        html.Br(),

        dcc.Loading(dcc.Graph(id='gra_detallado'), type='default'),

        html.Br(),

        dcc.Tabs([
            dcc.Tab(label='Histograma',           children=[dcc.Graph(id='histograma')]),
            dcc.Tab(label='Dispersión',           children=[dcc.Graph(id='dispersion')]),
            dcc.Tab(label='Desempeño',            children=[dcc.Graph(id='pie')]),
            dcc.Tab(label='Promedio por Carrera', children=[dcc.Graph(id='barras')])
        ], style={'marginTop': '30px'})

    ], style={'padding': '20px', 'backgroundColor': '#f5f7fa', 'minHeight': '100vh'})


    # ─── CALLBACK: RESET DE FILTROS tras cargue masivo o botón limpiar ────────
    @appnotas.callback(
        [
            Output('filtro_carrera',  'value'),
            Output('slider_edad',     'value'),
            Output('slider_promedio', 'value'),
            Output('banner_cargue',   'children'),
            Output('intervalo_refresco', 'max_intervals')
        ],
        [
            Input('intervalo_refresco', 'n_intervals'),
            Input('btn_limpiar',        'n_clicks')
        ]
    )
    def resetear_filtros(n_intervals, n_clicks):
        dataf = cargar_datos()
        e_min = int(dataf['Edad'].min()) if not dataf.empty else 18
        e_max = int(dataf['Edad'].max()) if not dataf.empty else 30

        # Detectar si viene de cargue masivo
        desde_cargue = session.pop('cargue_masivo', False)

        banner = None
        if desde_cargue:
            banner = html.Div(
                "✅ Cargue masivo completado — mostrando todos los estudiantes sin filtros",
                style={
                    'backgroundColor': '#f0fff4',
                    'border': '1px solid #a3e4b7',
                    'color': '#1e7e34',
                    'padding': '12px 16px',
                    'borderRadius': '8px',
                    'fontSize': '14px',
                    'marginBottom': '8px'
                }
            )

        return None, [e_min, e_max], [0, 5], banner, 1


    # ─── CALLBACK PRINCIPAL ───────────────────────────────────────────────────
    @appnotas.callback(
        [
            Output('tabla',      'data'),
            Output('tabla',      'columns'),
            Output('kpis',       'children'),
            Output('histograma', 'figure'),
            Output('dispersion', 'figure'),
            Output('pie',        'figure'),
            Output('barras',     'figure')
        ],
        [
            Input('filtro_carrera',  'value'),
            Input('slider_edad',     'value'),
            Input('slider_promedio', 'value')
        ]
    )
    def actualizar_comp(carrera, rango_edad, rango_prom):

        dataf     = cargar_datos()
        fig_empty = px.scatter(title="Sin datos disponibles")

        if dataf.empty:
            kpi_vacio = html.Div("No hay datos", style={'color': 'red', 'fontSize': 18})
            return [], [], [kpi_vacio], fig_empty, fig_empty, fig_empty, fig_empty

        df_work = dataf.copy()
        df_work['Edad']     = df_work['Edad'].astype(float)
        df_work['Promedio'] = df_work['Promedio'].astype(float)

        # Si no hay carrera seleccionada, mostrar todos
        if carrera:
            filtro = df_work[df_work['Carrera'] == carrera].copy()
        else:
            filtro = df_work.copy()

        # Aplicar rangos
        filtro = filtro[
            (filtro['Edad']     >= float(rango_edad[0])) &
            (filtro['Edad']     <= float(rango_edad[1])) &
            (filtro['Promedio'] >= float(rango_prom[0])) &
            (filtro['Promedio'] <= float(rango_prom[1]))
        ].copy()

        print(f"Filtro: carrera={carrera}, edad={rango_edad}, prom={rango_prom}")
        print(f"Filas resultantes: {len(filtro)}")

        if filtro.empty:
            fig_vacio = px.scatter(title="No hay estudiantes con estos filtros")
            kpis = [
                html.Div([html.H4("Promedio"),          html.H2("—")], style=kpi_style()),
                html.Div([html.H4("Total estudiantes"), html.H2(0)],   style=kpi_style()),
                html.Div([html.H4("Máxima"),            html.H2("—")], style=kpi_style()),
            ]
            return [], [], kpis, fig_vacio, fig_vacio, fig_vacio, fig_vacio

        prom  = round(filtro['Promedio'].mean(), 2)
        total = len(filtro)
        maxi  = round(filtro['Promedio'].max(), 2)

        kpis = [
            html.Div([html.H4("Promedio"),          html.H2(prom)],  style=kpi_style()),
            html.Div([html.H4("Total estudiantes"), html.H2(total)], style=kpi_style()),
            html.Div([html.H4("Máxima"),            html.H2(maxi)],  style=kpi_style()),
        ]

        titulo_carrera = carrera if carrera else "Todas las carreras"

        histo = px.histogram(
            filtro, x='Promedio', nbins=12,
            title='Distribución de Promedios',
            template='plotly_white'
        )

        dispersion = px.scatter(
            filtro, x='Edad', y='Promedio',
            color='Desempeño',
            title='Edad vs Promedio',
            template='plotly_white'
        )

        pie = px.pie(
            filtro, names='Desempeño',
            title='Distribución por Desempeño',
            hole=0.4, template='plotly_white'
        )

        barras = px.bar(
            filtro.groupby('Carrera')['Promedio'].mean().reset_index(),
            x='Carrera', y='Promedio',
            color='Carrera',
            title=f'Promedio por Carrera — {titulo_carrera}',
            template='plotly_white'
        )

        columns = [{"name": i, "id": i} for i in filtro.columns]

        return (
            filtro.to_dict('records'), columns, kpis,
            histo, dispersion, pie, barras
        )


    # ─── CALLBACK DETALLE ─────────────────────────────────────────────────────
    @appnotas.callback(
        Output('gra_detallado', 'figure'),
        Input('tabla', 'derived_virtual_data'),
        Input('tabla', 'derived_virtual_selected_rows')
    )
    def actualizar_detalle(rows, selected_rows):
        if not rows:
            return px.scatter(title='Selecciona filas en la tabla para ver detalle')

        df = pd.DataFrame(rows)
        if selected_rows:
            df = df.iloc[selected_rows]

        fig = px.scatter(
            df, x='Edad', y='Promedio',
            color='Desempeño', size='Promedio',
            hover_data=['Nombre', 'Carrera'],
            title='Análisis detallado de selección',
            template='plotly_white'
        )
        return fig


    return appnotas


def navbar_link_style():
    return {
        'color': 'white',
        'textDecoration': 'none',
        'fontSize': '14px',
        'opacity': '0.85',
        'fontWeight': '500'
    }


def kpi_style():
    return {
        'backgroundColor': '#3498db',
        'color': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'textAlign': 'center',
        'minWidth': '180px',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
    }