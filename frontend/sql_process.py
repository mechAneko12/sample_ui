
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import requests
import json

def database_table(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_auto_height(autoHeight=True)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=5)
    gb.configure_side_bar()
    #gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    gb.configure_selection('single')
    gridOptions = gb.build()

    from st_aggrid.shared import GridUpdateMode
    data = AgGrid(df, 
                gridOptions=gridOptions, 
                enable_enterprise_modules=True, 
                allow_unsafe_jscode=True, 
                update_mode=GridUpdateMode.SELECTION_CHANGED)
    
    return data

def process_get(server_url):
    r = requests.get(server_url)
    return r

def process_post(content, server_url):
    r = requests.post(
        server_url,
        data=json.dumps(content),
        timeout=8000
    )

    return r