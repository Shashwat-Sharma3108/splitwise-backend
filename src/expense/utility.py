from collections import defaultdict
from .models import Passbook, Expense

def get_simplified_data(user_id:int) -> dict:
    """
        Parameter : 
            user_id : ID of a user, inside the User model
        
        This function takes in a user_id and then does the following things:
            Fetches all the entries related to the user_id, then calculates
            1. The amount that user have to take from others and stores it
                in : 'user_to_take'  dict
            2. The amount that user have to give to  others and stores it 
                int : 'user_to_give' dict
        
        return : 
        {
            'user_to_take' : {'user1':amount,'user2':amount....},
            'user_to_give' : {'user1':amount,'user2':amount....}

        }
    """
    user_to_take = defaultdict(float) #to get a default value for non-existing key 
    user_to_give = defaultdict(float)

    # calculating where the user have payed for the expense
    amount_to_take = Expense.objects.filter(user=user_id)
    for entry in amount_to_take:
        passbook_entries = Passbook.objects.filter(expense=entry.id)       
        for p_entry in passbook_entries:
            if p_entry.user.id != user_id:
                user_to_take[p_entry.user.username] += p_entry.amount 
    
    # calculating where the user have not payed for the expense
    amount_to_give = Expense.objects.exclude(user=user_id)
    for entry in amount_to_give:
        passbook_entries_of_expense = Passbook.objects.filter(expense=entry.id)
        for p_entry in passbook_entries_of_expense:
            if p_entry.user.id == user_id:
                user_to_give[p_entry.expense.payer.username] += entry.amount if p_entry.user.id == user_id else 0

    # Combine the data into the desired format
    simplified_data = {'money_to_take': [], 'money_to_give': []}

    for debtor_id, amount in user_to_take.items():
        simplified_data['money_to_take'].append({'to': debtor_id, 'amount': amount})

    for payer_id, amount in user_to_give.items():
        simplified_data['money_to_give'].append({'from': payer_id, 'amount': amount})

    return simplified_data