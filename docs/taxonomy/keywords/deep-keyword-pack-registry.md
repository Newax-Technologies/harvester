# Harvester Deep Keyword Pack Registry

Status: **Proposed Candidate Dataset**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented or benchmark-approved**

This registry supplies reusable vocabulary packs that deepen all domain profiles without duplicating the same organization, facility, process, event, problem, technology, role, contact, and negative terms across 1,586 files.

Each pack is independently versioned. Assignment to a domain, activity, provider offering, source, language, or geography requires an explicit mapping.

## 1. Organization archetype packs

| Pack | Candidate terms |
| --- | --- |
| `PACK-ORG-MAKER` | manufacturer; manufacturing company; producer; fabricator; assembler; formulator; processor; production company; factory operator; contract manufacturer; original equipment manufacturer; OEM |
| `PACK-ORG-SUPPLIER` | supplier; authorized supplier; approved supplier; vendor; equipment supplier; material supplier; solution supplier; stockist; dealer; channel partner |
| `PACK-ORG-DISTRIBUTOR` | distributor; authorized distributor; national distributor; regional distributor; exclusive distributor; distribution company; master distributor; stockist; dealer network; channel distributor |
| `PACK-ORG-WHOLESALE` | wholesaler; wholesale company; bulk supplier; trade supplier; wholesale distributor; cash-and-carry operator; B2B seller |
| `PACK-ORG-RETAIL` | retailer; retail chain; shop; store; outlet; merchant; showroom; dealer; franchise; branch network; convenience store; speciality retailer |
| `PACK-ORG-ECOMMERCE` | online store; e-commerce retailer; ecommerce seller; marketplace seller; digital merchant; direct-to-consumer brand; D2C brand; online marketplace; commerce platform |
| `PACK-ORG-SERVICE` | service provider; specialist provider; professional firm; operator; contractor; managed service provider; maintenance company; support provider; implementation partner |
| `PACK-ORG-FACILITY` | facility; centre; center; campus; branch; site; unit; complex; depot; hub; terminal; plant; clinic; laboratory; warehouse; workshop |
| `PACK-ORG-INSTITUTION` | institution; institute; academy; university; college; school; hospital; authority; board; council; trust; foundation; association |
| `PACK-ORG-PUBLIC` | ministry; department; authority; commission; regulator; council; board; agency; municipal corporation; public institution; state-owned entity; government office |
| `PACK-ORG-NONPROFIT` | NGO; nonprofit organization; charity; charitable trust; foundation; welfare organization; community organization; development organization; humanitarian organization; civil-society organization |
| `PACK-ORG-PLATFORM` | software vendor; platform provider; technology company; SaaS provider; application provider; cloud provider; marketplace operator; digital platform; solution provider |

## 2. Commercial activity packs

| Pack | Candidate terms |
| --- | --- |
| `PACK-COM-MANUFACTURE` | manufacturing; manufacture; manufactured by; production; produced by; factory; production line; plant; capacity; output; contract manufacturing; private label manufacturing |
| `PACK-COM-PROCESS` | processing; grading; sorting; refining; blending; formulation; finishing; treatment; conversion; milling; extraction; purification; packaging |
| `PACK-COM-IMPORT` | importer; importing; imports; imported products; import licence; customs clearance; overseas sourcing; international procurement |
| `PACK-COM-EXPORT` | exporter; exporting; exports; export house; export markets; international sales; export licence; overseas distribution |
| `PACK-COM-DISTRIBUTE` | distribution; distributing; distributor network; dealer network; channel network; route to market; territory coverage; stockist network; supply network |
| `PACK-COM-WHOLESALE` | wholesale; wholesaling; bulk sales; trade sales; wholesale price; distributor price; dealer price; B2B catalogue |
| `PACK-COM-RETAIL` | retail; retailing; store sales; branch sales; point of sale; counter sales; showroom; outlet; retail network |
| `PACK-COM-SELL` | selling; sales; quotation; catalogue; price list; order booking; order processing; commercial department; business development |
| `PACK-COM-RESELL` | reseller; reselling; authorized reseller; channel partner; value-added reseller; VAR; dealer; franchisee |
| `PACK-COM-MARKET` | marketing; promotion; brand promotion; product launch; trade marketing; advertising; campaign; merchandising; demand generation |
| `PACK-COM-LEASE` | leasing; rental; hire; subscription; equipment lease; operating lease; asset rental; fleet rental |
| `PACK-COM-SCRAP` | scrap dealer; scrap trader; recycler; recycling company; material recovery; waste processor; dismantler; salvage; recovered material; secondary raw material |

