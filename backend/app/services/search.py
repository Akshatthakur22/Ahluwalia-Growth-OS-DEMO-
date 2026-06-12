from sqlalchemy.orm import Session
from app.repositories.contact import ContactRepository
from app.repositories.opportunity import OpportunityRepository, OwnershipRepository
from app.models.contact import Contact
from app.models.site import Site
from app.models.meeting import Meeting
from app.models.showroom_visit import ShowroomVisit
from app.models.opportunity import Opportunity
from app.models.ownership import OwnershipRecord
from app.models.user import User


class SearchService:
    def __init__(self):
        self.contact_repo = ContactRepository()
        self.opportunity_repo = OpportunityRepository()
        self.ownership_repo = OwnershipRepository()

    def _ownership_for_opportunities(self, db: Session, opportunities):
        if not opportunities:
            return []
        opp_ids = [o.id for o in opportunities]
        ownerships = (
            db.query(OwnershipRecord)
            .filter(OwnershipRecord.opportunity_id.in_(opp_ids))
            .all()
        )
        ownership_map = {o.opportunity_id: o for o in ownerships}

        user_ids = set()
        for rec in ownerships:
            for field in ("lead_creator_id", "marketing_owner_id", "sales_owner_id"):
                uid = getattr(rec, field, None)
                if uid:
                    user_ids.add(uid)

        users = (
            db.query(User).filter(User.id.in_(user_ids)).all()
            if user_ids else []
        )
        user_map = {u.id: u for u in users}

        result = []
        for opp in opportunities:
            ownership = ownership_map.get(opp.id)
            owners = {}
            if ownership:
                for field in ("lead_creator_id", "marketing_owner_id", "sales_owner_id"):
                    uid = getattr(ownership, field, None)
                    if uid:
                        user = user_map.get(uid)
                        owners[field.replace("_id", "")] = {
                            "id": str(uid),
                            "name": user.full_name if user else None,
                            "role": user.role.value if user else None,
                        }
            result.append({"opportunity": opp, "ownership": owners})
        return result

    def search_by_mobile(self, db: Session, mobile_number: str):
        contacts = self.contact_repo.get_by_mobile(db, mobile_number)
        site_ids = list({c.site_id for c in contacts})
        sites = db.query(Site).filter(Site.id.in_(site_ids)).all() if site_ids else []
        meetings = (
            db.query(Meeting)
            .join(Site)
            .join(Contact, Contact.site_id == Site.id)
            .filter(Contact.mobile_number == mobile_number)
            .all()
            if contacts else []
        )
        showroom_visits = (
            db.query(ShowroomVisit).filter(ShowroomVisit.site_id.in_(site_ids)).all()
            if site_ids else []
        )
        opportunities = (
            db.query(Opportunity).filter(Opportunity.site_id.in_(site_ids)).all()
            if site_ids else []
        )
        return {
            "mobile_number": mobile_number,
            "contacts": contacts,
            "sites": sites,
            "meetings": meetings,
            "showroom_visits": showroom_visits,
            "opportunities": opportunities,
            "opportunity_ownership": self._ownership_for_opportunities(db, opportunities),
        }

    def search_by_name(self, db: Session, name: str):
        contacts = self.contact_repo.search_by_name(db, name)
        site_ids = list({c.site_id for c in contacts})
        opportunities = (
            db.query(Opportunity).filter(Opportunity.site_id.in_(site_ids)).all()
            if site_ids else []
        )
        return {
            "query": name,
            "contacts": contacts,
            "opportunities": opportunities,
            "opportunity_ownership": self._ownership_for_opportunities(db, opportunities),
        }

    def suggest(self, db: Session, query: str, limit: int = 8):
        q = query.strip()
        if len(q) < 2:
            return []
        contacts = (
            db.query(Contact)
            .filter(
                (Contact.name.ilike(f"%{q}%")) | (Contact.mobile_number.ilike(f"{q}%"))
            )
            .limit(limit)
            .all()
        )
        return [
            {
                "type": "contact",
                "label": c.name,
                "sublabel": f"{c.mobile_number} · {c.firm_name or c.contact_type}",
                "mobile": c.mobile_number,
                "contact_id": str(c.id),
            }
            for c in contacts
        ]
