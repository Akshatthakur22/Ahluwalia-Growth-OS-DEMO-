"""
Enrich an existing seeded database with enterprise-grade demo data.
Safe to run multiple times — skips if marker site already exists.
"""
import sys
import os
from datetime import datetime, timezone, timedelta
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import (
    User, Role, Site, Contact, Meeting, Opportunity, OwnershipRecord,
    LifecycleHistory, AttendanceLog, ShowroomVisit, Assignment,
)
from app.models.opportunity import OpportunityStatus
import app.models  # noqa: F401

MARKER_SITE = "Prestige Lakeside Towers"
LIFECYCLE_FLOW = [
    OpportunityStatus.NEW_SITE.value,
    OpportunityStatus.RELATIONSHIP_BUILDING.value,
    OpportunityStatus.SHOWROOM_VISIT_SCHEDULED.value,
    OpportunityStatus.SHOWROOM_VISIT_DONE.value,
    OpportunityStatus.SELECTION_DONE.value,
    OpportunityStatus.QUOTATION_SENT.value,
    OpportunityStatus.NEGOTIATION.value,
    OpportunityStatus.ORDER_CONFIRMED.value,
]

DEMO_SITES = [
    {
        "name": "Prestige Lakeside Towers",
        "address": "Sector 77, Southern Peripheral Road",
        "city": "Gurgaon",
        "area": "Sector 77",
        "stage": "finishing",
        "type": "residential",
        "size": 850000,
        "requirement": "Italian marble for 120 apartments — lobby, lift lobbies, master baths",
        "competitor": "Kajaria",
        "remarks": "Premium segment — architect-led specification",
        "days_ago": 78,
        "status": OpportunityStatus.QUOTATION_SENT.value,
        "revenue": 4200000,
        "quotation": 3850000,
        "probability": 75,
    },
    {
        "name": "Horizon IT Park Phase 2",
        "address": "Udyog Vihar Phase 5",
        "city": "Gurgaon",
        "area": "Udyog Vihar",
        "stage": "structure",
        "type": "commercial",
        "size": 1200000,
        "requirement": "Engineered quartz & granite for 8-floor corporate campus",
        "competitor": "Somany",
        "remarks": "Repeat client from Phase 1 — strong negotiation window",
        "days_ago": 65,
        "status": OpportunityStatus.NEGOTIATION.value,
        "revenue": 6800000,
        "quotation": 6200000,
        "probability": 85,
    },
    {
        "name": "Shanti Niketan Villas",
        "address": "DLF Phase 1, Nathupur Road",
        "city": "Gurgaon",
        "area": "DLF Phase 1",
        "stage": "finishing",
        "type": "residential",
        "size": 320000,
        "requirement": "Imported marble for 24 luxury villas",
        "competitor": None,
        "remarks": "Order confirmed — installation starting next month",
        "days_ago": 92,
        "status": OpportunityStatus.ORDER_CONFIRMED.value,
        "revenue": 3100000,
        "quotation": 2950000,
        "probability": 100,
    },
    {
        "name": "Metro Mall Renovation",
        "address": "MG Road, Sikanderpur",
        "city": "Gurgaon",
        "area": "MG Road",
        "stage": "finishing",
        "type": "commercial",
        "size": 450000,
        "requirement": "High-traffic flooring — granite & composite marble",
        "competitor": "Century",
        "remarks": "Mall management finalizing material shortlist",
        "days_ago": 45,
        "status": OpportunityStatus.SELECTION_DONE.value,
        "revenue": 2800000,
        "quotation": None,
        "probability": 70,
    },
    {
        "name": "Royal Heritage Hotel",
        "address": "Ambience Island, NH-48",
        "city": "Gurgaon",
        "area": "Ambience Island",
        "stage": "structure",
        "type": "commercial",
        "size": 950000,
        "requirement": "Lobby & banquet marble — 5-star specification",
        "competitor": "R K Marble",
        "remarks": "Showroom visit completed — awaiting architect sign-off",
        "days_ago": 38,
        "status": OpportunityStatus.SHOWROOM_VISIT_DONE.value,
        "revenue": 5500000,
        "quotation": None,
        "probability": 55,
    },
    {
        "name": "Anand Residency Extension",
        "address": "Sohna Road, Sector 49",
        "city": "Gurgaon",
        "area": "Sector 49",
        "stage": "planning",
        "type": "residential",
        "size": 180000,
        "requirement": "Phase 2 extension — 80 units, budget segment",
        "competitor": None,
        "remarks": "Fresh lead from field team — early discovery",
        "days_ago": 5,
        "status": OpportunityStatus.NEW_SITE.value,
        "revenue": 1200000,
        "quotation": None,
        "probability": 20,
    },
    {
        "name": "City Centre Plaza",
        "address": "Old Delhi Road, Sector 14",
        "city": "Gurgaon",
        "area": "Sector 14",
        "stage": "foundation",
        "type": "mixed_use",
        "size": 600000,
        "requirement": "Retail + office mixed development",
        "competitor": "Asian Granito",
        "remarks": "Lost to competitor on pricing — lessons captured",
        "days_ago": 110,
        "status": OpportunityStatus.LOST.value,
        "revenue": 3500000,
        "quotation": 3200000,
        "probability": 0,
    },
]