## 3. Facility and asset packs

| Pack | Candidate terms |
| --- | --- |
| `PACK-FAC-PLANT` | plant; factory; production facility; manufacturing unit; industrial unit; processing facility; production site; assembly line; workshop |
| `PACK-FAC-WAREHOUSE` | warehouse; warehousing facility; distribution centre; distribution center; fulfilment centre; fulfillment center; depot; stockroom; storage facility; godown; godam |
| `PACK-FAC-COLDCHAIN` | cold store; cold storage; refrigerated warehouse; temperature-controlled facility; cold room; chiller; freezer; reefer; cold-chain hub |
| `PACK-FAC-LAB` | laboratory; lab; testing laboratory; quality-control lab; diagnostic lab; research lab; calibration lab; sample-processing facility |
| `PACK-FAC-CLINICAL` | hospital; clinic; medical centre; medical center; treatment centre; diagnostic centre; pharmacy; blood bank; rehabilitation centre |
| `PACK-FAC-EDUCATION` | campus; school; college; university; academy; training centre; institute; classroom; laboratory; library; examination centre |
| `PACK-FAC-HOSPITALITY` | hotel; resort; guest house; serviced apartment; restaurant; kitchen; banquet hall; venue; conference centre; spa |
| `PACK-FAC-LOGISTICS` | depot; hub; terminal; sorting centre; fulfilment centre; cross-dock; fleet yard; port; airport cargo terminal; container yard |
| `PACK-FAC-ENERGY` | power plant; generation station; substation; grid station; solar farm; wind farm; battery site; fuel depot; water treatment plant; waste facility |
| `PACK-FAC-TECH` | data centre; data center; network operations centre; NOC; security operations centre; SOC; cloud region; server room; telecom exchange |
| `PACK-ASSET-FLEET` | vehicle; truck; van; bus; car; motorcycle; rider fleet; delivery fleet; tanker; trailer; container; rolling stock |
| `PACK-ASSET-EQUIPMENT` | machinery; equipment; device; instrument; production line; machine; sensor; meter; scanner; terminal; handheld device; asset |

## 4. Operational process packs

| Pack | Candidate terms |
| --- | --- |
| `PACK-PROC-PRODUCTION` | production planning; work order; bill of materials; BOM; batch; lot; routing; scheduling; material requirement; downtime; yield; scrap; quality release |
| `PACK-PROC-INVENTORY` | receiving; put-away; bin location; stock count; cycle count; picking; packing; dispatch; replenishment; stock transfer; batch tracking; expiry tracking |
| `PACK-PROC-DISTRIBUTION` | order booking; territory; dealer; route plan; dispatch; delivery; proof of delivery; returns; collection; sales representative; channel management |
| `PACK-PROC-RETAIL` | point of sale; POS; checkout; price; promotion; shelf; replenishment; return; refund; loyalty; branch transfer; omnichannel |
| `PACK-PROC-CLINICAL` | patient registration; appointment; triage; consultation; diagnosis; treatment; procedure; prescription; admission; discharge; referral; billing |
| `PACK-PROC-EDUCATION` | admission; enrolment; enrollment; course registration; attendance; timetable; assessment; examination; grading; result; certificate; fee collection |
| `PACK-PROC-LEGAL` | client intake; conflict check; matter opening; case filing; hearing; deadline; document review; legal research; time entry; billing; settlement |
| `PACK-PROC-FINANCE` | onboarding; KYC; account opening; financing; underwriting; approval; transaction; settlement; reconciliation; reporting; audit; collection |
| `PACK-PROC-HOSPITALITY` | reservation; check-in; check-out; room allocation; housekeeping; guest request; food order; billing; maintenance request; event booking |
| `PACK-PROC-TRAVEL` | enquiry; itinerary; reservation; ticketing; visa support; booking confirmation; voucher; group departure; passenger manifest; refund |
| `PACK-PROC-LOGISTICS` | booking; pickup; sorting; line haul; hub movement; route assignment; delivery attempt; proof of delivery; COD reconciliation; return |
| `PACK-PROC-PUBLIC` | application; registration; verification; approval; licence; permit; inspection; public hearing; service request; grievance; benefit delivery |
| `PACK-PROC-NONPROFIT` | beneficiary registration; needs assessment; programme enrolment; distribution; field visit; donor reporting; grant management; monitoring and evaluation |

