from rest_framework.routers import DefaultRouter

from apps.finance.views import BudgetViewSet, ExpenseViewSet, GrantViewSet, InvoiceViewSet, PaymentViewSet

router = DefaultRouter()
router.register("budgets", BudgetViewSet, basename="budgets")
router.register("payments", PaymentViewSet, basename="payments")
router.register("invoices", InvoiceViewSet, basename="invoices")
router.register("expenses", ExpenseViewSet, basename="expenses")
router.register("grants", GrantViewSet, basename="grants")
urlpatterns = router.urls
