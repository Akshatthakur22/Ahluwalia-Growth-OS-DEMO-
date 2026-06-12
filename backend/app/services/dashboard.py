from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, case, text
from app.models.attendance import AttendanceLog
from app.models.site import Site
from app.models.meeting import Meeting
from app.models.opportunity import Opportunity, OpportunityStatus
from app.models.user import User, EmploymentStatus, Role
from app.models.showroom_visit import ShowroomVisit
from app.models.assignment import Assignment
from app.models.ownership import OwnershipRecord
from app.repositories.opportunity import OpportunityRepository

ALL_STATUSES = [s.value for s in OpportunityStatus]
LOST = OpportunityStatus.LOST.value
CONFIRMED = OpportunityStatus.ORDER_CONFIRMED.value
QUOTATION_STATES = (
    OpportunityStatus.QUOTATION_SENT.value,
    OpportunityStatus.NEGOTIATION.value,
)

# Single round-trip snapshot for ops counts (Neon latency optimization)
OPS_SNAPSHOT_SQL = text("""
SELECT
  (SELECT COUNT(*) FROM users WHERE status::text IN ('active', 'ACTIVE')) AS total_users,
  (SELECT COUNT(DISTINCT user_id) FROM attendance_logs WHERE check_in_time >= :today_start) AS checked_in_today,
  (SELECT COUNT(*) FROM attendance_logs WHERE check_in_time >= :today_start AND mock_location_detected = true) AS mock_gps_today,
  (SELECT COUNT(*) FROM sites) AS total_sites,
  (SELECT COUNT(*) FROM sites WHERE created_at >= :month_start) AS sites_this_month,
  (SELECT COUNT(*) FROM meetings) AS total_meetings,
  (SELECT COUNT(*) FROM opportunities) AS total_opportunities,
  (SELECT COUNT(*) FROM opportunities WHERE follow_up_date IS NOT NULL AND follow_up_date < :now AND current_status != 'lost') AS overdue_opp_followups,
  (SELECT COUNT(*) FROM meetings WHERE follow_up_date IS NOT NULL AND follow_up_date < :now) AS overdue_meeting_followups,
  (SELECT COUNT(*) FROM showroom_visits WHERE visit_date >= :month_start) AS showroom_this_month,
  (SELECT COUNT(*) FROM assignments) AS active_assignments
""")


