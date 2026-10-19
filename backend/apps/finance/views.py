from apps.common.api import make_serializer, make_viewset
from apps.finance.models import Expense, Grant, Invoice, Payment, StudyBudget

StudyBudgetSerializer = make_serializer(StudyBudget)
PaymentSerializer = make_serializer(Payment)
InvoiceSerializer = make_serializer(Invoice)
ExpenseSerializer = make_serializer(Expense)
GrantSerializer = make_serializer(Grant)

BudgetViewSet = make_viewset(StudyBudget, StudyBudgetSerializer, ["category"], ["study"], "budgets")
PaymentViewSet = make_viewset(Payment, PaymentSerializer, ["title"], ["study", "status", "kind"], "payments")
InvoiceViewSet = make_viewset(Invoice, InvoiceSerializer, ["number"], ["status"], "invoices")
ExpenseViewSet = make_viewset(Expense, ExpenseSerializer, ["category", "vendor"], ["status"], "expenses")
GrantViewSet = make_viewset(Grant, GrantSerializer, ["source", "reference"], ["status"], "grants")
