# Harvester Pakistan English, Urdu and Roman Urdu Keyword Pack

Status: **Proposed Candidate Locale Pack**  
Version: **0.1**  
Date: **5 August 2026**  
Implementation status: **Not reviewed for production use**

This pack provides a controlled starting vocabulary for Pakistan-focused discovery. It is not a complete translation of all 1,586 domain profiles. Every term requires lexical, domain, source, and native-language review before activation.

Pakistan business sources frequently mix English, Urdu script, Roman Urdu, abbreviations, and transliterated technical language. The system must support mixed-language evidence without silently replacing the canonical English identity.

## 1. Locale codes

```text
en-PK
ur-PK
ur-Latn-PK
MIXED-en-ur-PK
```

## 2. Organization and commerce cues

| English concept | Urdu candidates | Roman Urdu candidates | Notes |
| --- | --- | --- | --- |
| company | کمپنی | company; kampani | English spelling is common |
| organization | ادارہ; تنظیم | idara; tanzeem | Context-sensitive |
| institution | ادارہ | idara | Broad term; corroboration required |
| manufacturer | صنعت کار; مینوفیکچرر | sanat kar; manufacturer | Technical sources often use English |
| factory | کارخانہ; فیکٹری | karkhana; factory | Distinguish facility from legal entity |
| supplier | سپلائر; فراہم کنندہ | supplier; faraham kuninda | `supplier` is common |
| distributor | تقسیم کار; ڈسٹری بیوٹر | taqseem kar; distributor | |
| wholesaler | تھوک فروش | thok farosh; wholesaler | |
| retailer | خوردہ فروش; ریٹیلر | khurda farosh; retailer | |
| seller | فروخت کنندہ; بیچنے والا | farokht kuninda; bechne wala | Informal variant may be noisy |
| reseller | دوبارہ فروخت کنندہ; ری سیلر | reseller; dobara farokht | |
| dealer | ڈیلر | dealer | Highly ambiguous; domain required |
| stockist | اسٹاکسٹ | stockist | Common in pharmaceutical trade |
| importer | درآمد کنندہ; امپورٹر | daramad kuninda; importer | |
| exporter | برآمد کنندہ; ایکسپورٹر | baramad kuninda; exporter | |
| service provider | خدمات فراہم کرنے والا | service provider; khidmat faraham karne wala | |
| contractor | ٹھیکیدار; کنٹریکٹر | thekedar; contractor | |
| operator | آپریٹر; منتظم | operator; muntazim | Domain context required |
| branch | شاخ; برانچ | shaakh; branch | |
| franchise | فرنچائز | franchise | |
| association | انجمن; ایسوسی ایشن | anjuman; association | |
| chamber | ایوانِ تجارت; چیمبر | aiwan-e-tijarat; chamber | |
| NGO | غیر سرکاری تنظیم; این جی او | NGO; ghair sarkari tanzeem | |
| charity | فلاحی ادارہ; خیراتی ادارہ | falahi idara; khairati idara | |

## 3. Product and operational activities

| English concept | Urdu candidates | Roman Urdu candidates |
| --- | --- | --- |
| manufacturing | تیاری; پیداوار; مینوفیکچرنگ | tayari; paidawar; manufacturing |
| processing | پراسیسنگ; عمل کاری | processing; amal kari |
| assembling | اسمبلنگ; جوڑنا | assembling; jorna |
| packaging | پیکجنگ; پیکنگ | packaging; packing |
| importing | درآمد | daramad; importing |
| exporting | برآمد | baramad; exporting |
| distribution | تقسیم; ڈسٹری بیوشن | taqseem; distribution |
| wholesale | تھوک | thok; wholesale |
| retail | خوردہ; ریٹیل | khurda; retail |
| selling | فروخت | farokht; selling |
| marketing | مارکیٹنگ | marketing |
| promotion | تشہیر; پروموشن | tashheer; promotion |
| warehousing | گودام داری; ویئرہاؤسنگ | godam dari; warehousing |
| warehouse | گودام; ویئرہاؤس | godam; warehouse |
| cold storage | سرد خانہ; کولڈ اسٹوریج | sard khana; cold storage |
| logistics | رسد; لاجسٹکس | rasad; logistics |
| delivery | ترسیل; ڈیلیوری | tarsil; delivery |
| courier | کوریئر | courier |
| maintenance | دیکھ بھال; مینٹیننس | dekh bhal; maintenance |
| repair | مرمت; ریپئر | marammat; repair |
| installation | تنصیب; انسٹالیشن | tanseeb; installation |
| calibration | کیلیبریشن | calibration |
| recycling | دوبارہ قابل استعمال بنانا; ری سائیکلنگ | recycling; dobara istemal |
| scrap | کباڑ; اسکریپ | kabar; scrap |
| procurement | خریداری; پروکیورمنٹ | khareedari; procurement |
| tendering | ٹینڈر; مناقصہ | tender; munakasa |
| quotation | کوٹیشن; نرخ نامہ | quotation; nirkh nama |
| inventory | ذخیرہ; انوینٹری | zakhira; inventory |
| stock | مال کا ذخیرہ; اسٹاک | maal ka zakhira; stock |
| billing | بلنگ | billing |
| payment | ادائیگی; پیمنٹ | adaigi; payment |
| approval | منظوری; اپروول | manzoori; approval |
| reporting | رپورٹنگ; رپورٹ سازی | reporting; report sazi |
| monitoring | نگرانی; مانیٹرنگ | nigrani; monitoring |

