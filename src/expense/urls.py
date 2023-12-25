from django.urls import path
from .views import (
    ExpenseCreateView, 
    PassbookListView, 
    UserPassbookView, 
    ExpenseView, 
    UserExpenseView)

urlpatterns = [
    path('create/expense/', ExpenseCreateView.as_view(), name='expense-create'), # url-endpoint to create new expense
    path('passbook/', PassbookListView.as_view(), name='passbook-list'), # url-endpoint to list all passbook entries
    path('passbook/<int:user>/', UserPassbookView.as_view(), name='user-passbook'), # url-endpoint to show user specific passbook entries
    path('expense/',ExpenseView.as_view(), name='expense-list'), # url-endpoint to list all expense entries
    path('expense/<int:user>/',UserExpenseView.as_view(),name='expense-user-view')  # url-endpoint to show user specific expense entries
]