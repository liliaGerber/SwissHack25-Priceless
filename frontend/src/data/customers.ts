import {Customer} from "@/types/Customer.ts";

export const customers = [
    {
        name: 'Layla Odam',
        id: '67fac30146f3d88f8354ca28',
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
                    {description: 'Rent', amount: 950.0},
                    {description: 'Utilities', amount: 180.0},
                    {description: 'Insurance', amount: 130.0}
                ],
                variable_monthly: [
                    {description: 'Groceries', average: 350.0},
                    {description: 'Dining', average: 200.0},
                    {description: 'Transport', average: 120.0}
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
        suggestions: ['Discuss retirement plan', 'Offer savings plan upgrade'],
        interactions: [
            {date: '2025-04-01', note: 'Requested balance transfer info'},
            {date: '2025-03-22', note: 'Asked about fixed deposit rates'}
        ],
        upcomingTopics: ['Buy a house', 'Investment'],
        summary: 'Layla is a consistent mobile banking user with good credit and moderate risk. Shs responsive and values efficiency.'
    }, {
        name: 'Ben Dajsdfgjh',
        id: '67fac30146f3d88f8354ca27',
        email: 'ben.dajsdfgjh@finbank.com',
        phone: '+43 699 987654',
        address: 'Landstraßer Hauptstraße 44, 1030 Vienna, Austria',
        accountNumber: '1234567890',
        status: 'Inactive',
        birthdate: '1985-07-12',
        lastLogin: '2025-03-05 14:30',
        avatar: 'https://i.pravatar.cc/150?img=58',
        financial_data: {
            accounts: [
                {
                    type: 'checking',
                    iban: 'AT830000000123456789',
                    balance: 892.15,
                    currency: 'EUR',
                    monthly_inflow: 2100.0,
                    monthly_outflow: 1950.2,
                    last_updated: '2025-04-10'
                },
                {
                    type: 'savings',
                    iban: 'AT830000000987654321',
                    balance: 4300.0,
                    currency: 'EUR',
                    interest_rate: 1.1,
                    goal: 'Vacation fund',
                    last_updated: '2025-04-10'
                }
            ],
            investments: [
                {
                    type: 'mutual_fund',
                    name: 'Balanced Income Fund',
                    value: 3100.0,
                    currency: 'EUR',
                    risk_level: 'low',
                    performance_ytd: 2.5
                },
                {
                    type: 'stock',
                    name: 'Tesla Inc.',
                    ticker: 'TSLA',
                    value: 5700.0,
                    currency: 'EUR',
                    shares: 15,
                    purchase_price: 340.0,
                    current_price: 380.0
                }
            ],
            loans: [
                {
                    type: 'mortgage',
                    amount: 180000.0,
                    remaining_balance: 135000.0,
                    monthly_payment: 780.0,
                    interest_rate: 1.6,
                    term_years: 20,
                    start_date: '2020-01-15',
                    end_date: '2040-01-15'
                }
            ],
            credit_cards: [
                {
                    card_type: 'Mastercard Platinum',
                    credit_limit: 7000.0,
                    current_balance: 2600.0,
                    last_payment_date: '2025-03-28',
                    minimum_due: 130.0,
                    due_date: '2025-04-15'
                }
            ],
            income: {
                source: 'Freelance Graphic Designer',
                monthly_salary: 2500.0,
                bonus: 0.0,
                last_bonus_date: '',
                salary_payment_day: 28
            },
            expenses: {
                fixed_monthly: [
                    {description: 'Studio Rent', amount: 850.0},
                    {description: 'Internet & Utilities', amount: 210.0},
                    {description: 'Health Insurance', amount: 160.0}
                ],
                variable_monthly: [
                    {description: 'Food Delivery', average: 280.0},
                    {description: 'Co-working Space', average: 180.0},
                    {description: 'Transport', average: 95.0}
                ]
            },
            financial_goals: [
                {
                    goal: 'Europe Backpacking Trip',
                    target_amount: 10000.0,
                    saved_amount: 4300.0,
                    deadline: '2026-06-01'
                }
            ],
            credit_score: {
                score: 684,
                rating: 'Fair',
                last_checked: '2025-03-15'
            }
        },
        hobbies: ['Sketching', 'Hiking', 'Coffee Tasting'],
        avoidTopics: ['Late Payments', 'Debt Collection'],
        behavior: {
            appLogins: 12,
            transactions: 34,
            engagement: 48
        },
        suggestions: ['Recommend budgeting tool', 'Offer flexible savings account'],
        interactions: [
            {date: '2025-02-10', note: 'Asked about credit card limit increase'},
            {date: '2025-01-25', note: 'Requested loan payoff simulation'}
        ],
        upcomingTopics: ['Adjust savings goals', 'Explore retirement planning'],
        summary:
            'Ben is a creative professional who values flexibility and freedom. Financially stable with moderate engagement, he appreciates digital tools that simplify money management.'
    }
] as Customer[]