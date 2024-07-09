# Automated Business Intelligence Dashboard

## Description
An automated workflow that converts a small business's daily service provider reports (sales, payroll, service times) into a simple business intelligence dashboard.

## General
### Problem
Many small and medium-sized businesses use a collection of third-party services to handle various aspects of their operations. These services often provide daily reports that are useful for monitoring business health. However, these reports are typically in a format that is not easily consumable, forcing business owners to sift through multiple pages to extract relevant information.

### Solution
Automate the process of extracting relevant information from these reports and host a simple business intelligence dashboard that the business owner can access to see the relevant information at a glance.

![Demo](assets/demo.gif)

## Workflow
![Workflow](assets/workflow.png)
1. **Client Inbox (Zapier)**
   - Watch for emails from third-party providers
   - Extract the attachments and send to dedicated email addresses

2. **Automation Inbox (ActivePieces)**
   - ActivePieces server hosted locally on a Raspberry Pi with Docker Compose
   - Watch for emails from the client inbox
   - Upload the attachments to AWS S3

4. **Lambdas**
   - Schedule to run daily
   - Parse the reports and extract relevant information
   - Store the reports in Supabase for easy UI access

5. **Dashboard (Vue3)**
   - Basic Auth with Supabase
   - Display the relevant information in a simple, easy-to-read format
   - Hosted on Vercel

Note: Step 1 and 2 should ideally be combined into one service, but Zapier was necessary for handling emails with multiple attachments.

## Stack
- Zapier
- ActivePieces
- AWS S3
- AWS Lambda (Python)
- Supabase
- Vue3
- Vercel

## Notes and Learnings
### Modularity
Breaking the workflow into smaller, modular pieces made it more resilient to errors and easier to debug. For example, if email handling fails, the rest of the workflow can still run. This also simplifies testing individual components. Adding a new third-party provider in the future will only require adding a new module to the workflow.

### Locally Developed Lambda Functions (SAM)
Developing Lambda functions locally using the AWS SAM CLI was much faster than using the AWS console. This allowed for quicker iteration and testing. It was my first time using the SAM CLI, and I found it very useful.

### Hosting Workflow Automations Locally (ActivePieces)
While Zapier is the go-to for automating workflows, it can be pricey for a few tasks. ActivePieces, an open-source alternative, was used for most automations. However, Zapier was necessary for handling emails with multiple attachments. Hosting the ActivePieces server locally on a Raspberry Pi reduced recurring costs by ~$30/month. This project was also my first experience with Docker, which proved to be a useful tool for hosting the ActivePieces server.

### Parsing PDFs
Most third-party reports are in PDF format, which are harder to extract data from compared to plain text files. Initially, I used a paid service to parse PDFs but later found multiple Python libraries that did the job. In the end, [pypdf](https://pypi.org/project/pypdf/) was the best fit for my use case.

### Storing the Reports
While not necessary, storing the reports allows for later access to valuable data. Additionally, it made the workflow more modular and resilient to errors. AWS S3 is both cheap and easy to use for this purpose.

### LLMs are Great at Writing Regex and Styling!
Part of the project involved finding the correct metrics in stringified PDFs. LLMs excelled at writing regex, saving me hours. Additionally, LLMs are great at generating visually appealing web apps. Using Tailwind CSS with LLMs allowed for quick iteration without refactoring any CSS.

### Production with Third-Party Data
The main challenge in production was handling various edge cases with third-party vendors, such as missing reports. Ensuring the system could handle these cases gracefully without crashing was crucial.

## Costs
- Raspberry Pi: ~$50
- Zapier: Free Tier
- AWS S3: $0.023/GB (recurring)

## Todo / Possible Extensions
- [ ] Create weekly and monthly reports
- [x] Add trends or historical data to the reports
- [ ] Improve error handling and messaging
- [x] Add charts and graphs to the reports
- [x] Host on a cloud server instead of a local server for better resilience (my niece likes unplugging my Raspberry Pi)
- [ ] Move Zapier functionality to ActivePieces to reduce costs
- [ ] Delete S3 files after processing to reduce storage costs
- [x] Host ActivePieces locally to reduce costs