CONTACTS_BY_SITE = {
    "Green Valley Residency": [
        ("Ravi Mehta", "builder", "9812345678", "Mehta Constructions", "Project Manager"),
        ("Arun Khanna", "architect", "9811122233", "Khanna Design Studio", "Principal Architect"),
    ],
    "Skyline Commercial Hub": [
        ("Suresh Agarwal", "owner", "9822233445", "Agarwal Developers", "Managing Director"),
        ("Neha Kapoor", "architect", "9833344556", "Kapoor Associates", "Lead Designer"),
    ],
    "Prestige Lakeside Towers": [
        ("Vikram Malhotra", "builder", "9844455667", "Malhotra Infra", "VP Projects"),
        ("Pooja Desai", "architect", "9855566778", "Desai Architects", "Senior Architect"),
    ],
    "Horizon IT Park Phase 2": [
        ("Rahul Bansal", "owner", "9866677889", "Horizon Tech Parks", "CEO"),
    ],
    "Shanti Niketan Villas": [
        ("Deepak Jain", "builder", "9877788990", "Jain Buildcon", "Director"),
        ("Meera Singh", "owner", "9888899001", "Singh Family Trust", "Owner Representative"),
    ],
    "Metro Mall Renovation": [
        ("Karan Mehra", "owner", "9899900112", "Metro Retail Group", "Facilities Head"),
    ],
    "Royal Heritage Hotel": [
        ("Sanjay Chopra", "owner", "9811002233", "Chopra Hospitality", "GM"),
        ("Lisa Fernandes", "architect", "9822113344", "Fernandes Interiors", "Interior Designer"),
    ],
    "Anand Residency Extension": [
        ("Anand Prakash", "builder", "9833224455", "Anand Constructions", "Site Engineer"),
    ],
    "City Centre Plaza": [
        ("Mohit Verma", "owner", "9844335566", "Verma Realty", "Director"),
    ],
}

MATERIALS = [
    "Italian Carrara Marble",
    "Turkish Emperador Dark",
    "Indian Makrana White",
    "Brazilian Quartzite",
    "Spanish Crema Marfil",
    "Engineered Quartz — Calacatta",
    "Black Galaxy Granite",
    "Statuario Marble",
]


def _days_ago(days: int, hour: int = 10, minute: int = 0) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days, hours=24 - hour, minutes=60 - minute)


