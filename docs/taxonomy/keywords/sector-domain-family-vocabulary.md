# Harvester Sector and Domain-Family Vocabulary Registry

Status: **Proposed Candidate Dataset**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented or benchmark-approved**

This registry adds sector and domain-family vocabulary that can enrich the 1,586 separate domain profiles. Family vocabulary is contextual support, not a replacement for the canonical domain phrase.

## `BS-001 Healthcare`

- **Medicines and therapeutics:** pharmaceutical; pharma; medicine; medication; drug product; formulation; dosage form; active ingredient; generic; branded medicine; biologic; biosimilar; vaccine; therapeutic; clinical nutrition; prescription; OTC.
- **Devices and equipment:** medical device; medical equipment; diagnostic equipment; patient monitor; ventilator; imaging; surgical instrument; implant; rehabilitation equipment; assistive device; biomedical equipment.
- **Supplies and consumables:** medical disposable; surgical consumable; wound care; infection control; PPE; sterilization; reagent; test kit; transfusion supply; medical packaging.
- **Clinical facilities and services:** hospital; clinic; primary care; specialist clinic; diagnostic laboratory; imaging centre; pharmacy; dialysis centre; rehabilitation; home healthcare; ambulance.
- **Digital health:** HIS; EMR; EHR; LIS; RIS; PACS; pharmacy system; telemedicine; patient portal; remote patient monitoring; medical billing; clinical decision support.
- **Operations and research:** biomedical maintenance; calibration; medical logistics; cold chain; clinical research; clinical trial; accreditation; public health; screening; vaccination programme.
- **Context controls:** patient or diagnosis terms must not expose or infer personal medical information; `blood bank` must not resolve to financial banking.

## `BS-002 Education`

- **Institutions:** school; college; university; academy; institute; madrasa where selected; training centre; vocational institute; research institute; campus; education group.
- **Learning services:** teaching; instruction; tutoring; coaching; test preparation; professional training; corporate learning; online learning; distance education; special education.
- **Academic operations:** admission; enrolment; registration; course; programme; curriculum; attendance; timetable; assignment; assessment; examination; result; transcript; certificate; degree.
- **Education technology:** LMS; SIS; school management system; campus management; virtual classroom; learning platform; examination platform; student portal; parent portal; library system.
- **Facilities and support:** campus; classroom; laboratory; library; hostel; transport; cafeteria; sports facility; career services; student services.
- **Context controls:** `school` requires education context; student data, protected characteristics, and individual performance must not be inferred from public keywords.

## `BS-003 Food and Agriculture`

- **Crops and farming:** farm; farming; grower; crop; seed; fertilizer; pesticide; irrigation; greenhouse; orchard; plantation; horticulture; grain; fruit; vegetable; commodity.
- **Livestock and aquaculture:** livestock; cattle; poultry; dairy; milk; feed; veterinary; hatchery; fisheries; aquaculture; farm animal; meat production.
- **Food processing:** processing; milling; grinding; baking; beverage; dairy processing; meat processing; edible oil; frozen food; canning; packaging; quality control; food safety.
- **Supply chain:** aggregation; collection centre; mandi; wholesale market; cold storage; reefer; warehouse; distributor; exporter; traceability; grading; sorting.
- **Technology and services:** farm management; agritech; precision agriculture; soil testing; weather monitoring; irrigation automation; livestock monitoring; cold-chain monitoring.
- **Context controls:** botanical `plant` must be distinguished from processing plant; consumer recipes and nutrition advice are not organization evidence.

## `BS-004 Real Estate`

