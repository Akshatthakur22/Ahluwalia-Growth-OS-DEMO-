from pydantic import BaseModel
from typing import Dict, List, Any, Optional


class RevenueMetrics(BaseModel):
    total_pipeline_value: float
    weighted_pipeline_value: float
    confirmed_revenue: float
    quotations_outstanding: float
    avg_deal_size: float


class TopDealItem(BaseModel):
    id: str
    opportunity_name: str
    current_status: str
    expected_revenue: Optional[float] = None
    probability_of_conversion: Optional[float] = None


class ExecutiveDashboard(BaseModel):
    """CEO — revenue, pipeline, growth, strategic control."""
    revenue: RevenueMetrics
    opportunities: Dict[str, Any]
    pipeline_by_status: Dict[str, int]
    growth: Dict[str, Any]
    team_pulse: Dict[str, Any]
    top_deals: List[TopDealItem]


class ManagerDashboard(BaseModel):
    """Manager — team attendance, assignments, follow-ups, field execution."""
    team: Dict[str, Any]
    operations: Dict[str, Any]
    field_operations: Dict[str, Any]
    pipeline_snapshot: Dict[str, int]


# Legacy alias kept for any internal use
class DashboardMetrics(BaseModel):
    attendance: Dict[str, Any]
    field_operations: Dict[str, Any]
    opportunities: Dict[str, Any]
    revenue: RevenueMetrics
    pipeline_by_status: Dict[str, int]
    operations: Optional[Dict[str, Any]] = None


class RoleDashboardCard(BaseModel):
    label: str
    value: str
    subtitle: str
    accent: str


class RoleDashboard(BaseModel):
    role: str
    cards: List[RoleDashboardCard]
    pipeline_summary: Optional[Dict[str, int]] = None