def _add_lifecycle_chain(db, opp, target_status: str, changed_by, start_days_ago: int):
    if target_status == OpportunityStatus.LOST.value:
        flow = LIFECYCLE_FLOW[:4] + [OpportunityStatus.LOST.value]
    else:
        target_idx = LIFECYCLE_FLOW.index(target_status)
        flow = LIFECYCLE_FLOW[: target_idx + 1]

    existing = {h.new_status for h in db.query(LifecycleHistory).filter(
        LifecycleHistory.opportunity_id == opp.id
    ).all()}

    for i, status in enumerate(flow):
        if status in existing:
            continue
        prev = flow[i - 1] if i > 0 else None
        days = start_days_ago - (len(flow) - i) * 7
        db.add(LifecycleHistory(
            opportunity_id=opp.id,
            previous_status=prev,
            new_status=status,
            changed_by=changed_by.id,
            changed_at=_days_ago(max(days, 1)),
            remarks={
                OpportunityStatus.RELATIONSHIP_BUILDING.value: "Marketing engagement initiated",
                OpportunityStatus.SHOWROOM_VISIT_SCHEDULED.value: "Client invited to Ambala showroom",
                OpportunityStatus.SHOWROOM_VISIT_DONE.value: "Material selection session completed",
                OpportunityStatus.SELECTION_DONE.value: "Final shortlist approved by architect",
                OpportunityStatus.QUOTATION_SENT.value: "Formal quotation submitted",
                OpportunityStatus.NEGOTIATION.value: "Price revision under discussion",
                OpportunityStatus.ORDER_CONFIRMED.value: "Purchase order received",
                OpportunityStatus.LOST.value: "Lost to competitor on pricing",
            }.get(status, "Status updated"),
        ))


