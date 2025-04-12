export const customer = {
    name: 'Layla Odam',
    id: 'CUST-2048',
    email: 'layla.odam@bank.com',
    phone: '+43 660 123456',
    address: 'Seestadtstraße 1, 1220 Vienna, Austria',
    accountNumber: '9876543210',
    status: 'Active',
    birthdate: '1990-04-18',
    lastLogin: '2025-04-11 09:42',
    avatar: 'https://i.pravatar.cc/150?img=32',
    financial_data: {
        accounts: [
            {
                type: 'checking',
                iban: 'AT611904300234573201',
                balance: 4523.75,
                currency: 'EUR',
                monthly_inflow: 3200.0,
                monthly_outflow: 2850.5,
                last_updated: '2025-04-11'
            },
            {
                type: 'savings',
                iban: 'AT121904300234573202',
                balance: 15300.0,
                currency: 'EUR',
                interest_rate: 0.75,
                goal: 'Emergency fund',
                last_updated: '2025-04-11'
            }
        ],
        investments: [
            {
                type: 'mutual_fund',
                name: 'Global Equity Growth Fund',
                value: 8700.5,
                currency: 'EUR',
                risk_level: 'medium',
                performance_ytd: 6.3
            },
            {
                type: 'stock',
                name: 'Apple Inc.',
                ticker: 'AAPL',
                value: 2450.0,
                currency: 'EUR',
                shares: 10,
                purchase_price: 210.0,
                current_price: 245.0
            }
        ],
        loans: [
            {
                type: 'mortgage',
                amount: 250000.0,
                remaining_balance: 192000.0,
                monthly_payment: 950.0,
                interest_rate: 1.8,
                term_years: 25,
                start_date: '2019-06-01',
                end_date: '2044-06-01'
            },
            {
                type: 'personal_loan',
                amount: 10000.0,
                remaining_balance: 2200.0,
                monthly_payment: 200.0,
                interest_rate: 3.5,
                term_years: 5,
                start_date: '2021-03-01',
                end_date: '2026-03-01'
            }
        ],
        credit_cards: [
            {
                card_type: 'Visa Gold',
                credit_limit: 5000.0,
                current_balance: 1450.3,
                last_payment_date: '2025-04-05',
                minimum_due: 90.0,
                due_date: '2025-04-20'
            }
        ],
        income: {
            source: 'Software Engineer - TechCorp GmbH',
            monthly_salary: 3200.0,
            bonus: 1000.0,
            last_bonus_date: '2024-12-20',
            salary_payment_day: 25
        },
        expenses: {
            fixed_monthly: [
                { description: 'Rent', amount: 950.0 },
                { description: 'Utilities', amount: 180.0 },
                { description: 'Insurance', amount: 130.0 }
            ],
            variable_monthly: [
                { description: 'Groceries', average: 350.0 },
                { description: 'Dining', average: 200.0 },
                { description: 'Transport', average: 120.0 }
            ]
        },
        financial_goals: [
            {
                goal: 'Buy a house',
                target_amount: 60000.0,
                saved_amount: 22000.0,
                deadline: '2027-12-01'
            },
            {
                goal: "Children's Education Fund",
                target_amount: 30000.0,
                saved_amount: 12500.0,
                deadline: '2035-09-01'
            }
        ],
        credit_score: {
            score: 748,
            rating: 'Good',
            last_checked: '2025-03-20'
        }
    },
    hobbies: ['Traveling', 'Photography', 'Cycling'],
    avoidTopics: ['Divorce', 'Lost Job'],
    behavior: {
        appLogins: 21,
        transactions: 48,
        engagement: 66
    },
    suggestions: ['Discuss investment options', 'Offer savings plan upgrade'],
    interactions: [
        { date: '2025-04-01', note: 'Requested balance transfer info' },
        { date: '2025-03-22', note: 'Asked about fixed deposit rates' }
    ],
    summary: 'Layla is a consistent mobile banking user with good credit and moderate risk. Shs responsive and values efficiency.'
};