# Harvester Sector Lead-Generation Overlays

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

These overlays strengthen discovery for the 16 broad sectors without copying provider-specific service logic into the canonical domain registry.

Each overlay identifies high-value trigger families, operational indicators, scale cues, likely responsible functions, preferred source classes, and important exclusions. Actual opportunity logic still requires an active provider offering and an approved domain–activity combination.

## `BS-001 Healthcare`

- **High-value triggers:** facility expansion; new clinic or service line; hospital procurement; accreditation or compliance deadline; equipment installation or replacement; digital-health implementation; workforce expansion; direct patient or professional inquiry where permitted.
- **Operational indicators:** manual patient records; appointment backlog; disconnected clinical and billing systems; laboratory or imaging integration issues; inventory and expiry problems; equipment downtime; cold-chain requirements; poor branch visibility.
- **Scale cues:** bed count; number of sites; specialist departments; laboratory volume; pharmacy network; diagnostic branches; ambulance fleet.
- **Likely functions:** hospital administration; medical director; IT; biomedical engineering; operations; procurement; finance; quality and compliance.
- **Preferred sources:** official facility websites; health registries; procurement portals; authorized directories; job boards; accreditation notices; company announcements.
- **Critical exclusions:** never infer a diagnosis or patient need from unrelated personal activity; healthcare privacy and referral rules override commercial relevance.

## `BS-002 Education`

- **High-value triggers:** new campus or program; admissions cycle; accreditation; LMS or student-system procurement; examination modernization; digital-learning launch; faculty and administrative hiring.
- **Operational indicators:** manual admissions; fragmented student records; spreadsheet attendance; fee reconciliation delays; disconnected LMS and administration; examination backlog; weak parent or student communication.
- **Scale cues:** student count; campuses; faculties; programs; branch network; online learner volume.
- **Likely functions:** rector or vice chancellor; principal; registrar; IT; academics; admissions; examinations; finance; procurement.
- **Preferred sources:** institution websites; education registries; accreditation bodies; tender portals; admissions pages; job boards; news announcements.
- **Critical exclusions:** separate educational institutions from “school of thought,” informal content creators, and unrelated course mentions.

## `BS-003 Food and Agriculture`

- **High-value triggers:** crop season; new processing line; export certification; cold-chain expansion; packaging procurement; traceability requirement; new farm, dairy, livestock, or processing facility.
- **Operational indicators:** manual farm records; yield uncertainty; fragmented supplier data; temperature excursions; stock spoilage; batch and traceability gaps; distributor coordination problems.
- **Scale cues:** acreage; herd size; production capacity; processing volume; warehouses; export markets; collection centres.
- **Likely functions:** owner; farm manager; operations; production; quality; procurement; supply chain; cold-chain manager; finance.
- **Preferred sources:** agriculture registries; processor websites; export and certification records; procurement notices; job boards; trade associations; news.
- **Critical exclusions:** distinguish industrial “plant” from botanical plant and food product mentions from actual operating businesses.

## `BS-004 Real Estate`

- **High-value triggers:** new development; project launch; property acquisition; portfolio expansion; facility-management contract; leasing campaign; smart-building or tenant-system requirement.
- **Operational indicators:** disconnected leads and property inventory; booking confusion; manual installment tracking; document-version risk; delayed maintenance; weak tenant communication; poor portfolio visibility.
- **Scale cues:** units; developments; buildings; managed properties; cities; agents; tenant count.
- **Likely functions:** developer or owner; chief operating officer; sales; property management; facilities; finance; IT; procurement.
- **Preferred sources:** developer websites; land and company registries; project announcements; property portals; tenders; careers pages; maps.
- **Critical exclusions:** distinguish property assets from financial or IT assets and avoid treating portal listings as proof of ownership.

## `BS-005 Construction`

- **High-value triggers:** tender award; new project; contractor prequalification; site mobilization; material procurement; equipment deployment; compliance or inspection requirement.
- **Operational indicators:** manual site reporting; drawing and document confusion; delayed approvals; weak subcontractor visibility; material tracking gaps; equipment downtime; safety-reporting burden.
- **Scale cues:** contract value; active sites; workforce; equipment fleet; project duration; geographic coverage.
- **Likely functions:** managing director; project director; operations; engineering; commercial; procurement; quantity surveying; HSE; finance; IT.
- **Preferred sources:** tender and procurement portals; contractor websites; project announcements; government development plans; job boards; industry directories.
- **Critical exclusions:** distinguish a design concept, supplier product, or completed historical project from an active contractor opportunity.

## `BS-006 Legal`

