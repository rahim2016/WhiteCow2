from .config import *
import requests, json
import logging
import pandas as pd
import numpy as np
from datetime import datetime

logger = logging.getLogger('django')


def property_search_query(url, query_params):

        # header
        headers = {
            "x-rapidapi-host": host,
            "x-rapidapi-key": api_key
        }
       
        # response

        response = requests.request("GET", url, headers=headers, params=query_params)
        if response.ok:
            return response
        else:
            logger.error(f"Error in making API request ")
            return None
 
def process_query_response(response):
    if response is not None:  
        content = json.loads(response.content)
        df = pd.DataFrame.from_dict(content['data']['results'])
        return df 
    else:
        return None


def get_estimate_value(property_id):
    try:
        url = url_estimate
        querystring = {"property_id":property_id}
        headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': host
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.content)
        return data
    except:
        return None


def calculate_deal(list_property_id, df):
    deal_dict = {}
    for_cast = None
    for list_ in list_property_id:
        data = get_estimate_value(list_)
        try:
            for_cast= data['data']['forecast_values'][0]['estimates'][-1]['estimate']
        except:
            for_cast= 0
        df2 =df[df["property_id"] == list_]["list_price"]
        initial=df2.to_list()[0]
        percentage_change = ((for_cast - initial)/initial) *100
        deal_dict[list_] = percentage_change
    return deal_dict

def get_deal_datafrane(deal_dict, df):
    sort_deal = sorted(deal_dict.items(), key=lambda x: x[1], reverse=True)
    property_id_deal = [k[0] for k in sort_deal][:3]
    df_deal = df[df['property_id'].isin(property_id_deal) ]
    return df_deal









def formatting(df):
    #df.drop('Unnamed: 0', inplace = True, axis = 1)
    #df.drop('Unnamed: 0.1', inplace = True, axis = 1)

    column_names_json = ['primary_photo','source','description','branding','lead_attributes','photos',
    'flags','products','other_listings','location']
    column_names_date_time = ['last_update_date','list_date']

    
    for col in column_names_json:
        df[col] = df[col].apply(json.dumps)
        
    for col in column_names_json:
        df[col] = df[col].apply(json.loads)
    
    for i in df.itertuples():
        
        df['last_update_date'] = i.last_update_date.replace('T',' ') 
        df['list_date'] = i.last_update_date.replace('T',' ')
       
    for i in df.itertuples():
        df['last_update_date'] = i.last_update_date.replace('Z','')
        df['list_date'] = i.last_update_date.replace('Z','')

    for j in df.itertuples():
        df['last_update_date'] = datetime.strptime(i.last_update_date, "%Y-%m-%d %H:%M:%S")
        df['list_date'] = datetime.strptime(i.last_update_date, "%Y-%m-%d %H:%M:%S")




    return df



def get_query_params(address, assets):
        """
        This method is to get the user's query parameters. It will be later used to make a get request to the realestate API
        to get data.
        """
        address_params = vars(address)

        asset_params = vars(assets)

        query_params = {}
        query_params.update(address_params)
        query_params.update(asset_params)
        query_params.pop('_state')
        query_params.pop('id')
        #query_params = json.dumps(query_params)
        #query_params = query_params.replace('"', "")
        # query_params.update(compute_params)

        return query_params