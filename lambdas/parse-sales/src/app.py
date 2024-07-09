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
    {'id': 1, 'page': 3},
    {'id': 2, 'page': 6},
    {'id': 3, 'page': 0},
    {'id': 4, 'page': 9}
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
    file_key = f"sales-{event_date}.pdf"

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
            # Net sales (may or may not have commas or decimals)
            net_sales = re.search(r"Net Sales\s+\$([\d.,]+)", text)

            # Customer count
            customer_count = re.search(r"Guest Count:\s+(\d+)", text)

            # Labor percent
            labor_percent = re.search(r"Labor Percent:\s+([\d.]+)%", text)

            # Sales per labor hour
            sales_per_labor_hour = re.search(r"Sales Per Labor Hour:\s+\$([\d.]+)", text)

            # Donation count
            donation_count = re.search(r"Donation Count:\s+(\d+)", text)

            # Refunds
            refunds = re.search(r"Refunds\s+\$([\d.]+)", text)

            """Format the extracted items"""
            if net_sales:
                net_sales = float(net_sales.group(1).replace(",", ""))
            else:
                net_sales = None
                print(f"Net sales not found for store: {store['id']}")

            if customer_count:
                customer_count = int(customer_count.group(1))
            else:
                customer_count = None
                print(f"Customer count not found for store: {store['id']}")

            if labor_percent:
                labor_percent = float(labor_percent.group(1))
            else:
                labor_percent = None
                print(f"Labor percent not found for store: {store['id']}")

            if sales_per_labor_hour:
                sales_per_labor_hour = float(sales_per_labor_hour.group(1))
            else:
                sales_per_labor_hour = None
                print(f"Sales per labor hour not found for store: {store['id']}")

            if donation_count:
                donation_count = int(donation_count.group(1))
            else:
                donation_count = None
                print(f"Donation count not found for store: {store['id']}")

            if refunds:
                refunds = float(refunds.group(1))
            else:
                refunds = None
                print(f"Refunds not found for store: {store['id']}")

            """Insert the extracted items into the Supabase database"""
            supabase.table('sales').insert(
                {'store_id': store['id'], 'net_sales': net_sales, 'customer_count': customer_count, 'labor_percent': labor_percent,
                 'sales_per_labor_hour': sales_per_labor_hour, 'donation_count': donation_count, 'refunds': refunds, 'date': event_date}
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
