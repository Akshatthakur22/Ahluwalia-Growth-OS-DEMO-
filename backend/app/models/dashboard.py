from sqlalchemy import Column, Numeric, DateTime
from app.models.base import BaseModel


class DashboardSnapshot(BaseModel):
    """
    Dashboard snapshot model for reporting optimization.
    """
    __tablename__ = "dashboard_snapshots"
    
    snapshot_date = Column(DateTime(timezone=True), nullable=False, index=True)
    attendance_count = Column(Numeric(10, 0), nullable=True)
    active_opportunities = Column(Numeric(10, 0), nullable=True)
    confirmed_orders = Column(Numeric(10, 0), nullable=True)
    revenue_pipeline = Column(Numeric(15, 2), nullable=True)
