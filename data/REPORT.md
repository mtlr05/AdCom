# FDA AdCom pivotal-vote dataset: final report (scope 2016-11-04 to 2026)

Generated 2026-11-04 12:09 ET. Files are in the data root (this folder). Main table: adcom_full_pivotal.csv / adcom_full.xlsx (156 product-meeting rows). Excluded sheet: excluded.csv (169 rows, each with a reason). Gaps: 0.

## Counts by committee

| committee   |   rows |   press_votes |   outcome_press_or_company |
|:------------|-------:|--------------:|---------------------------:|
| ODAC        |     38 |             2 |                          9 |
| AMDAC       |     16 |             4 |                          3 |
| AADPAC      |     13 |             3 |                          4 |
| PDAC        |     12 |             1 |                          4 |
| EMDAC       |     11 |             2 |                          3 |
| CRDAC       |     10 |             2 |                          5 |
| CTGTAC      |      8 |             0 |                          3 |
| PCNS        |      8 |             0 |                          1 |
| AAC         |      6 |             1 |                          2 |
| PADAC       |      6 |             1 |                          3 |
| GIDAC       |      6 |             0 |                          2 |
| VRBPAC      |      6 |             0 |                          1 |
| DSaRM       |      5 |             0 |                          3 |
| BRUDAC      |      4 |             3 |                          0 |
| DODAC       |      2 |             0 |                          0 |
| MIDAC       |      2 |             0 |                          0 |
| GeMDAC      |      1 |             0 |                          0 |
| NDAC        |      1 |             0 |                          1 |
| PDAC+PCNS   |      1 |             0 |                          0 |

## Verification rate by field

**Vote**: FDA 137 (88%), press 19 (12%)

**Final outcome**: FDA 63 (40%), FDA (openFDA) 49 (31%), press 38 (24%), SEC/company 6 (4%)

**Orphan status for the indication**: N 97 (62%), Y 57 (37%), review 2 (1%)

**Review priority basis**: existing 91 (58%), supplement not matched in openFDA 39 (25%), openFDA ORIG 3 (2%), unverified: CBER BLA/sBLA not in openFDA; no priority source checked 2 (1%), PRIORITY: QIDP priority review, Cempra 10-K https://www.sec.gov/Archives/edgar/data/1461993/000156459017002719/cemp-10k_20161231.htm (SEC; FDA transcript does not restate the designation) 1 (1%), PRIORITY: https://www.novartis.com/news/media-releases/novartis-announces-first-car-t-cell-therapy-bla-pediatric-and-young-adult-patients-rr-b-cell-all-granted-fda-priority-review 1 (1%), PRIORITY: https://www.sec.gov/Archives/edgar/data/1609351/000160935117000074/spark-20178kblaacceptance.htm 1 (1%), openFDA supplement S-9 1 (1%), openFDA supplement S-18 1 (1%), PRIORITY: Daiichi Sankyo press release 21 Nov 2018, FDA accepted the R/R FLT3-ITD AML NDA and granted priority review, PDUFA 25 May 2019 (press). https://www.daiichisankyo.com/media/press_release/detail/index_3224.html 1 (1%), openFDA supplement S-12 1 (1%), PRIORITY: FDA SBRA for BLA 125706, "BLA filed (priority review)" 30 Mar 2020, the submission reviewed on 13 Aug 2020. https://www.fda.gov/media/185192/download 1 (1%), openFDA supplement S-89 1 (1%), STANDARD: https://www.fda.gov/media/170827/download 1 (1%), no openFDA record (BLA at CBER or unapproved) 1 (1%), PRIORITY: https://investor.bluebirdbio.com/news-releases/news-release-details/bluebird-bio-announces-fda-priority-review-biologics-license-0 1 (1%), PRIORITY: https://www.sec.gov/Archives/edgar/data/1293971/000129397121000089/blue-20211122.htm 1 (1%), PRIORITY: Y-mAbs press release 31 May 2022, FDA accepted the omburtamab BLA for priority review, PDUFA 30 Nov 2022 (press). https://ir.ymabs.com/news-releases/news-release-details/y-mabs-announces-fda-acceptance-biologics-license-application 1 (1%), STANDARD: Cytokinetics 4 Feb 2022 acceptance, relayed by Drugs.com: FDA assigned a standard review, PDUFA 30 Nov 2022 (secondary). https://www.drugs.com/history/omecamtiv-mecarbil.html 1 (1%), PRIORITY: https://investorrelations.sarepta.com/news-releases/news-release-details/sarepta-therapeutics-announces-us-fda-has-accepted-filing-and 1 (1%), not found (unverified): no priority designation located; checked FDA briefing https://www.fda.gov/media/172397/download 1 (1%), PRIORITY: Lykos press release 4 Jun 2024: FDA accepted the NDA on 9 Feb 2024 and granted priority review (press). https://www.prnewswire.com/news-releases/lykos-therapeutics-provides-update-on-fda-advisory-committee-meeting-for-investigational-mdma-assisted-therapy-for-ptsd-302163950.html 1 (1%), STANDARD: openFDA drugsfda BLA 761145 supplement 29, review_priority STANDARD, status date 2025-11-06. FDA minutes identify the 20 May 2025 sBLA as 761145/S-029 (https://www.fda.gov/media/187747/download). 1 (1%), unverified for the reviewed submission: PRIORITY applied to original BLA (https://www.capricor.com/investors/news-events/press-releases/detail/305/capricor-therapeutics-announces-fda-acceptance-and-priority); adcom reviewed a Class 2 resubmission (https://www.capricor.com/investors/news-events/press-releases/detail/338/capricor-therapeutics-announces-establishment-of-new-pdufa ; .../detail/354/capricor-therapeutics-announces-extension-of-pdufa-target) 1 (1%), unverified for the reviewed submission: PRIORITY applied to original BLA (https://ir.replimune.com/news-releases/news-release-details/replimune-announces-biologics-license-application-acceptance-and); adcom reviewed a Class 1 resubmission (https://ir.replimune.com/news-releases/news-release-details/replimune-announces-fda-acceptance-rp1-biologics-license) 1 (1%)

