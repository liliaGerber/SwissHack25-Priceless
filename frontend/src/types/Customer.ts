export interface Customer {
    name: string
    id: string
    email: string
    phone: string
    address: string
    accountNumber: string
    status: string
    birthdate: string
    lastLogin: string
    avatar: string
    summary: string

    financial_data: {
        accounts: Array<{
            type: 'checking' | 'savings'
            iban: string
            balance: number
            currency: string
            last_updated: string
            monthly_inflow?: number
            monthly_outflow?: number
            interest_rate?: number
            goal?: string
        }>
        investments: Array<
            | {
            type: 'mutual_fund'
            name: string
            value: number
            currency: string
            risk_level: 'low' | 'medium' | 'high'
            performance_ytd: number
        }
            | {
            type: 'stock'
            name: string
            ticker: string
            value: number
            currency: string
            shares: number
            purchase_price: number
            current_price: number
        }
        >
        loans: Array<{
            type: 'mortgage' | 'personal_loan'
            amount: number
            remaining_balance: number
            monthly_payment: number
            interest_rate: number
            term_years: number
            start_date: string
            end_date: string
        }>
        credit_cards: Array<{
            card_type: string
            credit_limit: number
            current_balance: number
            last_payment_date: string
            minimum_due: number
            due_date: string
        }>
        income: {
            source: string
            monthly_salary: number
            bonus: number
            last_bonus_date: string
            salary_payment_day: number
        }
        expenses: {
            fixed_monthly: Array<{
                description: string
                amount: number
            }>
            variable_monthly: Array<{
                description: string
                average: number
            }>
        }
        financial_goals: Array<{
            goal: string
            target_amount: number
            saved_amount: number
            deadline: string
        }>
        credit_score: {
            score: number
            rating: 'Excellent' | 'Good' | 'Fair' | 'Poor' | string
            last_checked: string
        }
    }

    hobbies: string[]
    avoidTopics: string[]
    behavior: {
        appLogins: number
        transactions: number
        engagement: number
    }
    suggestions: string[],
    upcomingTopics: string[],
    interactions: Array<{
        date: string
        note: string
    }>
}