## 5. Business event and timing packs

| Pack | Candidate terms |
| --- | --- |
| `PACK-EVT-LAUNCH` | launched; launch; opening; inauguration; commissioned; introduced; new service; new product; new platform; newly registered |
| `PACK-EVT-EXPANSION` | expansion; expanding; new branch; new facility; additional capacity; capacity increase; geographic expansion; nationwide rollout; new campus |
| `PACK-EVT-HIRING` | hiring; vacancy; careers; recruitment; new role; implementation manager; operations manager; systems analyst; transformation lead |
| `PACK-EVT-FUNDING` | funding; investment; grant; budget approved; capital expenditure; financing secured; project allocation; donor award |
| `PACK-EVT-MA` | merger; acquisition; acquired; takeover; ownership change; restructuring; consolidation; spin-off; divestment |
| `PACK-EVT-CONTRACT` | contract awarded; contract signed; renewal; retender; contract expiry; support ending; maintenance agreement; framework agreement |
| `PACK-EVT-COMPLIANCE` | compliance deadline; licence renewal; audit finding; corrective action; certification required; regulatory reporting; inspection due |
| `PACK-EVT-MAINTENANCE` | maintenance due; calibration due; service interval; inspection due; overhaul; replacement cycle; end of support; end of life |
| `PACK-EVT-SEASONAL` | admission season; tax season; audit season; harvest season; Hajj season; holiday demand; annual planning; budget cycle |

## 6. Direct intent and procurement packs

| Pack | Candidate terms |
| --- | --- |
| `PACK-INTENT-VENDOR` | seeking vendor; vendor required; looking for supplier; implementation partner required; service provider required; invite vendors |
| `PACK-INTENT-QUOTE` | request a quote; quotation required; price proposal; commercial proposal; estimate required; submit quotation |
| `PACK-INTENT-DEMO` | request demo; schedule demonstration; proof of concept; POC; product presentation; technical demonstration |
| `PACK-PROCURE-RFP` | RFP; request for proposal; proposal invited; technical proposal; financial proposal; bid document |
| `PACK-PROCURE-RFQ` | RFQ; request for quotation; quotation notice; price bid; comparative statement |
| `PACK-PROCURE-EOI` | EOI; expression of interest; prequalification; registration of firms; empanelment; vendor enlistment |
| `PACK-PROCURE-TENDER` | tender; tender notice; invitation to bid; NIT; bid invitation; procurement notice; bidding document |
| `PACK-PROCURE-AWARD` | award notice; successful bidder; contract awarded; letter of acceptance; purchase order issued |
| `PACK-PROCURE-NEGATIVE` | tender cancelled; bid cancelled; deadline expired; award completed; procurement suspended; corrigendum; amendment |

## 7. Operational problem packs

These packs require an active provider offering and evidence rules.