Review priority values: {'PRIORITY': 60, 'STANDARD': 51, 'unverified': 45}. Unverified is mostly unapproved products, CBER BLAs and supplements that openFDA does not tag.

1-year outcome: {'unverified': 63, 'approved': 58, 'not approved within 1 yr': 35}. 'unverified' at 1 year means the approval date is known only to the month, or the decision is still pending inside the window.

## 2x2 tables: adcom vote vs FDA outcome (ties and superseded meetings removed; unverified counts shown)

| subset                           | outcome   |   n |   FavApproved |   FavNotApproved |   UnfavApproved |   UnfavNotApproved |   outcome_unverified |
|:---------------------------------|:----------|----:|--------------:|-----------------:|----------------:|-------------------:|---------------------:|
| All                              | final     | 150 |            90 |                6 |              10 |                 43 |                    1 |
| All                              | 1yr       |  89 |            52 |               14 |               5 |                 18 |                   62 |
| Rare (orphan Y)                  | final     |  55 |            40 |                2 |               2 |                 11 |                    1 |
| Rare (orphan Y)                  | 1yr       |  35 |            23 |                6 |               2 |                  4 |                   21 |
| Common (orphan N)                | final     |  93 |            48 |                4 |               8 |                 32 |                    0 |
| Common (orphan N)                | 1yr       |  52 |            28 |                7 |               3 |                 14 |                   41 |
| Priority                         | final     |  59 |            48 |                2 |               2 |                  6 |                    0 |
| Priority                         | 1yr       |  41 |            31 |                6 |               2 |                  2 |                   18 |
| Standard                         | final     |  48 |            34 |                0 |               8 |                  6 |                    0 |
| Standard                         | 1yr       |  36 |            20 |                6 |               3 |                  7 |                   12 |
| CNS (PCNS/PDAC)                  | final     |  20 |            12 |                0 |               1 |                  7 |                    0 |
| CNS (PCNS/PDAC)                  | 1yr       |  14 |            10 |                1 |               1 |                  2 |                    6 |
| CGT (CTGTAC + CAR-T/MSC)         | final     |  11 |            10 |                0 |               0 |                  1 |                    1 |
| CGT (CTGTAC + CAR-T/MSC)         | 1yr       |   5 |             2 |                2 |               0 |                  1 |                    7 |
| Rare + priority                  | final     |  35 |            29 |                1 |               1 |                  4 |                    0 |
| Rare + priority                  | 1yr       |  23 |            18 |                3 |               1 |                  1 |                   12 |
| Approval-only: All               | final     | 116 |            72 |                6 |               8 |                 30 |                    0 |
| Approval-only: All               | 1yr       |  68 |            42 |               11 |               3 |                 12 |                   48 |
| Approval-only: Common            | final     |  75 |            39 |                4 |               7 |                 25 |                    0 |
| Approval-only: Common            | 1yr       |  44 |            25 |                5 |               2 |                 12 |                   31 |
| Approval-only: Rare              | final     |  40 |            32 |                2 |               1 |                  5 |                    0 |
| Approval-only: Rare              | 1yr       |  23 |            17 |                5 |               1 |                  0 |                   17 |
| Approval-only: Rare + priority   | final     |  25 |            22 |                1 |               0 |                  2 |                    0 |
| Approval-only: Rare + priority   | 1yr       |  14 |            12 |                2 |               0 |                  0 |                   11 |
| Approval-only: CGT               | final     |   8 |             8 |                0 |               0 |                  0 |                    0 |
| Approval-only: CGT               | 1yr       |   2 |             1 |                1 |               0 |                  0 |                    6 |
| 2016-11-04..2021 (Daval overlap) | final     |  91 |            55 |                4 |               6 |                 26 |                    0 |
| 2016-11-04..2021 (Daval overlap) | 1yr       |  56 |            33 |               11 |               2 |                 10 |                   35 |

