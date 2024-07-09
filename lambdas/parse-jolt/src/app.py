import os
import json
import boto3
from pypdf import PdfReader
from io import BytesIO
import re
from supabase import create_client
import datetime
from shared import get_secret


s3 = boto3.client('s3')

# Create a Supabase client
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = get_secret()['service_roll']
supabase = create_client(supabase_url, supabase_key)

stores = [
    {'id': 1, 'jolt_id': '100'},
    {'id': 2, 'jolt_id': '200'},
    {'id': 3, 'jolt_id': '300'},
    {'id': 4, 'jolt_id': '400'}
]


def extract_text_from_pdf(pdf_content, page_number):
    pdf_reader = PdfReader(BytesIO(pdf_content))
    page = pdf_reader.pages[page_number]
    return page.extract_text()


def lambda_handler(event, context):
    # Fetch the S3 bucket name from environment variables
    bucket_name = os.getenv('S3_BUCKET')
    # Yesterday's date
    event_date = datetime.datetime.now().date()
    event_date = event_date - datetime.timedelta(days=1)
    event_date = event_date.strftime('%Y-%m-%d')
    # set the file key
    file_key = f"jolt-{event_date}.pdf"

    try:

        # Fetch the PDF file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        pdf_content = response['Body'].read()

        # Extract text from the PDF
        text = extract_text_from_pdf(pdf_content, 0)

        # clean the text
        text = text.replace('\n', ' ').replace('\r', ' ')

        print(text)

        # Iterate through the stores
        for store in stores:

            """Extract items from text"""
            # Complete % for the store which is the first value in the parentheses after the store id note
            # that the value may be in the format xx.xx% or xx% so the regex must account for both
            # For example, for store 100, the regex should match 60.98% or 60%
            # An example for store['jolt_id'] = 200 that should match to 79.49% or 79% is below
            # 200- Stuarts Draft DQ31 (79.49%) 26 (66.67%) 5
            store_id = store['jolt_id']
            pattern = f'{store_id}-' + r".*?\(([\d.%]+)\)"
            complete_percent = re.search(pattern, text)

            if complete_percent.group(1):
                # remove the percentage sign
                complete_percent = complete_percent.group(1).replace('%', '')
                # turn into a float
                complete_percent = float(complete_percent)
            else:
                complete_percent = None
                print(f"Complete percent not found for store: {store['id']}")

            """Insert the extracted items into the Supabase database"""
            supabase.table('jolt').insert(
                {'store_id': store['id'], 'complete_percent': complete_percent, 'date': event_date}
            ).execute()

        return {
            'statusCode': 200
        }

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error processing PDF', 'error': str(e)}),
        }