| Pack | Candidate terms |
| --- | --- |
| `PACK-PAIN-MANUAL` | manual process; paper based; spreadsheet based; manual entry; repetitive entry; manual approval; handwritten record; offline record |
| `PACK-PAIN-DISCONNECTED` | disconnected systems; data silos; separate software; manual transfer; duplicate records; no integration; system does not communicate |
| `PACK-PAIN-VISIBILITY` | no real-time visibility; delayed report; difficult to track; lack of dashboard; incomplete reporting; status unknown; no consolidated view |
| `PACK-PAIN-QUALITY` | frequent error; data error; rework; mismatch; reconciliation issue; inconsistent process; missing record; incorrect stock |
| `PACK-PAIN-DELAY` | delayed approval; slow response; backlog; waiting list; pending cases; late dispatch; processing delay; turnaround time |
| `PACK-PAIN-SCALE` | capacity constraint; growing users; multiple branches; volume increase; overloaded process; expansion difficulty; performance issue |
| `PACK-PAIN-CONTROL` | weak permission; no audit trail; uncontrolled access; unclear responsibility; approval bypass; untracked change; poor accountability |
| `PACK-PAIN-DATA` | duplicate data; export limitation; data portability; vendor lock-in; incomplete history; inconsistent master data; data ownership concern |
| `PACK-PAIN-CUSTOMER` | missed follow-up; slow service; complaint backlog; no self-service; booking difficulty; communication gap; status enquiry |
| `PACK-PAIN-MAINTENANCE` | unplanned downtime; missed maintenance; breakdown; calibration overdue; service backlog; spare-part shortage; asset failure |
| `PACK-PAIN-IOT` | no remote monitoring; manual meter reading; unmonitored equipment; no telemetry; delayed alert; disconnected sensor; no environmental visibility |
| `PACK-PAIN-COMPLIANCE` | audit finding; overdue report; licence risk; missing documentation; traceability gap; nonconformance; corrective action pending |

## 8. Existing-solution and technology packs

| Pack | Candidate terms |
| --- | --- |
| `PACK-TECH-GENERIC` | software; system; platform; application; database; portal; dashboard; mobile app; cloud; on-premises; legacy system |
| `PACK-TECH-ERP` | ERP; enterprise resource planning; finance module; inventory module; procurement module; HR module; production module |
| `PACK-TECH-CRM` | CRM; customer relationship management; lead management; sales pipeline; customer database; sales automation |
| `PACK-TECH-WMS` | WMS; warehouse management system; inventory system; barcode system; bin management; picking system |
| `PACK-TECH-TMS` | TMS; transport management system; fleet management system; route planning; dispatch system; vehicle tracking |
| `PACK-TECH-HEALTH` | EMR; EHR; HIS; hospital management system; clinic management system; LIS; RIS; PACS; pharmacy system; telemedicine |
| `PACK-TECH-EDU` | LMS; SIS; student information system; school management system; campus management; examination system; learning platform |
| `PACK-TECH-RETAIL` | POS; point-of-sale system; retail ERP; e-commerce platform; order management system; loyalty platform; omnichannel system |
| `PACK-TECH-LEGAL` | legal practice management; matter management; case management; document management; legal billing; e-filing; legal research platform |
| `PACK-TECH-FINANCE` | core banking; payment gateway; digital wallet; loan origination; accounting software; treasury system; reconciliation system; AML system |
| `PACK-TECH-HOSPITALITY` | PMS; property management system; channel manager; booking engine; restaurant POS; guest app; housekeeping system |
| `PACK-TECH-MANUFACTURING` | MES; manufacturing execution system; SCADA; PLC; CMMS; quality management system; production planning; industrial IoT |
| `PACK-TECH-CLOUD` | cloud hosting; private cloud; public cloud; data centre; backup; disaster recovery; managed infrastructure; container platform |
| `PACK-TECH-INTEGRATION` | API; integration; middleware; data synchronization; webhook; connector; ETL; EDI; system-to-system; single sign-on |

## 9. Responsible-function packs