class DashboardService:
    def __init__(self):
        self.opportunity_repo = OpportunityRepository()

    def _time_bounds(self):
        today = datetime.now(timezone.utc).date()
        today_start = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
        month_start = datetime(today.year, today.month, 1, tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return today_start, month_start, now

    def _zero_fill_pipeline(self, counts: dict) -> dict:
        return {status: counts.get(status, 0) for status in ALL_STATUSES}

    def _ops_snapshot(self, db: Session) -> dict:
        today_start, month_start, now = self._time_bounds()
        row = db.execute(
            OPS_SNAPSHOT_SQL,
            {"today_start": today_start, "month_start": month_start, "now": now},
        ).mappings().one()
        return dict(row)

    def _revenue_metrics(self, db: Session) -> dict:
        active = Opportunity.current_status != LOST
        row = db.query(
            func.coalesce(func.sum(case((active, Opportunity.expected_revenue), else_=0)), 0),
            func.coalesce(func.sum(case((
                active,
                Opportunity.expected_revenue * Opportunity.probability_of_conversion / 100,
            ), else_=0)), 0),
            func.coalesce(func.sum(case((
                Opportunity.current_status == CONFIRMED,
                func.coalesce(Opportunity.quotation_value, Opportunity.expected_revenue),
            ), else_=0)), 0),
            func.coalesce(func.sum(case((
                Opportunity.current_status.in_(QUOTATION_STATES),
                func.coalesce(Opportunity.quotation_value, Opportunity.expected_revenue),
            ), else_=0)), 0),
            func.count(case((active, 1))),
        ).one()

        total, weighted, confirmed, quotations, active_count = (
            float(row[0] or 0), float(row[1] or 0), float(row[2] or 0),
            float(row[3] or 0), int(row[4] or 0),
        )
        return {
            "total_pipeline_value": round(total, 2),
            "weighted_pipeline_value": round(weighted, 2),
            "confirmed_revenue": round(confirmed, 2),
            "quotations_outstanding": round(quotations, 2),
            "avg_deal_size": round(total / active_count, 2) if active_count else 0,
        }

    def get_executive_dashboard(self, db: Session) -> dict:
        snap = self._ops_snapshot(db)
        pipeline = self._zero_fill_pipeline(self.opportunity_repo.count_by_status(db))
        revenue = self._revenue_metrics(db)

        confirmed = pipeline.get("order_confirmed", 0)
        lost = pipeline.get("lost", 0)
        total_opps = int(snap["total_opportunities"] or 0)
        active_pipeline = total_opps - lost
        win_rate = round((confirmed / (confirmed + lost) * 100), 1) if (confirmed + lost) else 0

        top_deals = (
            db.query(Opportunity)
            .filter(Opportunity.current_status != LOST)
            .order_by(Opportunity.expected_revenue.desc().nullslast())
            .limit(5)
            .all()
        )

        total_users = int(snap["total_users"] or 0)
        checked_in = int(snap["checked_in_today"] or 0)

        return {
            "revenue": revenue,
            "opportunities": {
                "total": total_opps,
                "active_pipeline": active_pipeline,
                "confirmed_orders": confirmed,
                "lost": lost,
                "win_rate_percent": win_rate,
                "in_negotiation": pipeline.get("negotiation", 0),
                "quotations_sent": pipeline.get("quotation_sent", 0),
            },
            "pipeline_by_status": pipeline,
            "growth": {
                "sites_this_month": int(snap["sites_this_month"] or 0),
                "total_sites": int(snap["total_sites"] or 0),
                "showroom_visits_this_month": int(snap["showroom_this_month"] or 0),
                "total_meetings": int(snap["total_meetings"] or 0),
            },
            "team_pulse": {
                "attendance_percentage": round((checked_in / total_users * 100) if total_users else 0, 1),
                "checked_in_today": checked_in,
                "total_active_employees": total_users,
            },
            "top_deals": [
                {
                    "id": str(d.id),
                    "opportunity_name": d.opportunity_name,
                    "current_status": d.current_status,
                    "expected_revenue": float(d.expected_revenue) if d.expected_revenue else None,
                    "probability_of_conversion": float(d.probability_of_conversion) if d.probability_of_conversion else None,
                }
                for d in top_deals
            ],
        }

    def get_manager_dashboard(self, db: Session) -> dict:
        snap = self._ops_snapshot(db)
        pipeline = self._zero_fill_pipeline(self.opportunity_repo.count_by_status(db))

        total_users = int(snap["total_users"] or 0)
        checked_in = int(snap["checked_in_today"] or 0)

        pipeline_snapshot = {
            "new_site": pipeline.get("new_site", 0),
            "relationship_building": pipeline.get("relationship_building", 0),
            "showroom_visit_scheduled": pipeline.get("showroom_visit_scheduled", 0),
            "showroom_visit_done": pipeline.get("showroom_visit_done", 0),
            "quotation_sent": pipeline.get("quotation_sent", 0),
            "negotiation": pipeline.get("negotiation", 0),
            "order_confirmed": pipeline.get("order_confirmed", 0),
            "lost": pipeline.get("lost", 0),
        }

        return {
            "team": {
                "total_active_employees": total_users,
                "checked_in_today": checked_in,
                "not_checked_in": max(0, total_users - checked_in),
                "attendance_percentage": round((checked_in / total_users * 100) if total_users else 0, 1),
                "mock_gps_incidents": int(snap["mock_gps_today"] or 0),
            },
            "operations": {
                "overdue_opportunity_followups": int(snap["overdue_opp_followups"] or 0),
                "overdue_meeting_followups": int(snap["overdue_meeting_followups"] or 0),
                "showroom_visits_this_month": int(snap["showroom_this_month"] or 0),
                "active_assignments": int(snap["active_assignments"] or 0),
                "showroom_visits_scheduled": pipeline.get("showroom_visit_scheduled", 0),
            },
            "field_operations": {
                "total_sites": int(snap["total_sites"] or 0),
                "sites_this_month": int(snap["sites_this_month"] or 0),
                "total_meetings": int(snap["total_meetings"] or 0),
            },
            "pipeline_snapshot": pipeline_snapshot,
        }

    def get_role_dashboard(self, db: Session, user: User) -> dict:
        today_start, month_start, _ = self._time_bounds()

        if user.role == Role.FIELD_EXECUTIVE:
            my_sites = db.query(func.count(Site.id)).filter(Site.discovered_by == user.id).scalar() or 0
            month_sites = db.query(func.count(Site.id)).filter(
                Site.discovered_by == user.id, Site.created_at >= month_start
            ).scalar() or 0
            check_ins = db.query(func.count(AttendanceLog.id)).filter(
                AttendanceLog.user_id == user.id,
                AttendanceLog.check_in_time >= month_start,
            ).scalar() or 0
            checked_today = db.query(AttendanceLog.id).filter(
                AttendanceLog.user_id == user.id,
                AttendanceLog.check_in_time >= today_start,
            ).first() is not None
            total_sites = db.query(func.count(Site.id)).scalar() or 0
            return {
                "role": user.role.value,
                "cards": [
                    {"label": "Sites Discovered", "value": str(my_sites), "subtitle": f"{month_sites} this month", "accent": "green"},
                    {"label": "Check-ins", "value": str(check_ins), "subtitle": "This month", "accent": "blue"},
                    {"label": "Today", "value": "Checked In" if checked_today else "Not Yet", "subtitle": "Attendance status", "accent": "purple" if checked_today else "gray"},
                    {"label": "Active Sites", "value": str(total_sites), "subtitle": "Team portfolio", "accent": "orange"},
                ],
            }

        if user.role == Role.MARKETING_EXECUTIVE:
            my_assignments = db.query(func.count(Assignment.id)).filter(Assignment.assigned_to == user.id).scalar() or 0
            my_meetings = db.query(func.count(Meeting.id)).filter(Meeting.conducted_by == user.id).scalar() or 0
            month_meetings = db.query(func.count(Meeting.id)).filter(
                Meeting.conducted_by == user.id, Meeting.meeting_date >= month_start
            ).scalar() or 0
            owned = db.query(func.count(OwnershipRecord.id)).filter(
                OwnershipRecord.marketing_owner_id == user.id
            ).scalar() or 0
            marketing_stages = db.query(func.count(Opportunity.id)).filter(
                Opportunity.current_status.in_([
                    OpportunityStatus.RELATIONSHIP_BUILDING.value,
                    OpportunityStatus.SHOWROOM_VISIT_SCHEDULED.value,
                ])
            ).scalar() or 0
            return {
                "role": user.role.value,
                "cards": [
                    {"label": "My Assignments", "value": str(my_assignments), "subtitle": "Active sites", "accent": "purple"},
                    {"label": "Meetings Held", "value": str(my_meetings), "subtitle": f"{month_meetings} this month", "accent": "blue"},
                    {"label": "My Pipeline", "value": str(owned), "subtitle": "Owned opportunities", "accent": "green"},
                    {"label": "In Marketing", "value": str(marketing_stages), "subtitle": "Early-stage deals", "accent": "orange"},
                ],
            }

        if user.role == Role.SALES_EXECUTIVE:
            sales_stages = [
                OpportunityStatus.SHOWROOM_VISIT_DONE.value,
                OpportunityStatus.SELECTION_DONE.value,
                OpportunityStatus.QUOTATION_SENT.value,
                OpportunityStatus.NEGOTIATION.value,
            ]
            visits = db.query(func.count(ShowroomVisit.id)).filter(
                ShowroomVisit.sales_executive_id == user.id
            ).scalar() or 0
            month_visits = db.query(func.count(ShowroomVisit.id)).filter(
                ShowroomVisit.sales_executive_id == user.id,
                ShowroomVisit.visit_date >= month_start,
            ).scalar() or 0
            owned = db.query(func.count(OwnershipRecord.id)).filter(
                OwnershipRecord.sales_owner_id == user.id
            ).scalar() or 0
            in_sales = db.query(func.count(Opportunity.id)).filter(
                Opportunity.current_status.in_(sales_stages)
            ).scalar() or 0
            quotations = db.query(func.count(Opportunity.id)).filter(
                Opportunity.current_status == OpportunityStatus.QUOTATION_SENT.value
            ).scalar() or 0
            sales_revenue = db.query(func.coalesce(func.sum(Opportunity.expected_revenue), 0)).filter(
                Opportunity.current_status.in_(sales_stages + [CONFIRMED])
            ).scalar()
            return {
                "role": user.role.value,
                "cards": [
                    {"label": "Showroom Visits", "value": str(visits), "subtitle": f"{month_visits} this month", "accent": "orange"},
                    {"label": "My Accounts", "value": str(owned), "subtitle": "Sales-owned deals", "accent": "blue"},
                    {"label": "In Sales Stage", "value": str(in_sales), "subtitle": "Active negotiations", "accent": "purple"},
                    {"label": "Quotations Out", "value": str(quotations), "subtitle": f"₹{float(sales_revenue or 0)/100000:.1f}L pipeline", "accent": "green"},
                ],
                "pipeline_summary": self._zero_fill_pipeline(self.opportunity_repo.count_by_status(db)),
            }

        return {"role": user.role.value, "cards": []}
