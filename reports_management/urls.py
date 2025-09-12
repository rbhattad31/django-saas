# from django.urls import path
# from . import views
# from .views import AgentCommissionReportViewSet

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('agent-commission-report/', views.agent_commission_report, name='agent_commission_report'),
#     path('agent-commission-report/datatable/', AgentCommissionReportViewSet.as_view({'post': 'datatable_filter'}), name='agent_commission_datatable'),
#     path('api/agents/dropdown/', AgentCommissionReportViewSet.as_view({'get': 'agent_dropdown'}), name='agent-dropdown'),
#     path('agent-performance-report/', views.agent_performance_report, name='agent_performance_report'),
#     path('agent-performance-report/datatable/', AgentCommissionReportViewSet.as_view({'post': 'performance_datatable_filter'}), name='agent_performance_datatable'),
# ]
from django.urls import path
from . import views
from .views import AgentCommissionReportViewSet

urlpatterns = [
    path('agent-commission-report/', views.agent_commission_report, name='agent_commission_report'),
    path('agent-commission-report/datatable/', AgentCommissionReportViewSet.as_view({'post': 'datatable_filter'}), name='agent_commission_datatable'),
    path('api/agents/dropdown/', AgentCommissionReportViewSet.as_view({'get': 'agent_dropdown'}), name='agent-dropdown'),
    path('agent-performance-report/', views.agent_performance_report, name='agent_performance_report'),
    path('agent-performance-report/datatable/', AgentCommissionReportViewSet.as_view({'post': 'performance_datatable_filter'}), name='agent_performance_datatable'),
]