## Corrections 2026-11-04

| meeting_date   | brand                  |    app | old        | new    | basis                                                                                                                                                                                      |
|:---------------|:-----------------------|-------:|:-----------|:-------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2023-05-12     | Elevidys               | 125781 | N          | Y      | corrected 2026-11-04 on audit: OOPD 2013 "Treatment of Duchenne Muscular Dystrophy" (delandistrogene moxeparvovec / Sarepta) matches indication                                            |
| 2018-05-10     | WAYLIVRA               | 210645 | N          | Y      | corrected 2026-11-04 on audit: OOPD volanesorsen "Treatment of familial chylomicronemia syndrome" matches indication                                                                       |
| 2020-07-14     | BLENREP                | 761158 | Y          | Y      | corrected 2026-11-04 on audit: OOPD 2017-06-22 belantamab mafodotin "Treatment of multiple myeloma" (Designated/Approved)                                                                  |
| 2025-07-17     | BLENREP                | 761440 | N          | Y      | corrected 2026-11-04 on audit: OOPD 2017-06-22 belantamab mafodotin "Treatment of multiple myeloma" (Designated/Approved)                                                                  |
| 2019-06-06     |                        | 212862 | N          | Y      | corrected 2026-11-04 on audit: OOPD pretomanid designation for tuberculosis matches BPaL indication (XDR/TI-MDR pulmonary TB)                                                              |
| 2021-05-27     | TZIELD                 | 761183 | N          | Y      | corrected 2026-11-04 on audit: OOPD teplizumab designation for (recent-onset/delay of) type 1 diabetes matches indication                                                                  |
| 2017-05-10     | GLEOLAN                | 208630 | N          | Y      | corrected 2026-11-04 on audit: OOPD aminolevulinic acid designation for visualization of malignant glioma matches Gleolan indication                                                       |
| 2024-09-13     | OCALIVA                | 207999 | N          | Y      | corrected 2026-11-04 on audit: OOPD obeticholic acid designation "Treatment of primary biliary cirrhosis/cholangitis" matches indication                                                   |
| 2023-09-27     | NurOwn                 | 125782 | N          | Y      | corrected 2026-11-04 on audit: OOPD 2011-02-04 "mesenchymal stromal cells secreting neurotrophic factors" (BrainStorm) for ALS                                                             |
| 2017-06-20     | VICTOZA                | 022341 | Y          | N      | corrected 2026-11-04 on audit: keyword match was to anti-IL-21 (NNC0114-0006) T1D designation, a different product; liraglutide has no designation; LEADER CV-risk claim in T2DM is common |
| 2018-01-09     | JATENZO                | 206089 | Y          | N      | corrected 2026-11-04 on audit: testosterone designations are for constitutional delay of puberty / HIV wasting (other indications/products); hypogonadism is common                        |
| 2018-01-10     | TLANDO                 | 208088 | Y          | N      | corrected 2026-11-04 on audit: testosterone designations are for constitutional delay of puberty / HIV wasting (other indications/products); hypogonadism is common                        |
| 2021-07-15     | (roxadustat)           | 213805 | Y          | N      | corrected 2026-11-04 on audit: spurious keyword match; only roxadustat designation is MDS (2025-12-13, after the decision, other indication); CKD anemia is common                         |
| 2024-05-24     | AWIQLI FLEXTOUCH       | 761326 | Y          | N      | corrected 2026-11-04 on audit: match was neonatal-diabetes designation of a different product; no insulin icodec designation; T1D/T2D common                                               |
| 2018-03-07     | BLINCYTO               | 125557 | review     | Y      | corrected 2026-11-04 on audit: OOPD blinatumomab designation for acute lymphoblastic leukemia (2008) covers MRD+ ALL                                                                       |
| 2021-10-07     | LIVTENCITY             | 215596 | review     | Y      | corrected 2026-11-04 on audit: OOPD maribavir designation for clinically significant CMV viremia/disease in at-risk (transplant) patients matches indication                               |
| 2018-07-26     | ARAKODA                | 210607 | review     | N      | corrected 2026-11-04 on audit: only tafenoquine designation is "Treatment of malaria" (GSK, 2013); Arakoda is prophylaxis (prevention) by a different sponsor, not covered                 |
| 2022-09-22     | from Rebiotix Inc.     | 125739 | N          | Y      | corrected 2026-11-04 on audit: OOPD 2014-03-10 "fecal microbiota, live - jslm" (Ferring) for prevention of recurrent CDI, Designated/Approved = Rebyota                                    |
| 2022-10-28     |                        | 761176 | N          | Y      | corrected 2026-11-04 on audit: OOPD 2016-08-29 131-I-8H9 (omburtamab, Y-mAbs) "Treatment of neuroblastoma" covers CNS/leptomeningeal metastases from neuroblastoma                         |
| 2021-09-17     |                        |        | unverified | N      | corrected 2026-11-04 on audit: no OOPD designation for RSV or COVID-19 vaccines (searched rsv/respiratory syncytial/covid/sars-cov/bnt162); common indication                              |
| 2023-02-28     | 769/0)                 | 125769 | unverified | N      | corrected 2026-11-04 on audit: no OOPD designation for RSV or COVID-19 vaccines (searched rsv/respiratory syncytial/covid/sars-cov/bnt162); common indication                              |
| 2023-03-01     | 775/0)                 | 125775 | unverified | N      | corrected 2026-11-04 on audit: no OOPD designation for RSV or COVID-19 vaccines (searched rsv/respiratory syncytial/covid/sars-cov/bnt162); common indication                              |
| 2023-05-18     | 768/0)                 | 125768 | unverified | N      | corrected 2026-11-04 on audit: no OOPD designation for RSV or COVID-19 vaccines (searched rsv/respiratory syncytial/covid/sars-cov/bnt162); common indication                              |
| 2025-05-20     | DARZALEX FASPRO        | 761145 | N          | review | corrected 2026-11-04 on audit: daratumumab designation is "Treatment of multiple myeloma" (2013); high-risk smoldering MM is a precursor state - ambiguous whether covered                 |
| 2026-07-30     | TUDRIQEV               | 125827 | N          | review | corrected 2026-11-04 on audit: no OOPD record found for vusolimogene oderparepvec/RP1/GALV-HSV; advanced melanoma post-PD-1 - left for review                                              |
| 2016-11-04     |                        | 209006 | N          | N      | corrected 2026-11-04 on audit: no OOPD record for solithromycin (searched oopd_all.csv); community-acquired bacterial pneumonia is a common indication                                     |
| 2021-06-24     | retifanlimab injection | 761209 | Y          | Y      | corrected 2026-11-04 on audit: OOPD 2020-03-24 retifanlimab "anal cancer" matches SCAC (earlier basis wrongly cited Merkel cell)                                                           |
| 2018-08-07     | ARIKAYCE KIT           | 207356 | Y          | Y      | corrected 2026-11-04 on audit: OOPD 2013-03-25 liposomal amikacin (Insmed) NTM infections, Designated/Approved                                                                             |
| 2021-04-15     | Lantidra               | 125734 | Y          | Y      | corrected 2026-11-04 on audit: OOPD 2017-02-01 donislecel-jujn (CellTrans) "Treatment of Brittle Type 1 Diabetes", Designated/Approved                                                     |
| 2018-07-12     | KRINTAFEL              | 210795 | Y          | Y      | corrected 2026-11-04 on audit: OOPD 2013-01-15 tafenoquine (GSK) "Treatment of malaria", Designated/Approved                                                                               |

