# views.py
from rest_framework import generics, views, status
from rest_framework.response import Response
from .models import Expense, Passbook
from .serializers import ExpenseSerializer, ExactDataSplitSerializer, PercentageDictSerializer, PassbookSerializer
from django.contrib.auth.models import User
from .utility import get_simplified_data
from .tasks import send_expense_notification

class ExpenseCreateView(views.APIView):
    """
        Allowed HTTP Method:
            - POST
    """
    def post(self, request, *args, **kwargs):
        """
            Parameter : request, args(tuple), kwargs(dict)

            request_data : {
                'expense' : {},
                'user_ids' : [],
                'percentage_user_split' : {},
                'exact_data_split' : {}
            }
        """
        request_data = request.data.get('expense')
        serializer = ExpenseSerializer(request_data)

        expense_data = serializer.validated_data
        split_type = expense_data.get('split_type',None)

        group_users = request.data.get('user_ids',[])
        expense_amount = expense_data.get('total_amount_spend')

        if len(group_users) > 1000:
            return Response({"Error":"Group Cannot have more than 1000 User"},status=status.HTTP_400_BAD_REQUEST)
        
        if expense_amount > 10000000:
            return Response({"Error":"Expense cannot be more than 1cr"},status=status.HTTP_400_BAD_REQUEST)
        
        if split_type == 'Equal':
            splitted_amount = round(expense_amount/group_users.count(), 2)
            for user in group_users:
                passbook_entry = Passbook(
                    user=user,
                    splitted_amount = splitted_amount,
                    payer_id = self.request.user
                )
                passbook_entry.save()
                send_expense_notification.delay(passbook_entry) #adding to celery Queue
            
        elif split_type == 'Percent':

            percentage_dict_serializer = PercentageDictSerializer(
                self.request.data.get('percentage_user_split'),
                many=True
                )

            if not percentage_dict_serializer.is_valid():
                errors = {
                'percentage_dict_errors': percentage_dict_serializer.errors
            }
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                #percentage_dict : [{'user_id':id,'percentage':10},.....]
                calculate_percentage = [p_dict_data.get('percentage',0) for p_dict_data in percentage_dict_serializer.data]

                if sum(calculate_percentage) > 100:
                    return Response({"error":"Invalid Percentage Provided, Must not be greater than 100"},status=status.HTTP_400_BAD_REQUEST)
                elif sum(calculate_percentage) < 0:
                    return Response({"error":"Invalid Percentage Provided, Must not be greater than 0"},status=status.HTTP_400_BAD_REQUEST)
                
                for data in percentage_dict_serializer.data:
                    passbook_entry = Passbook(
                        user = User.objects.get(pk=data.get('user_id')),
                        expense_amount = expense_amount * float(data.get('percentage')),
                        payer_id = self.request.user
                    )
                    passbook_entry.save()
                    send_expense_notification.delay(passbook_entry)

        elif split_type == 'Exact':
            # excat_data_split = [{'user_id':id, amount:10},.....]

            exact_data_split_serializer = ExactDataSplitSerializer(data=self.request.data.get('excat_data_split'), many=True)

            if exact_data_split_serializer.is_valid(raise_exception=True):
                for data in exact_data_split_serializer.data:
                    passbook_entry = Passbook(
                        user = User.objects.get(pk=data.get('user_id')),
                        expense_amount = data.get('amount'),
                        payer_id = self.request.user
                    )
                    passbook_entry.save()
                    send_expense_notification.delay(passbook_entry)
            else:
                errors = {
                'excat_data_split_errors': exact_data_split_serializer.errors,
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Invalid split_type'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Added to the expense model
        serializer.save()
        return Response({"message":"Expense Recorded"},status=status.HTTP_201_CREATED)

class PassbookListView(views.APIView):
    """
        Allowed HTTP Method:
            - GET
    """
    def get(self, request, *args, **kwargs):
        '''
            Flag : simplify , if true returns a simplified data for user Expenses
        '''
        simplify = request.query_params.get('simplify',False)
        passbook_data = PassbookSerializer(Passbook.objects.all()).data
        if simplify:
            simplified_data = get_simplified_data(request.user)
            return Response({'data':simplified_data},status=status.HTTP_200_OK)
        return Response({'data':passbook_data},status=status.HTTP_200_OK)
    
class UserPassbookView(views.APIView):
    """
        Allowed HTTP Method:
            - GET
    """
    def get(self, request, *args, **kwargs):
        '''
            This function returns the list of Passbook entries created for the user 
        '''
        user = kwargs.get('user')
        response_data = PassbookSerializer(Passbook.objects.filter(user=user), many=True)
        return Response({'data':response_data.data},status=status.HTTP_200_OK)
    
class ExpenseView(generics.ListAPIView):
    """
        Allowed HTTP Method:
            - GET
        
        Using the built in ListAPIView which provides the functionality
        for GET request
    """
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

class UserExpenseView(views.APIView):
    """
        Allowed HTTP Method:
            - GET
    """
    def get(self, request, *args, **kwargs):
        '''
            This function returns the list of Expenses created by the user
        '''
        user = kwargs.get('user')
        response_data = ExpenseSerializer(Expense.objects.filter(payer=user), many=True).data
        return Response({'data':response_data},status=status.HTTP_200_OK)