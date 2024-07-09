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
    {'id': 1, 'page': 1},
    {'id': 2, 'page': 2},
    {'id': 3, 'page': 0},
    {'id': 4, 'page': 3}
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
    file_key = f"hourly-sales-and-labor-{event_date}.pdf"

    try:

        # Fetch the PDF file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        pdf_content = response['Body'].read()

        # Iterate through the stores
        for store in stores:

            # Extract text from the PDF
            text = extract_text_from_pdf(pdf_content, store['page'])

            # clean the text
            text = text.replace('\n', ' ').replace('\r', ' ')

            """Extract items from text"""
            # Capture the 6th number after ' 1:00 AM' (be careful to include the space before the number)
            # For example in the text below I want to capture the number 1.00
            # 1:00 AM $0.00 0 $0.00 0 $0.00 1.00 $0.00 0.00%
            match = re.search(r' 1:00 AM \$\d+\.\d+ \d+ \$\d+\.\d+ \d+ \$\d+\.\d+ (\d+\.\d+) \$\d+\.\d+ \d+\.\d+%', text)

            if match:
                overnight_clockins = float(match.group(1))
            else:
                overnight_clockins = None
                print(f"Overnight Clockin not found for store: {store['id']}")

            """Insert the extracted items into the Supabase database"""
            supabase.table('hourly').insert(
                {'store_id': store['id'], 'overnight_clockins': overnight_clockins, 'date': event_date}
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