vote_type counts: {'approval/benefit-risk': 120, 'effectiveness-only': 26, 'restriction/other': 10}. center: {'CDER': 138, 'CBER': 18}. CGT rows: 12.

## Still press-only votes (no FDA minutes or transcript found)

| meeting_date   | committee   | brand     | generic                                      |   vote_yes |   vote_no |
|:---------------|:------------|:----------|:---------------------------------------------|-----------:|----------:|
| 2017-11-01     | PDAC        | BRIXADI   | buprenorphine weekly/monthly depot (CAM2038) |         17 |         3 |
| 2018-01-09     | BRUDAC      | JATENZO   | oral testosterone undecanoate                |          9 |        10 |
| 2018-01-10     | BRUDAC      | TLANDO    | oral testosterone undecanoate                |          6 |        13 |
| 2018-05-10     | EMDAC       | WAYLIVRA  | volanesorsen                                 |         12 |         8 |
| 2018-07-25     | PADAC       | NUCALA    | mepolizumab (COPD)                           |          3 |        16 |
| 2019-01-16     | BRUDAC      | EVENITY   | romosozumab                                  |         18 |         1 |
| 2019-06-06     | AMDAC       |           | pretomanid                                   |         14 |         4 |
| 2019-08-07     | AMDAC       | DESCOVY   | emtricitabine/TAF PrEP                       |         16 |         2 |
| 2019-10-16     | AMDAC       | FETROJA   | cefiderocol                                  |         14 |         2 |
| 2020-01-14     | AADPAC      |           | oxycodegol (NKTR-181)                        |          0 |        27 |
| 2020-01-15     | AADPAC      | SEGLENTIS | tramadol/celecoxib                           |         13 |        13 |
| 2020-01-16     | AADPAC      | POSIMIR   | bupivacaine ER solution                      |          6 |         6 |
| 2021-02-09     | ODAC        | KEYTRUDA  | pembrolizumab (early TNBC)                   |         10 |         0 |
| 2021-03-24     | AAC         |           | tanezumab                                    |          1 |        19 |
| 2021-05-27     | EMDAC       | TZIELD    | teplizumab                                   |         10 |         7 |
| 2022-10-26     | CRDAC       | JESDUVROQ | daprodustat                                  |         13 |         3 |
| 2022-10-28     | ODAC        |           | 131I-omburtamab                              |          0 |        16 |
| 2022-12-13     | CRDAC       |           | omecamtiv mecarbil                           |          3 |         8 |
| 2023-04-17     | AMDAC       | XACDURO   | sulbactam-durlobactam                        |         12 |         0 |