- **Development:** real-estate developer; housing project; commercial project; mixed-use development; plot; apartment; tower; society; scheme; master plan; booking; instalment.
- **Brokerage and sales:** property dealer; real-estate agency; broker; agent; listing; sale; rent; lease; buyer; tenant; lead; viewing; property portal.
- **Property operations:** property management; tenancy; rent collection; maintenance; service charge; facility management; community management; owner association.
- **Assets and facilities:** building; unit; apartment; office; shop; warehouse property; land; estate; mall; community; gated development.
- **Proptech:** property CRM; listing platform; tenant portal; maintenance system; access control; smart building; facility monitoring; visitor management.
- **Context controls:** `scheme`, `asset`, `unit`, and `project` require property context; property advertisement alone does not prove the operator’s internal capability gap.

## `BS-005 Construction`

- **Contracting:** contractor; general contractor; subcontractor; civil works; building contractor; EPC; design-build; project management; construction company.
- **Engineering and design:** architect; structural engineer; civil engineer; MEP; consultant; surveyor; quantity surveyor; geotechnical; BIM; CAD.
- **Materials:** cement; concrete; steel; brick; block; glass; aluminium; timber; tile; sanitary; paint; insulation; roofing; construction chemical.
- **Trades and systems:** electrical; plumbing; HVAC; fire safety; elevator; solar installation; access control; security system; fit-out; interior works.
- **Equipment and site operations:** heavy equipment; crane; excavator; batching plant; scaffolding; site office; labour; material tracking; progress; safety; inspection.
- **Technology:** project management system; BIM coordination; document control; procurement; contractor management; equipment telemetry; site monitoring.
- **Context controls:** physical fire-safety, aluminium, solar, and control systems must not be classified as software merely because they contain `system`.

## `BS-006 Legal`

- **Practice areas:** corporate law; commercial law; litigation; dispute resolution; arbitration; tax law; intellectual property; employment; family law; property law; regulatory; banking law.
- **Legal operations:** client intake; conflict check; matter; case; hearing; deadline; filing; petition; contract; agreement; opinion; due diligence; legal research; document review.
- **Institutions and actors:** law firm; advocate; barrister; legal consultant; chamber; court; tribunal; registrar; arbitrator; mediator; in-house legal department.
- **Legal technology:** matter management; case management; document management; legal billing; e-filing; contract lifecycle; legal research platform; client portal.
- **Compliance services:** company registration; secretarial; licensing; policy; regulatory filing; compliance review; investigation; governance.
- **Context controls:** `case`, `appeal`, `trust`, `filing`, and `security` are highly ambiguous; keywords must not accuse persons or organizations of wrongdoing.

## `BS-007 Finance`

- **Banking and financing:** Islamic banking; retail banking; corporate banking; SME finance; microfinance; trade finance; project finance; Ijarah; leasing; housing finance; supply-chain finance.
- **Payments:** payment gateway; digital wallet; merchant acquiring; POS payment; remittance; transfer; settlement; reconciliation; bill payment; cross-border payment.
- **Investment:** asset management; fund; pension; private equity; venture capital; Sukuk; brokerage; wealth management; portfolio; custody.
- **Takaful:** family Takaful; general Takaful; claims; underwriting; contribution; risk survey; brokerage; distribution.
- **Accounting and tax:** bookkeeping; financial reporting; audit; tax; payroll accounting; AP; AR; treasury; controls; forensic accounting.
- **Risk and compliance:** Shariah governance; AML; KYC; sanctions; credit risk; operational risk; fraud; regulatory reporting; GRC.
- **Financial technology:** core banking; digital banking; loan origination; payment processing; accounting software; treasury system; risk analytics; eKYC; open banking.
- **Context controls:** bank, trust, security, audit, asset, and scheme require finance-specific context; weak evidence must not imply financial distress or misconduct.

## `BS-008 Retail`

- **Store formats:** supermarket; grocery; department store; speciality store; convenience store; showroom; outlet; chain; franchise; kiosk; mall retailer.
- **Product retail:** apparel; footwear; electronics; appliance; furniture; beauty; jewellery; automotive; pharmacy; books; sports; home improvement.
- **Commerce operations:** POS; checkout; pricing; promotion; merchandising; inventory; replenishment; branch transfer; return; refund; loyalty; customer service.
- **E-commerce:** online store; marketplace; seller; product catalogue; cart; checkout; order management; fulfilment; last-mile delivery; click and collect; omnichannel.
- **Supply:** importer; distributor; wholesaler; dealer; supplier; procurement; warehouse; stock; vendor; private label.
- **Context controls:** consumer reviews and personal shopping requests are not B2B organization evidence unless the use case explicitly includes them.