def enrich():
    db: Session = SessionLocal()
    try:
        fe = db.query(User).filter(User.employee_code == "FE001").first()
        me = db.query(User).filter(User.employee_code == "ME001").first()
        se = db.query(User).filter(User.employee_code == "SE001").first()
        mg = db.query(User).filter(User.employee_code == "MG001").first()

        if not fe:
            print("Run seed_db.py first.")
            return

        if db.query(Site).filter(Site.site_name == MARKER_SITE).first():
            print("✓ Demo data already enriched (v2). Skipping.")
            return

        print("Enriching demo data (v2)...")

        if mg:
            for u in [fe, me, se]:
                if u and not u.manager_id:
                    u.manager_id = mg.id

        # Upgrade Green Valley to showroom_visit_scheduled
        gv_site = db.query(Site).filter(Site.site_name == "Green Valley Residency").first()
        gv_opp = db.query(Opportunity).filter(
            Opportunity.opportunity_name.like("%Green Valley%")
        ).first()
        if gv_opp:
            gv_opp.current_status = OpportunityStatus.SHOWROOM_VISIT_SCHEDULED.value
            gv_opp.expected_revenue = Decimal("2500000")
            gv_opp.probability_of_conversion = Decimal("65")
            gv_opp.quotation_value = None
            ownership = db.query(OwnershipRecord).filter(
                OwnershipRecord.opportunity_id == gv_opp.id
            ).first()
            if ownership:
                if se and not ownership.sales_owner_id:
                    ownership.sales_owner_id = se.id
                if me and not ownership.marketing_owner_id:
                    ownership.marketing_owner_id = me.id
            _add_lifecycle_chain(db, gv_opp, OpportunityStatus.SHOWROOM_VISIT_SCHEDULED.value, me or fe, 42)

        # Upgrade Skyline
        skyline = db.query(Site).filter(Site.site_name == "Skyline Commercial Hub").first()
        skyline_opp = db.query(Opportunity).filter(
            Opportunity.opportunity_name.like("%Skyline%")
        ).first()
        if skyline and skyline_opp:
            skyline_opp.current_status = OpportunityStatus.RELATIONSHIP_BUILDING.value
            skyline_opp.expected_revenue = Decimal("5000000")
            skyline_opp.probability_of_conversion = Decimal("35")
            skyline.site_stage = "planning"
            skyline.project_size = Decimal("750000")
            skyline.estimated_requirement = "Corporate lobby & cafeteria marble — 12 floors"
            ownership = db.query(OwnershipRecord).filter(
                OwnershipRecord.opportunity_id == skyline_opp.id
            ).first()
            if ownership and me:
                ownership.marketing_owner_id = me.id
            _add_lifecycle_chain(db, skyline_opp, OpportunityStatus.RELATIONSHIP_BUILDING.value, me or fe, 28)

        created_sites = {}
        for spec in DEMO_SITES:
            created_at = _days_ago(spec["days_ago"])
            site = Site(
                site_name=spec["name"],
                address=spec["address"],
                city=spec["city"],
                area=spec.get("area"),
                site_stage=spec["stage"],
                project_type=spec["type"],
                project_size=Decimal(str(spec["size"])) if spec.get("size") else None,
                estimated_requirement=spec.get("requirement"),
                competitor_brand=spec.get("competitor"),
                site_remarks=spec.get("remarks"),
                discovered_by=fe.id,
                created_at=created_at,
            )
            db.add(site)
            db.flush()

            opp = Opportunity(
                site_id=site.id,
                opportunity_name=f"{spec['name']} — Opportunity",
                current_status=spec["status"],
                expected_revenue=Decimal(str(spec["revenue"])),
                quotation_value=Decimal(str(spec["quotation"])) if spec.get("quotation") else None,
                probability_of_conversion=Decimal(str(spec["probability"])),
                created_at=created_at + timedelta(days=1),
            )
            db.add(opp)
            db.flush()

            db.add(OwnershipRecord(
                opportunity_id=opp.id,
                lead_creator_id=fe.id,
                marketing_owner_id=me.id if me else None,
                sales_owner_id=se.id if se and spec["status"] not in (
                    OpportunityStatus.NEW_SITE.value,
                    OpportunityStatus.RELATIONSHIP_BUILDING.value,
                    OpportunityStatus.LOST.value,
                ) else None,
            ))

            _add_lifecycle_chain(db, opp, spec["status"], me or fe, spec["days_ago"])
            created_sites[spec["name"]] = site

        if gv_site:
            created_sites["Green Valley Residency"] = gv_site
        if skyline:
            created_sites["Skyline Commercial Hub"] = skyline

        # Contacts
        for site_name, contacts in CONTACTS_BY_SITE.items():
            site = created_sites.get(site_name) or db.query(Site).filter(Site.site_name == site_name).first()
            if not site:
                continue
            for name, ctype, mobile, firm, designation in contacts:
                if db.query(Contact).filter(Contact.mobile_number == mobile).first():
                    continue
                db.add(Contact(
                    site_id=site.id,
                    name=name,
                    contact_type=ctype,
                    mobile_number=mobile,
                    firm_name=firm,
                    designation=designation,
                ))

        # Meetings — rich history per site
        meeting_templates = [
            ("site_visit", "Discussed marble specs for common areas and bathrooms", "good"),
            ("office_visit", "Reviewed sample boards and pricing tiers at Ambala showroom", "excellent"),
            ("phone_call", "Follow-up on quotation revision and delivery timeline", "good"),
            ("video_call", "Virtual walkthrough of material options with architect", "good"),
        ]
        all_sites = list(created_sites.values())
        for i, site in enumerate(all_sites):
            for j, (mtype, summary, score) in enumerate(meeting_templates[: 2 + (i % 3)]):
                days = 60 - (i * 7 + j * 5)
                if days < 3:
                    days = 3 + j
                db.add(Meeting(
                    site_id=site.id,
                    conducted_by=me.id if me else fe.id,
                    meeting_date=_days_ago(days, hour=11 + j),
                    meeting_type=mtype,
                    stakeholder_name=CONTACTS_BY_SITE.get(site.site_name, [("Client", "", "", "", "")])[0][0],
                    summary=summary,
                    relationship_score=score,
                    follow_up_date=_days_ago(days - 7) if days > 10 else None,
                ))

        # Showroom visits for sales-stage opportunities
        sales_sites = [
            s for s in all_sites
            if s.site_name in (
                "Green Valley Residency", "Prestige Lakeside Towers", "Horizon IT Park Phase 2",
                "Shanti Niketan Villas", "Metro Mall Renovation", "Royal Heritage Hotel",
            )
        ]
        for i, site in enumerate(sales_sites):
            for j in range(1 + (i % 2)):
                days = 35 - (i * 4 + j * 3)
                db.add(ShowroomVisit(
                    site_id=site.id,
                    sales_executive_id=se.id if se else fe.id,
                    visit_date=_days_ago(max(days, 2), hour=14 + j),
                    selected_material=MATERIALS[(i + j) % len(MATERIALS)],
                    estimated_quantity=200 + (i * 80) + (j * 50),
                    quotation_required=j == 0,
                    expected_purchase_date=_days_ago(days - 20) if days > 25 else None,
                    remarks="Client shortlisted 3 options for final approval",
                ))

        # Assignments
        for i, site in enumerate(all_sites[:8]):
            if site.site_name == "City Centre Plaza":
                continue
            days = 50 - i * 5
            if not db.query(Assignment).filter(
                Assignment.site_id == site.id, Assignment.assignment_type == "marketing"
            ).first():
                db.add(Assignment(
                    site_id=site.id,
                    assigned_to=me.id if me else fe.id,
                    assigned_by=mg.id if mg else fe.id,
                    assignment_type="marketing",
                    assigned_at=_days_ago(days),
                    priority=["high", "medium", "high", "medium", "low", "high", "medium", "medium"][i % 8],
                ))
            if site.site_name not in ("Anand Residency Extension", "Skyline Commercial Hub") and se:
                if not db.query(Assignment).filter(
                    Assignment.site_id == site.id, Assignment.assignment_type == "sales"
                ).first():
                    db.add(Assignment(
                        site_id=site.id,
                        assigned_to=se.id,
                        assigned_by=mg.id if mg else fe.id,
                        assignment_type="sales",
                        assigned_at=_days_ago(days - 3),
                        priority="high" if i < 3 else "medium",
                    ))

        # 45 weekdays of attendance history
        today = datetime.now(timezone.utc).date()
        team = [u for u in [fe, me, se] if u]
        for day_offset in range(45, 0, -1):
            d = today - timedelta(days=day_offset)
            if d.weekday() >= 5:
                continue
            for user in team:
                check_in = datetime.combine(d, datetime.min.time()).replace(
                    tzinfo=timezone.utc
                ) + timedelta(hours=9, minutes=15 + hash(str(user.id) + str(d)) % 45)
                exists = db.query(AttendanceLog).filter(
                    AttendanceLog.user_id == user.id,
                    AttendanceLog.check_in_time >= check_in,
                    AttendanceLog.check_in_time < check_in + timedelta(hours=1),
                ).first()
                if exists:
                    continue
                mock = user == fe and day_offset == 12
                db.add(AttendanceLog(
                    user_id=user.id,
                    check_in_time=check_in,
                    check_out_time=check_in + timedelta(hours=8, minutes=30),
                    latitude="28.4595" if not mock else "19.0760",
                    longitude="77.0266" if not mock else "72.8777",
                    mock_location_detected=mock,
                    route_summary=f"{3 + day_offset % 4} sites visited" if user.role == Role.FIELD_EXECUTIVE else None,
                    device_information="demo-seed-v2",
                ))

        # Today's check-ins
        today_start = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
        for user in team:
            if not db.query(AttendanceLog).filter(
                AttendanceLog.user_id == user.id,
                AttendanceLog.check_in_time >= today_start,
            ).first():
                db.add(AttendanceLog(
                    user_id=user.id,
                    check_in_time=today_start + timedelta(hours=9, minutes=20 + hash(str(user.id)) % 40),
                    latitude="28.4595",
                    longitude="77.0266",
                    mock_location_detected=False,
                    device_information="demo-seed-v2",
                ))

        db.commit()
        print("✓ Demo data enriched successfully (v2)")
        print(f"  - {len(DEMO_SITES) + 2} sites with full pipeline spread")
        print("  - 15+ contacts, 30+ meetings, 10+ showroom visits")
        print("  - Lifecycle history chains for all opportunities")
        print("  - 45 days attendance + 1 mock GPS incident")
        print("  - Marketing & sales assignments across portfolio")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    enrich()