Teplizumab: an FDA review (761183Orig1s000OtherR) confirms that "the majority" voted favourably, which supports the direction of the vote but not the exact count. Romosozumab, Descovy and tanezumab: FDA review PDFs were image-only or did not contain the tally.

## Outcomes sourced from press or company statements only

| meeting_date   | brand                                  | generic                                                         | final_action                                                                                    | final_action_date   |
|:---------------|:---------------------------------------|:----------------------------------------------------------------|:------------------------------------------------------------------------------------------------|:--------------------|
| 2016-11-04     |                                        | solithromycin                                                   | CRL (not approved as of 2026-11)                                                                | 2016-12-29          |
| 2017-08-02     |                                        |                                                                 | CRL (not approved as of 2026-11)                                                                | 2017-09-22          |
| 2017-09-28     | Translarna                             | ataluren                                                        | CRL (not approved)                                                                              | 2017-10             |
| 2017-11-16     |                                        |                                                                 | not approved (no FDA approval on record as of 2026-11; openFDA has no NDA 209367)               |                     |
| 2018-01-11     |                                        |                                                                 | CRL (not approved)                                                                              | 2018-01-29          |
| 2018-05-03     |                                        |                                                                 | CRL (not approved as of 2026-11)                                                                | 2018-08             |
| 2018-05-10     | WAYLIVRA                               | volanesorsen                                                    | CRL (not approved as of 2026-11)                                                                | 2018-08             |
| 2018-05-22     |                                        |                                                                 | CRL (not approved)                                                                              | 2018-07-27          |
| 2018-06-26     |                                        |                                                                 | CRL (not approved)                                                                              | 2018-08-06          |
| 2018-07-25     | NUCALA                                 | mepolizumab (COPD)                                              | CRL 2018-09-07 (later approved 2025-05-22 on new MATINEE data; S-007)                           | 2018-09-07          |
| 2018-11-01     |                                        |                                                                 | CRL (not approved as of 2026-11)                                                                | 2019-02-01          |
| 2018-11-14     | (MNK-812 abuse-deterrent IR oxycodone) |                                                                 | CRL (not approved)                                                                              | 2018-12-12          |
| 2019-09-18     |                                        |                                                                 | CRL (not approved; no approval on record)                                                       | 2019                |
| 2019-11-13     | JARDIANCE                              | EMPAGLIFLOZIN                                                   | CRL (T1D supplement not approved)                                                               | 2020-03             |
| 2019-12-10     |                                        |                                                                 | CRL (not approved)                                                                              | 2019-12-24          |
| 2020-01-14     |                                        | oxycodegol (NKTR-181)                                           | withdrawn by sponsor (not approved)                                                             | 2020-01             |
| 2020-01-15     |                                        |                                                                 | not approved (no action after 2nd adcom; see SEC ex99)                                          |                     |
| 2020-02-26     | TOOKAD                                 | padeliporfin                                                    | not approved (no FDA approval on record; CRL not located)                                       |                     |
| 2020-08-31     | TRELEGY ELLIPTA                        | FLUTICASONE FUROATE;UMECLIDINIUM BROMIDE;VILANTEROL TRIFENATATE | not approved (mortality claim not added to label)                                               |                     |
| 2020-10-08     |                                        |                                                                 | not approved (no approval on record; discontinued 2022)                                         |                     |
| 2021-03-24     |                                        | tanezumab                                                       | CRL; development discontinued 2021-10 (not approved)                                            | 2021                |
| 2021-04-15     | Lantidra                               | donislecel (allogeneic islets)                                  | approved                                                                                        | 2023-06-28          |
| 2021-06-24     |                                        |                                                                 | CRL (SCAC indication; retifanlimab later approved for Merkel cell 2023 / SCAC 2025 on new data) | 2021-07-23          |
| 2021-07-15     | (roxadustat)                           |                                                                 | CRL (not approved as of 2026-11)                                                                | 2021-08-11          |
| 2021-09-17     |                                        |                                                                 | not approved as asked (16+ booster sBLA); EUA booster for 65+/high-risk                         | 2021-09-22          |
| 2021-12-08     | (bardoxolone methyl)                   |                                                                 | CRL (not approved as of 2026-11)                                                                | 2022-02-25          |
| 2022-02-10     |                                        |                                                                 | CRL (not approved as of 2026-11)                                                                | 2022-03-24          |
| 2022-02-15     |                                        |                                                                 | not approved (CRLs 2020-10-09, 2021-06-11; appeal denied 2022-03-18)                            | 2022-03-18          |
| 2022-06-10     | Zynteglo                               | betibeglogene autotemcel (beti-cel)                             | approved                                                                                        | 2022-08-17          |
| 2022-06-17     | NUPLAZID                               | PIMAVANSERIN TARTRATE                                           | CRL (supplemental indication not approved)                                                      | 2022-08-04          |
| 2022-09-22     |                                        | poziotinib                                                      | CRL (not approved as of 2026-11)                                                                | 2022-11-24          |
| 2022-10-28     |                                        | 131I-omburtamab                                                 | CRL (not approved as of 2026-11)                                                                | 2022-11-30          |
| 2022-12-13     |                                        | omecamtiv mecarbil                                              | CRL (not approved as of 2026-11)                                                                | 2023-02-28          |
| 2023-09-13     | ONPATTRO                               | PATISIRAN SODIUM                                                | CRL (supplemental indication not approved)                                                      | 2023-10-08          |
| 2023-10-05     | LUMAKRAS                               | SOTORASIB                                                       | CRL (full approval sNDA not approved; accelerated approval stands)                              | 2023-12-26          |
| 2023-11-17     |                                        |                                                                 | CRL (not approved as of 2026-11)                                                                | 2023-12-20          |
| 2024-03-15     | CARVYKTI                               |                                                                 | approved (CARVYKTI after 1 prior line)                                                          | 2024-04-05          |
| 2024-03-15     | ABECMA                                 |                                                                 | approved (ABECMA after 2 prior lines)                                                           | 2024-04-04          |
| 2024-09-13     | OCALIVA                                | OBETICHOLIC ACID                                                | CRL (full approval sNDA)                                                                        | 2024-11-12          |
| 2024-10-31     |                                        |                                                                 | CRL (not approved as of 2026-11)                                                                | 2024-12-20          |
| 2025-01-10     |                                        |                                                                 | CRL (not approved as of 2026-11)                                                                | 2025-03-11          |
| 2025-05-20     | COLUMVI                                | glofitamab                                                      | CRL (2L DLBCL sBLA)                                                                             | 2025-07-18          |
| 2025-07-18     | REXULTI                                | BREXPIPRAZOLE                                                   | CRL (PTSD sNDA)                                                                                 | 2025-09             |
| 2026-07-29     | (deramiocel)                           | deramiocel (CAP-1002)                                           | pending (PDUFA extended to 2026-11-22)                                                          |                     |

