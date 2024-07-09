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
    {'id': 1, 'abbreviation': 'bw'},
    {'id': 2, 'abbreviation': 'sd'},
    {'id': 3, 'abbreviation': 'ek'},
    {'id': 4, 'abbreviation': 'vr'}
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

    try:

        for store in stores:

            # set the file key
            file_key = f"hme-{store['abbreviation']}-{event_date}.pdf"

            # Fetch the PDF file from S3
            response = s3.get_object(Bucket=bucket_name, Key=file_key)
            pdf_content = response['Body'].read()

            # Extract text from the PDF
            text = extract_text_from_pdf(pdf_content, 0)

            # clean the text
            text = text.replace('\n', ' ').replace('\r', ' ')

            # regex pattern to extract the 'Lane Total' time
            # it should match '03:33' in the example text
            pattern = r"Lane Total\s+(\d+)\s+(\d+:\d+)"
            match = re.search(pattern, text)
            if match:
                ave_time = match.group(2)
                # convert mm:ss string to seconds int
                ave_time = int(ave_time.split(':')[0]) * 60 + int(ave_time.split(':')[1])
            else:
                ave_time = None
                print(f"Average time (hme) not found for store: {store['id']}")

            """Insert the extracted items into the Supabase database"""
            supabase.table('hme').insert(
                {'store_id': store['id'], 'average_time': ave_time, 'date': event_date}
            ).execute()

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Successfully processed PDF'}),
        }

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error processing PDF', 'error': str(e)}),
        }
