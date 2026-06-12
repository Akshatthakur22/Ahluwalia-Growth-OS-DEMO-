from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, case, text
from app.models.opportunity import Opportunity, OpportunityStatus
from app.models.user import User, Role
from app.repositories.opportunity import OpportunityRepository

ALL_STATUSES = [s.value for s in OpportunityStatus]
LOST = OpportunityStatus.LOST.value
CONFIRMED = OpportunityStatus.ORDER_CONFIRMED.value
QUOTATION_STATES = (
    OpportunityStatus.QUOTATION_SENT.value,
    OpportunityStatus.NEGOTIATION.value,
)

# Ops snapshot + pipeline status counts in one Neon round-trip
EXEC_SNAPSHOT_SQL = text("""
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
  (SELECT COUNT(*) FROM assignments) AS active_assignments,
  (SELECT COALESCE(json_object_agg(current_status, cnt), '{}'::json) FROM (
    SELECT current_status, COUNT(*)::int AS cnt FROM opportunities GROUP BY current_status
  ) p) AS pipeline_json
""")

FIELD_DASH_SQL = text("""
SELECT
  (SELECT COUNT(*)::int FROM sites WHERE discovered_by = :uid) AS my_sites,
  (SELECT COUNT(*)::int FROM sites WHERE discovered_by = :uid AND created_at >= :month_start) AS month_sites,
  (SELECT COUNT(*)::int FROM attendance_logs WHERE user_id = :uid AND check_in_time >= :month_start) AS check_ins,
  (SELECT EXISTS(
    SELECT 1 FROM attendance_logs WHERE user_id = :uid AND check_in_time >= :today_start
  )) AS checked_today,
  (SELECT COUNT(*)::int FROM sites) AS total_sites
""")

MARKETING_DASH_SQL = text("""
SELECT
  (SELECT COUNT(*)::int FROM assignments WHERE assigned_to = :uid) AS my_assignments,
  (SELECT COUNT(*)::int FROM meetings WHERE conducted_by = :uid) AS my_meetings,
  (SELECT COUNT(*)::int FROM meetings WHERE conducted_by = :uid AND meeting_date >= :month_start) AS month_meetings,
  (SELECT COUNT(*)::int FROM ownership_records WHERE marketing_owner_id = :uid) AS owned,
  (SELECT COUNT(*)::int FROM opportunities WHERE current_status IN ('relationship_building', 'showroom_visit_scheduled')) AS marketing_stages
""")

SALES_DASH_SQL = text("""
SELECT
  (SELECT COUNT(*)::int FROM showroom_visits WHERE sales_executive_id = :uid) AS visits,
  (SELECT COUNT(*)::int FROM showroom_visits WHERE sales_executive_id = :uid AND visit_date >= :month_start) AS month_visits,
  (SELECT COUNT(*)::int FROM ownership_records WHERE sales_owner_id = :uid) AS owned,
  (SELECT COUNT(*)::int FROM opportunities WHERE current_status IN (
    'showroom_visit_done', 'selection_done', 'quotation_sent', 'negotiation'
  )) AS in_sales,
  (SELECT COUNT(*)::int FROM opportunities WHERE current_status = 'quotation_sent') AS quotations,
  (SELECT COALESCE(SUM(expected_revenue), 0) FROM opportunities WHERE current_status IN (
    'showroom_visit_done', 'selection_done', 'quotation_sent', 'negotiation', 'order_confirmed'
  )) AS sales_revenue,
  (SELECT COALESCE(json_object_agg(current_status, cnt), '{}'::json) FROM (
    SELECT current_status, COUNT(*)::int AS cnt FROM opportunities GROUP BY current_status
  ) p) AS pipeline_json
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

    def _pipeline_from_json(self, raw) -> dict:
        if not raw:
            return self._zero_fill_pipeline({})
        if isinstance(raw, dict):
            return self._zero_fill_pipeline({k: int(v) for k, v in raw.items()})
        return self._zero_fill_pipeline({})

    def _exec_snapshot(self, db: Session) -> tuple[dict, dict]:
        today_start, month_start, now = self._time_bounds()
        row = db.execute(
            EXEC_SNAPSHOT_SQL,
            {"today_start": today_start, "month_start": month_start, "now": now},
        ).mappings().one()
        data = dict(row)
        pipeline = self._pipeline_from_json(data.pop("pipeline_json", None))
        return data, pipeline

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
        snap, pipeline = self._exec_snapshot(db)
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
        snap, pipeline = self._exec_snapshot(db)

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
        params = {"uid": user.id, "today_start": today_start, "month_start": month_start}

        if user.role == Role.FIELD_EXECUTIVE:
            row = db.execute(FIELD_DASH_SQL, params).mappings().one()
            return {
                "role": user.role.value,
                "cards": [
                    {"label": "Sites Discovered", "value": str(row["my_sites"]), "subtitle": f"{row['month_sites']} this month", "accent": "green"},
                    {"label": "Check-ins", "value": str(row["check_ins"]), "subtitle": "This month", "accent": "blue"},
                    {"label": "Today", "value": "Checked In" if row["checked_today"] else "Not Yet", "subtitle": "Attendance status", "accent": "purple" if row["checked_today"] else "gray"},
                    {"label": "Active Sites", "value": str(row["total_sites"]), "subtitle": "Team portfolio", "accent": "orange"},
                ],
            }

        if user.role == Role.MARKETING_EXECUTIVE:
            row = db.execute(MARKETING_DASH_SQL, params).mappings().one()
            return {
                "role": user.role.value,
                "cards": [
                    {"label": "My Assignments", "value": str(row["my_assignments"]), "subtitle": "Active sites", "accent": "purple"},
                    {"label": "Meetings Held", "value": str(row["my_meetings"]), "subtitle": f"{row['month_meetings']} this month", "accent": "blue"},
                    {"label": "My Pipeline", "value": str(row["owned"]), "subtitle": "Owned opportunities", "accent": "green"},
                    {"label": "In Marketing", "value": str(row["marketing_stages"]), "subtitle": "Early-stage deals", "accent": "orange"},
                ],
            }

        if user.role == Role.SALES_EXECUTIVE:
            row = db.execute(SALES_DASH_SQL, params).mappings().one()
            pipeline = self._pipeline_from_json(row["pipeline_json"])
            sales_revenue = float(row["sales_revenue"] or 0)
            return {
                "role": user.role.value,
                "cards": [
                    {"label": "Showroom Visits", "value": str(row["visits"]), "subtitle": f"{row['month_visits']} this month", "accent": "orange"},
                    {"label": "My Accounts", "value": str(row["owned"]), "subtitle": "Sales-owned deals", "accent": "blue"},
                    {"label": "In Sales Stage", "value": str(row["in_sales"]), "subtitle": "Active negotiations", "accent": "purple"},
                    {"label": "Quotations Out", "value": str(row["quotations"]), "subtitle": f"₹{sales_revenue/100000:.1f}L pipeline", "accent": "green"},
                ],
                "pipeline_summary": pipeline,
            }

        return {"role": user.role.value, "cards": []}