## Orphan status: unresolved

| meeting_date   | committee   |    app | brand           | product_text   |
|:---------------|:------------|-------:|:----------------|:---------------|
| 2025-05-20     | ODAC        | 761145 | DARZALEX FASPRO |                |
| 2026-07-30     | CTGTAC      | 125827 | TUDRIQEV        | Tudriqev       |

## Decisions on the wrong-question rows (item 4)
- Tavneos 2021-05-06: switched to the benefit-risk vote, 10-8 (FDA minutes). The efficacy vote was 9-9.
- Ocaliva 2024-09-13: switched to the benefit-risk vote, 1-10-3 (media/182630). The clinical-benefit vote was 1-13.
- Zelnorm 2018-10-17: kept 11-1 ("reintroduction supported").
- Entresto 2020-12-15: kept 12-1 ("ANY indication").
- Lynparza 2023-04-28: kept 11-1, but this was a vote to restrict the indication, not an approve/reject vote. Flagged as favourable-restricted.
- Lumakras 2023-10-05: kept 2-10 as a proxy. The only vote was on whether PFS could be interpreted. Flagged.
- Aduhelm 2020-11-06: pivotal set to 0-10-1 (final question, Study 302 as primary evidence). Q1 was 1-8-2 and is noted on the row (media/145690).