| Pack | Candidate roles and functions |
| --- | --- |
| `PACK-ROLE-EXEC` | chief executive; CEO; managing director; director; owner; founder; general manager |
| `PACK-ROLE-OPERATIONS` | chief operating officer; COO; operations director; operations manager; plant manager; branch manager; administrator |
| `PACK-ROLE-IT` | CIO; CTO; IT director; head of IT; IT manager; systems manager; infrastructure manager; applications manager |
| `PACK-ROLE-DIGITAL` | digital transformation head; automation lead; enterprise architect; business systems manager; product owner; programme manager |
| `PACK-ROLE-PROCUREMENT` | procurement director; procurement manager; purchase manager; supply-chain head; sourcing manager; vendor-management officer |
| `PACK-ROLE-FINANCE` | CFO; finance director; finance manager; controller; accounts head; treasury head; internal audit head |
| `PACK-ROLE-SALES` | commercial director; sales head; sales manager; distribution manager; channel manager; business-development manager |
| `PACK-ROLE-WAREHOUSE` | warehouse head; warehouse manager; inventory manager; fulfilment manager; logistics manager; distribution-centre manager |
| `PACK-ROLE-FACILITY` | facility manager; maintenance manager; engineering manager; biomedical engineer; asset manager; energy manager |
| `PACK-ROLE-COMPLIANCE` | compliance head; risk manager; quality manager; regulatory affairs manager; data-protection officer; audit manager |
| `PACK-ROLE-SECTOR` | medical director; registrar; principal; dean; legal operations manager; hotel general manager; fleet manager; programme director |

A role term supports function resolution. It does not prove budget, authority, or consent.

## 10. Contact-route packs

| Pack | Candidate terms |
| --- | --- |
| `PACK-CONTACT-GENERAL` | official contact; contact us; business inquiry; enquiry; corporate office; head office |
| `PACK-CONTACT-PROCUREMENT` | procurement portal; vendor registration; supplier registration; tender contact; bids email; procurement office |
| `PACK-CONTACT-SALES` | sales inquiry; business development; corporate sales; enterprise sales; dealer inquiry; distributor inquiry |
| `PACK-CONTACT-PARTNER` | partner with us; channel partner; technology partner; implementation partner; alliance inquiry |
| `PACK-CONTACT-SUPPORT` | support portal; service desk; helpdesk; maintenance request; technical support |
| `PACK-CONTACT-PUBLIC` | public information officer; citizen service; official helpline; department contact; public grievance |

## 11. Negative and contradiction packs

| Pack | Candidate terms |
| --- | --- |
| `PACK-NEG-EDUCATIONAL` | definition; meaning; course; syllabus; training material; research paper; student assignment; template; sample document |
| `PACK-NEG-JOBS` | jobs only; vacancy only; career advice; salary; interview questions; CV; resume; job seeker |
| `PACK-NEG-CONSUMER` | personal use; home remedy; individual patient; personal loan; consumer complaint; retail product review where B2B is required |
| `PACK-NEG-CLOSED` | permanently closed; dissolved; struck off; inactive; ceased operations; licence revoked; suspended |
| `PACK-NEG-PROCUREMENT` | tender cancelled; tender awarded; bid closed; deadline passed; procurement suspended; project completed |
| `PACK-NEG-ROLE` | former employee; retired; left company; no longer affiliated; obituary; historical role |
| `PACK-NEG-DUPLICATE` | mirrored page; syndicated copy; scraper directory; cached duplicate; press-release copy |
| `PACK-NEG-HOMONYM` | river bank; blood bank; botanical plant; school of thought; legal case versus product case; cloud weather |
| `PACK-NEG-CONTACT` | do not contact; unsubscribe; suppression; legal restriction; platform restriction; conflict of interest |

## 12. Mapping rule

A domain profile gains depth by mapping to relevant packs:

```text
Domain identity profile
+ one or more organization packs
+ approved activity packs
+ facility and process packs
+ optional regulatory and technology packs
+ offering-specific event, pain and intent packs
+ role and contact packs after eligibility gates
+ negative and contradiction packs
+ source and locale policy
```

No pack applies globally merely because it exists.

## 13. Delivery boundary

These are candidate vocabulary packs. They require profile assignments, lexical review, source review, benchmarks, and controlled activation before runtime use.
