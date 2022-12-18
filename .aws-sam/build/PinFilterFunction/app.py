import json
import boto3
import pandas as pd
from criteria_config import config
from functions import pin_filter

s3_client = boto3.client('s3')
bucket_name = "oc-data-config"
# s3_file_name = "brand_comms.csv"
s3_file_name = 'pincodes.csv'
resp = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)
pin_config_df = pd.read_csv(resp['Body'])
pin_config_df = pin_config_df[['partnerid', 'Pincode', 'location_type']]
pin_code_exc_df = pin_config_df[pin_config_df['location_type'] == 'loc_pincode_exc']
pin_code_inc_df = pin_config_df[pin_config_df['location_type'] == 'loc_pincode_inc']
del pin_config_df

def lambda_handler(event, context):
    pin = event['pin']
    category_code = event['categoryCode']
    config_df = pd.json_normalize(config)
    config_df = config_df[config_df['Category ID'] == category_code]
    partner_ids = list(set(config_df['Partner ID'].to_list()))
    partner_ids = [str(x) for x in partner_ids]
    return {
        "statusCode": 200,
        "partners" : pin_filter(partner_ids, pin_code_inc_df, pin_code_exc_df, pin)
    }