## Reconciliation with the hand-verified data (out/, 2016-11 onward)

| date       | brand        | app          | status   | new   | handverified   |
|:-----------|:-------------|:-------------|:---------|:------|:---------------|
| 2017-10-12 | Luxturna     | 125610       | match    | 16-0  | 16-0           |
| 2021-04-15 | Lantidra     | 125734       | match    | 12-4  | 12-4           |
| 2022-06-09 | Skysona      | 125755       | match    | 15-0  | 15-0           |
| 2022-06-10 | Zynteglo     | 125717       | match    | 13-0  | 13-0           |
| 2023-05-12 | Elevidys     | 125781       | match    | 8-6   | 8-6            |
| 2023-09-27 | NurOwn       | 125782       | match    | 1-17  | 1-17           |
| 2026-07-29 | (deramiocel) | 125842       | match    | 3-9   | 3-9            |
| 2026-07-30 | Tudriqev     | 125827       | match    | 10-3  | 10-3           |
| 2017-09-28 | Translarna   | 200896       | DIFF     | 1-10  | 0-10           |
| 2018-04-19 | Epidiolex    | 210365       | match    | 13-0  | 13-0           |
| 2020-11-06 | Aduhelm      | 761178       | match    | 0-10  | 0-10           |
| 2022-03-30 | Relyvrio     | 216660       | match    | 4-6   | 4-6            |
| 2022-09-07 | Relyvrio     | 216660       | match    | 7-2   | 7-2            |
| 2023-03-22 | Qalsody      | 215887       | match    | 9-0   | 9-0            |
| 2023-06-09 | Leqembi      | 761269/S-001 | MISSING  | nan   | 6-0            |
| 2024-06-10 | Kisunla      | 761248       | match    | 11-0  | 11-0           |
| 2023-04-14 | Rexulti      | 205422/S-009 | match    | 9-1   | 9-1            |

- Leqembi is present (app 761269). It shows as MISSING above only because of the "/S-001" suffix in the key.
- Translarna: the minutes give A:0 / B:10 / C:1. We code C ("sufficient to conclude effective") as yes, which gives 1-10. The out/ data treats C as an abstain, giving 0-10-1. This is a coding choice, not a data error.
- PCNS: all 8 present (Translarna, Epidiolex, Aduhelm, Relyvrio x2, Qalsody, Leqembi, Kisunla), plus the joint Rexulti PDAC+PCNS row. CGT: Luxturna, Skysona, Zynteglo, Elevidys, NurOwn, Lantidra, deramiocel and Tudriqev (now added: 10-3, FDA SBRA media/194230) are present, and Kymriah, Ryoncil, Carvykti and Abecma are flagged CGT (12 CGT rows).