## 4. Procurement and intent cues

| English | Urdu candidates | Roman Urdu candidates |
| --- | --- | --- |
| tender notice | ٹینڈر نوٹس; نوٹسِ مناقصہ | tender notice; munakasa notice |
| request for proposal | تجویز طلب; آر ایف پی | tajweez talab; RFP |
| request for quotation | نرخ نامہ طلب; آر ایف کیو | nirkh nama talab; RFQ |
| expression of interest | اظہارِ دلچسپی; ای او آئی | izhar-e-dilchaspi; EOI |
| vendor registration | وینڈر رجسٹریشن; فراہم کنندہ اندراج | vendor registration; supplier indraj |
| supplier required | سپلائر درکار | supplier darkar |
| quotation required | کوٹیشن درکار | quotation darkar |
| bids invited | بولیاں طلب; ٹینڈر مطلوب | boliyan talab; bids invited |
| contract award | معاہدہ ایوارڈ; ٹھیکہ منظور | contract award; theka manzoor |
| tender cancelled | ٹینڈر منسوخ | tender mansookh |
| deadline extended | آخری تاریخ میں توسیع | aakhri tareekh mein tosee |

## 5. Operational problem cues

| English concept | Urdu candidates | Roman Urdu candidates |
| --- | --- | --- |
| manual process | دستی عمل; مینوئل پراسیس | dasti amal; manual process |
| paper records | کاغذی ریکارڈ | kaghzi record |
| spreadsheet based | اسپریڈشیٹ پر مبنی | spreadsheet par mabni |
| duplicate entry | دوہرا اندراج | dohra indraj |
| delayed approval | منظوری میں تاخیر | manzoori mein takheer |
| stock mismatch | اسٹاک میں فرق | stock mein farq |
| reporting delay | رپورٹ میں تاخیر | report mein takheer |
| no real-time visibility | فوری معلومات دستیاب نہیں | real-time maloomat nahi |
| disconnected systems | غیر مربوط نظام | ghair marboot nizam |
| system integration | نظاموں کا انضمام | nizam ka inzimam; system integration |
| data synchronization | ڈیٹا ہم آہنگی | data hum ahangi; synchronization |
| legacy system | پرانا نظام; لیگیسی سسٹم | purana nizam; legacy system |
| software upgrade | سافٹ ویئر اپ گریڈ | software upgrade |
| migration | منتقلی; مائیگریشن | muntaqili; migration |

## 6. Facilities and common sector cues

| Concept | Urdu candidates | Roman Urdu candidates |
| --- | --- | --- |
| hospital | ہسپتال | hospital; haspatal |
| clinic | کلینک | clinic |
| laboratory | تجربہ گاہ; لیبارٹری | tajurba gah; laboratory; lab |
| pharmacy | دواخانہ; فارمیسی | dawa khana; pharmacy |
| school | اسکول; مدرسہ where context permits | school; madrasa |
| college | کالج | college |
| university | جامعہ; یونیورسٹی | jamia; university |
| law firm | قانونی فرم | qanooni firm; law firm |
| court | عدالت | adalat; court |
| bank | بینک | bank |
| hotel | ہوٹل | hotel |
| restaurant | ریسٹورنٹ; طعام گاہ | restaurant; taam gah |
| warehouse | گودام | godam |
| distribution centre | تقسیمی مرکز; ڈسٹری بیوشن سینٹر | taqseemi markaz; distribution center |
| industrial estate | صنعتی علاقہ | sanati ilaqa; industrial estate |
| power plant | بجلی گھر; پاور پلانٹ | bijli ghar; power plant |
| data centre | ڈیٹا سینٹر | data center |
| government department | سرکاری محکمہ | sarkari mehakma |
| municipal service | بلدیاتی خدمت | baldiati khidmat |

## 7. Negative and ambiguity examples

- `bank` must distinguish financial bank, blood bank, river bank, and data bank.
- `plant` must distinguish factory, power plant, water plant, and botanical plant.
- `dealer` requires a selected product or service domain.
- `agent` may mean sales agent, travel agent, software agent, legal agent, or person acting for another.
- `scheme` may describe a housing development, government programme, financial scheme, or fraudulent allegation; context and source are mandatory.
- `case` may be legal matter, medical case, product case, or grammatical example.
- `فارم` may represent `form` or `farm` depending script use and context.
- Roman Urdu spelling is non-standard; variants increase recall but can sharply reduce precision.

## 8. Mixed-language examples

```text
pharma distributor Lahore
ادویات distributor
medical equipment supplier کراچی
school management software درکار
warehouse system quotation required
گودام inventory manual hai
hospital billing system tender
solar panel distributor فیصل آباد
```

Mixed-language text must be preserved. The language detector may assign more than one language or a mixed-language state.

## 9. Review requirements

Before activation:

- review by fluent Urdu and Pakistan business-domain reviewers;
- verify script, transliteration, common usage, and regional variants;
- remove literal translations not used in real commercial language;
- create positive, negative, and ambiguous source examples;
- test mixed English–Urdu and Roman Urdu;
- define match mode and precision tier for every term;
- ensure sensitive-sector terms cannot expose personal or confidential information;
- version every approved locale profile separately from the English canonical profile.

## 10. Delivery boundary

This is a candidate seed pack. It does not claim complete Urdu coverage or production approval.