- **High-value triggers:** firm expansion; new practice area; company formation activity; regulatory deadline; litigation or transaction volume; legal-technology procurement; explicit request for counsel.
- **Operational indicators:** fragmented matter records; deadline risk; document-version problems; manual time billing; weak knowledge retrieval; client-update delays; conflict-check limitations.
- **Scale cues:** partners; practice groups; offices; active matters; corporate client base; jurisdictions.
- **Likely functions:** managing partner; practice head; legal operations; general counsel; company secretary; IT; finance; compliance.
- **Preferred sources:** law-firm websites; bar and company registries; procurement portals; legal directories; public requests; job boards; regulatory notices.
- **Critical exclusions:** never invent misconduct, legal exposure, or case need from weak or sensational sources; conflict and confidentiality controls apply.

## `BS-007 Finance`

- **High-value triggers:** product launch; branch or channel expansion; regulatory reporting change; core-system replacement; payment or fintech partnership; audit finding; Shariah-governance requirement; explicit procurement.
- **Operational indicators:** manual reconciliation; onboarding delays; fragmented customer data; weak audit trail; compliance burden; disconnected channels; legacy systems; reporting delays.
- **Scale cues:** branches; customers; transactions; assets under management; merchant network; agent network; payment volume.
- **Likely functions:** chief executive; operations; CIO/CTO; finance; risk; compliance; Shariah governance; procurement; digital banking.
- **Preferred sources:** regulator publications; official company reports; procurement notices; job boards; product announcements; authorized financial directories.
- **Critical exclusions:** distinguish banking from blood/data/river bank; do not infer financial distress or crime from weak evidence.

## `BS-008 Retail`

- **High-value triggers:** new stores; e-commerce launch; franchise expansion; distribution change; POS or ERP procurement; seasonal campaigns; new product categories.
- **Operational indicators:** stock inaccuracy; branch reporting gaps; disconnected online and physical sales; manual replenishment; returns friction; supplier-data fragmentation; pricing inconsistency.
- **Scale cues:** stores; franchises; SKUs; warehouses; channels; cities; order volume.
- **Likely functions:** owner; retail operations; merchandising; e-commerce; supply chain; IT; finance; procurement; customer experience.
- **Preferred sources:** retailer websites; maps; app stores; marketplaces; job boards; franchise announcements; procurement pages; social channels.
- **Critical exclusions:** a product listing alone does not prove the seller owns inventory, operates stores, or has purchase authority.

## `BS-009 Hospitality`

- **High-value triggers:** hotel opening; renovation; new property; management contract; booking-system replacement; smart-room or energy project; event-season demand.
- **Operational indicators:** disconnected reservations and billing; housekeeping delays; maintenance backlog; manual inventory; weak guest history; energy waste; multi-property reporting gaps.
- **Scale cues:** rooms; properties; restaurants; banquet capacity; locations; staff; annual occupancy.
- **Likely functions:** general manager; operations; rooms division; revenue; IT; facilities; engineering; procurement; finance.
- **Preferred sources:** property websites; booking platforms; tourism registries; job boards; renovation announcements; tenders; maps.
- **Critical exclusions:** separate hospitality operators from travel agencies, property listings, restaurant reviews, and event-only venues.

## `BS-010 Travel`

- **High-value triggers:** seasonal packages; new route or destination; Hajj/Umrah season; booking-platform launch; visa-service expansion; corporate travel contract; explicit traveller inquiry.
- **Operational indicators:** manual booking; fragmented supplier inventory; itinerary errors; payment reconciliation; customer-notification delays; agent-network coordination problems.
- **Scale cues:** destinations; branches; bookings; agents; supplier network; group size; routes.
- **Likely functions:** owner; travel operations; reservations; product contracting; digital commerce; finance; customer service; IT.
- **Preferred sources:** agency websites; tourism and pilgrimage registries; airline and hotel partner pages; social channels; job boards; direct inquiries.
- **Critical exclusions:** separate destination content and travel blogging from licensed or operating travel providers.

## `BS-011 Manufacturing and Industry`

- **High-value triggers:** new plant or line; capacity expansion; automation project; quality certification; equipment procurement; export growth; maintenance shutdown; ERP/MES replacement.
- **Operational indicators:** manual production reporting; downtime; weak traceability; disconnected machines and ERP; inventory mismatch; quality rework; maintenance backlog; energy inefficiency.
- **Scale cues:** plants; lines; production capacity; shifts; workforce; export markets; machine count.
- **Likely functions:** plant manager; operations; production; engineering; maintenance; quality; supply chain; IT/OT; procurement; finance.
- **Preferred sources:** manufacturer websites; industrial registries; procurement portals; certification databases; job boards; export records; trade media.
- **Critical exclusions:** distinguish actual manufacturers from distributors, resellers, product brands, and articles discussing manufacturing.

## `BS-012 Logistics`