## `BS-009 Hospitality`

- **Accommodation:** hotel; resort; guest house; serviced apartment; hostel; lodge; boutique hotel; property; room; suite; occupancy.
- **Food service:** restaurant; cafe; catering; kitchen; banquet; room service; food and beverage; menu; order; table reservation.
- **Guest operations:** booking; reservation; check-in; check-out; front desk; concierge; housekeeping; guest request; complaint; loyalty; billing.
- **Events and facilities:** banquet hall; wedding venue; conference centre; event venue; spa; gym; pool; maintenance; energy management.
- **Technology:** PMS; booking engine; channel manager; restaurant POS; guest app; housekeeping system; revenue management; online travel agency integration.
- **Context controls:** hospitality property operations remain separate from travel agencies and destination services.

## `BS-010 Travel`

- **Agencies and operators:** travel agency; tour operator; destination management company; DMC; ticketing agent; corporate travel; pilgrimage operator; Hajj; Umrah.
- **Products and services:** flight; hotel booking; package; itinerary; visa support; transfer; excursion; guide; group tour; insurance where permitted; voucher.
- **Operations:** enquiry; reservation; ticketing; booking confirmation; passenger; manifest; departure; cancellation; refund; supplier; allotment.
- **Technology:** booking platform; GDS; reservation system; travel CRM; itinerary builder; supplier integration; payment; customer portal.
- **Context controls:** `agent`, `package`, `tour`, and `booking` require travel context; personal travel posts are not organization evidence.

## `BS-011 Manufacturing and Industry`

- **Production:** manufacturing; factory; industrial plant; production line; assembly; processing; fabrication; machining; moulding; casting; finishing; packaging.
- **Materials and sectors:** food; textile; garment; pharmaceutical; medical device; chemical; plastic; rubber; metal; electrical; electronics; furniture; paper; packaging.
- **Operations:** BOM; work order; production plan; batch; lot; routing; capacity; yield; scrap; downtime; OEE; quality; maintenance; inventory.
- **Industrial technology:** MES; ERP; SCADA; PLC; CMMS; QMS; industrial IoT; machine monitoring; predictive maintenance; energy monitoring.
- **Supply chain:** raw material; supplier; procurement; warehouse; distribution; export; contract manufacturing; OEM; private label.
- **Context controls:** plant must distinguish industrial facility from botanical use; `system` may be physical, embedded, control, or software.

## `BS-012 Logistics`

- **Freight and forwarding:** freight forwarder; cargo; shipment; line haul; trucking; haulage; customs clearance; air freight; sea freight; road freight.
- **Courier and postal:** courier; parcel; postal; express; last mile; rider; pickup; sorting; hub; delivery attempt; proof of delivery; COD.
- **Warehousing:** warehouse; distribution centre; fulfilment; cross-dock; inventory; bin; picking; packing; dispatch; returns; reverse logistics.
- **Cold chain:** refrigerated; reefer; cold store; temperature-controlled; pharmaceutical logistics; food cold chain; temperature excursion.
- **Fleet:** vehicle; driver; route; dispatch; GPS; fuel; maintenance; utilization; geofence; trip; depot.
- **Technology:** WMS; TMS; fleet management; shipment tracking; barcode; QR; handheld; route optimization; customer portal.
- **Context controls:** port may mean shipping port or computing port; `postal` and courier are related but retain distinct operational evidence where relevant.

## `BS-013 Energy`