## Shortfall vs Daval, 2016-2021 (daval_shortfall_explained.csv has one row per year x committee)

| committee   |   daval_meetings |   ours_product_vote_rows |   ours_excluded |   pre_window_2016 |   residual_shortfall |   residual_after_prewindow |
|:------------|-----------------:|-------------------------:|----------------:|------------------:|---------------------:|---------------------------:|
| AAC         |               11 |                        6 |               1 |                 3 |                    4 |                          1 |
| AADPAC      |               28 |                       10 |               2 |                 4 |                   16 |                         12 |
| AMDAC       |               16 |                       11 |               3 |                 1 |                    2 |                          1 |
| BRUDAC      |                8 |                        4 |               3 |                 1 |                    1 |                          0 |
| CRDAC       |                6 |                        5 |               0 |                 0 |                    1 |                          1 |
| DODAC       |                3 |                        2 |               0 |                 0 |                    1 |                          1 |
| DSaRM       |                2 |                        3 |               9 |                 0 |                  -10 |                        -10 |
| EMDAC       |               11 |                        7 |               0 |                 3 |                    4 |                          1 |
| GIDAC       |                5 |                        4 |               0 |                 1 |                    1 |                          0 |
| MIDAC       |                2 |                        1 |               3 |                 0 |                   -2 |                         -2 |
| NDAC        |                3 |                        1 |               1 |                 1 |                    1 |                          0 |
| ODAC        |               38 |                       17 |              10 |                 2 |                   11 |                          9 |
| PADAC       |                3 |                        3 |               2 |                 0 |                   -2 |                         -2 |
| PCAC        |                7 |                        0 |               0 |                 0 |                    7 |                          7 |
| PCNS        |                4 |                        3 |               0 |                 1 |                    1 |                          0 |
| PDAC        |               14 |                        9 |               2 |                 3 |                    3 |                          0 |
| PSCPAC      |                3 |                        0 |               3 |                 0 |                    0 |                          0 |

Totals: Daval 164 meetings. We have 86 product-vote rows and 39 excluded meetings. 20 of Daval's 2016 meetings fall before 2016-11-04, outside our scope. That leaves a net 19 unexplained.
- PCAC accounts for 7: compounding-list meetings, not NDA/BLA approvals.
- AADPAC/DSaRM joint meetings are attributed differently: AADPAC is +16 and DSaRM is -10 (net 6).
- The remainder (roughly 6-10, mostly ODAC, EMDAC and AAC) has not been identified meeting by meeting. Daval publishes counts only, not a meeting list, so a true row-by-row match is not possible. Likely causes are multi-day meetings counted per day and class or policy sessions with no NDA/BLA in the Federal Register notice.

## What changed this stage
- Fixed a bug in final.py where curated "add" rows overwrote existing rows (index collision). This raised the row count from 121 to 155. Curated rows that duplicated an existing meeting/app are now merged instead of added.
- All 68 gap meetings resolved:
  - 30 gap meetings became rows (gap_votes.csv: 12 FDA-sourced, the rest press).
  - About 32 were moved to excluded with a reason (gap_excl.csv: no vote, cancelled, class review, IND, duplicate).
  - The remaining gaps duplicated existing rows.
- All 38 unverified outcomes are now sourced. Supplements are matched by supplement number in openFDA and checked against the FDA approval letter text (ltr/). CBER outcomes come from FDA BLA approval lists and letters. The rest are press or company statements, flagged as such.
- Added orphan_for_indication: OOPD designation keyword-matched to the indication, hand-verified values carried over from legacy rows, and 26 weak matches adjudicated (orphan_adj.csv).
- Added vote_source_tier and outcome_source_tier columns.

## Not done / caveats
- Press votes (list above) could not be confirmed against FDA documents. The fda.gov committee pages return 404, and the review PDFs found were image-only.
- The waiter loops chained after mscan/ait matched their own command lines and could never finish, so they were killed. mscan.py (144000–196000) has since finished, but the 118000–144000 range and ait2 never ran. With gaps at 0, those runs are optional. The pipeline was rerun manually.
- Pre-2016-11 rows stay in sheet pre_2016-11_not_curated and were not worked further.