- **High-value triggers:** fleet expansion; new hub; delivery contract; route launch; warehouse opening; WMS/TMS procurement; cold-chain requirement; postal or courier digitization.
- **Operational indicators:** poor shipment visibility; manual dispatch; failed-delivery handling; COD reconciliation; warehouse inaccuracies; route inefficiency; vehicle downtime; disconnected tracking.
- **Scale cues:** vehicles; riders; hubs; warehouses; routes; parcels; shipments; branches.
- **Likely functions:** chief operating officer; logistics; fleet; warehouse; distribution; last-mile; IT; procurement; finance; customer service.
- **Preferred sources:** operator websites; maps; tender portals; job boards; fleet announcements; app stores; tracking pages; trade associations.
- **Critical exclusions:** distinguish network, port, route, and carrier meanings by transport context; copied tracking pages are not independent evidence.

## `BS-013 Energy`

- **High-value triggers:** new generation project; grid or utility modernization; renewable installation; metering program; energy-efficiency project; regulatory requirement; maintenance outage.
- **Operational indicators:** limited asset visibility; manual meter reading; outage response delays; maintenance backlog; energy-loss uncertainty; disconnected field operations; weak forecasting.
- **Scale cues:** generation capacity; sites; meters; customers; substations; field teams; assets.
- **Likely functions:** operations; generation; transmission/distribution; engineering; asset management; field service; IT/OT; procurement; finance; regulatory affairs.
- **Preferred sources:** regulator and utility publications; project announcements; procurement portals; environmental approvals; job boards; company reports.
- **Critical exclusions:** distinguish physical energy systems from financial “energy markets,” academic research, and product-only suppliers.

## `BS-014 Technology`

- **High-value triggers:** product launch; funding; enterprise partnership; new region; hiring surge; platform migration; compliance certification; public request for technical capability.
- **Operational indicators:** scaling limitations; integration backlog; support burden; legacy architecture; security or reliability gaps; fragmented data; manual customer operations.
- **Scale cues:** customers; users; transactions; developers; regions; integrations; infrastructure footprint.
- **Likely functions:** founder; chief executive; CTO/CIO; engineering; product; security; operations; customer success; procurement; finance.
- **Preferred sources:** company websites; product documentation; authorized professional profiles; job boards; app marketplaces; repositories where authorized; funding news.
- **Critical exclusions:** exclude generic “AI-powered,” “cloud,” or “platform” marketing unless supported by defined technical or commercial evidence.

## `BS-015 Government`

- **High-value triggers:** approved program; budget allocation; tender; public-service modernization; new department or facility; regulatory mandate; digitization or smart-city project.
- **Operational indicators:** paper processes; citizen-service delays; fragmented departmental systems; weak records; manual reporting; field-operation visibility gaps; legacy infrastructure.
- **Scale cues:** population served; departments; offices; facilities; program budget; geographic coverage; transaction volume.
- **Likely functions:** secretary; director general; commissioner; program/project director; CIO; procurement; finance; operations; department head.
- **Preferred sources:** official gazettes; procurement portals; government websites; budget documents; project reports; public registries; authorized directories.
- **Critical exclusions:** only official or authorized routes may be used for procurement and contact; political persuasion or sensitive profiling is outside this taxonomy.

## `BS-016 Nonprofit`

- **High-value triggers:** grant award; new program; geographic expansion; donor requirement; monitoring-and-evaluation system; beneficiary-management need; fundraising campaign; partnership request.
- **Operational indicators:** spreadsheet beneficiary records; fragmented program data; weak donor reporting; manual field collection; volunteer coordination problems; limited outcome visibility.
- **Scale cues:** programs; beneficiaries; field offices; countries/districts; grants; donors; staff and volunteers.
- **Likely functions:** executive director; country director; program director; operations; grants; monitoring and evaluation; finance; IT; procurement.
- **Preferred sources:** organization websites; donor and grant portals; charity registries; program reports; procurement pages; job boards; partnership announcements.
- **Critical exclusions:** distinguish registered organizations and active programs from informal fundraising posts; sensitive beneficiary data must not be collected for commercial targeting.

## Universal overlay rules

1. Sector overlays guide retrieval and ranking; they do not replace domain-specific keyword profiles.
2. Provider offerings determine which trigger and pain profiles are commercially relevant.
3. Scale cues support fit and value assessment but do not prove budget or need.
4. Decision-maker cues identify possible responsibility, not consent or purchase authority.
5. Preferred sources do not authorize prohibited collection methods.
6. Sensitive-sector restrictions override lead volume targets.
7. Every signal retains source, event date, extraction date, freshness, match mode, and evidence state.
8. Overlapping sectors must reuse one resolved organization and evidence graph rather than creating duplicate leads.
