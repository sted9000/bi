export const dataMixin = {
    data: () => ({
        storeProperties: {
            1: {borderColor: '#36A2EB', backgroundColor: '#9BD0F5'},
            2: {borderColor: '#FFCE56', backgroundColor: '#FFEB9C'},
            3: {borderColor: '#4BC0C0', backgroundColor: '#96D8D8'},
            4: {borderColor: '#9966FF', backgroundColor: '#CBB3FF'}
        },
        metrics: [
            {id: 1, value: 'net_sales', text: 'Net Sales'},
            {id: 2, value: 'labor_percent', text: 'Labor %'},
            {id: 3, value: 'sales_per_labor_hour', text: 'Sales per Labor Hour'},
            {id: 4, value: 'donation_count', text: 'Donation Count'},
            {id: 5, value: 'refunds', text: 'Refunds'},
            {id: 6, value: 'customer_count', text: 'Customer Count'},
            {id: 7, value: 'total', text: 'Break Total'},
            {id: 8, value: 'average_time', text: 'HME Average'},
            {id: 9, value: 'overnight_clockins', text: 'Overnight Clockins'},
            {id: 10, value: 'complete_percent', text: 'Jolt Complete %'},
            {id: 11, value: 'over_short', text: 'Over/Short'},


        ],
        tables: {
            'net_sales': 'sales',
            'labor_percent': 'sales',
            'sales_per_labor_hour': 'sales',
            'donation_count': 'sales',
            'refunds': 'sales',
            'customer_count': 'sales',
            'total': 'breaks',
            'average_time': 'hme',
            'overnight_clockins': 'hourly',
            'complete_percent': 'jolt',
            'over_short': 'till',

        }
    })
};