- **Generation:** power plant; generation; thermal; hydro; nuclear where applicable; captive power; independent power producer; IPP.
- **Renewables:** solar; photovoltaic; PV; wind; biomass; biogas; mini-grid; battery storage; inverter; renewable energy.
- **Grid and utilities:** transmission; distribution; substation; feeder; meter; smart meter; grid; outage; load; demand; billing.
- **Fuels:** oil; gas; LNG; LPG; petroleum; fuel depot; pipeline; refinery; filling station; lubricant.
- **Water and waste:** water utility; treatment plant; pumping; sewerage; wastewater; solid waste; recycling; environmental service.
- **Operations and technology:** SCADA; energy management; telemetry; meter data; asset management; predictive maintenance; remote monitoring; outage management.
- **Context controls:** solar system may be physical infrastructure, not software; `plant` and `grid` require energy or utility context.

## `BS-014 Technology`

- **Software:** software company; product company; SaaS; enterprise software; application; platform; mobile app; web application; vertical software.
- **Cloud and infrastructure:** cloud; hosting; managed infrastructure; data centre; server; container; Kubernetes; backup; disaster recovery; network.
- **Data and AI:** database; analytics; BI; data warehouse; data lake; machine learning; artificial intelligence; AI agent; NLP; computer vision.
- **Cybersecurity:** security operations; SOC; IAM; endpoint security; network security; vulnerability; penetration test; compliance; incident response.
- **Telecommunications:** telecom; ISP; broadband; fibre; wireless; mobile network; tower; connectivity; unified communications.
- **Hardware and embedded:** computer; server; device; electronics; embedded system; IoT device; sensor; gateway; industrial computer.
- **Services:** IT services; managed service provider; MSP; system integrator; implementation; support; consulting; outsourcing; helpdesk.
- **Context controls:** AI, cloud, platform, network, security, and system are broad terms requiring technical and organizational context.

## `BS-015 Government`

- **Institutions:** ministry; department; authority; commission; board; council; agency; municipal corporation; district administration; public institution.
- **Public services:** registration; licence; permit; certificate; tax; utility; land record; citizen service; grievance; benefit; inspection; enforcement.
- **Municipal and infrastructure:** water; sanitation; waste; road; streetlight; public transport; emergency service; facility; asset; works department.
- **Digital government:** e-government; citizen portal; e-office; case management; records management; digital identity; payment; open data; service dashboard.
- **Procurement:** tender; RFP; RFQ; EOI; prequalification; procurement plan; bid; award; framework agreement.
- **Context controls:** public records must be used within legal and purpose limits; political beliefs, affiliations, and protected traits must not be inferred.

## `BS-016 Nonprofit`

- **Organizations:** NGO; nonprofit; charity; foundation; trust; welfare organization; community organization; humanitarian organization; development organization.
- **Programmes:** education; health; livelihood; relief; food distribution; water; shelter; protection; inclusion; climate; community development.
- **Operations:** beneficiary registration; needs assessment; field visit; programme delivery; distribution; volunteer; case management; monitoring and evaluation; M&E.
- **Funding:** donor; grant; proposal; fundraising; donation; zakat; waqf; sponsorship; restricted fund; donor reporting.
- **Governance and accountability:** board; trustee; compliance; safeguarding; audit; impact report; financial report; transparency; data protection.
- **Technology:** donor management; grant management; beneficiary system; field data collection; volunteer management; programme dashboard; mobile data capture.
- **Context controls:** beneficiary, health, disability, poverty, religion, and protection terms require strict privacy and sensitive-data safeguards.

## Mapping rule

A sector-family term can strengthen a canonical domain match only when:

- the selected sector and domain are eligible;
- the term is mapped to the domain family;
- a suitable organization, activity, entity, source, or structured category provides context;
- exclusions and contradictions pass;
- sensitive-sector policy permits the use;
- the originating profile and version are retained.

## Delivery boundary

These are candidate enrichment vocabularies. They do not replace profile-level review, authoritative classifications, locale packs, benchmarks, or provider-offering signals.
