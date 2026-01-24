"""
Tests for infobox expansion (expend_infobox.py)
"""
from src.infobox.expend_infobox import expend_new

# Test data from infoboxTest.php
TEXT_INPUT = r"""{{Infobox drug|verifiedrevid=461217017|image=Omaveloxolone structure.svg|width=250|alt=|caption=<!-- Names -->|pronounce=|tradename=Skyclarys|synonyms=RTA 408|IUPAC_name=N-((4aS,6aR,6bS,8aR,12aS,14aR,14bS)-1 1-cyano-2,2,6a,6b,9,9,12a-heptamethyl-10,14-dioxo-1,2,3,4,4a,5,6,6a,6b,7,8,8a,9,10,12a,14,14a,14b- octadecahydropicen-4a-yl)-2,2-difluoropropanamide

<!-- Clinical data -->|pregnancy_AU=<!-- A / B1 / B2 / B3 / C / D / X -->|pregnancy_AU_comment=|pregnancy_category=|routes_of_administration=[[By mouth]]|onset=|duration_of_action=|Drugs.com={{Drugs.com|monograph|omaveloxolone}}|MedlinePlus=<!-- Legal data -->|legal_AU=<!-- S2, S3, S4, S5, S6, S7, S8, S9 or Unscheduled -->|legal_AU_comment=|legal_CA=<!-- OTC, Rx-only, Schedule I, II, III, IV, V, VI, VII, VIII -->|legal_CA_comment=|legal_DE=<!-- Anlage I, II, III or Unscheduled -->|legal_DE_comment=|legal_EU=|legal_EU_comment=|legal_NZ=<!-- Class A, B, C -->|legal_NZ_comment=|legal_UN=<!-- N I, II, III, IV / P I, II, III, IV -->|legal_UN_comment=|legal_UK=<!-- GSL, P, POM, CD, CD Lic, CD POM, CD No Reg POM, CD (Benz) POM, CD (Anab) POM or CD Inv POM / Class A, B, C -->|legal_UK_comment=|legal_US=Rx-only|legal_US_comment=<ref name="Skyclarys FDA label">{{Cite web |url=https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/216718Orig1s000lbl.pdf |title=Archived copy |access-date=1 March 2023 |archive-date=1 March 2023 |archive-url=https://web.archive.org/web/20230301063942/https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/216718Orig1s000lbl.pdf |url-status=live }}</ref>|legal_status=<!-- For countries not listed above -->|DailyMedID=Omaveloxolone

<!-- Pharmacokinetic data -->|bioavailability=|protein_bound=|metabolism=|metabolites=|elimination_half-life=|excretion=<!-- Chemical and physical data -->|C=33|F=2|H=44|N=2|O=3|SMILES=O=C4C(\C#N)=C/[C@@]5(/C3=C/C(=O)[C@H]2[C@](CC[C@@]1(NC(=O)C(F)(F)C)CCC(C)(C)C[C@H]12)(C)[C@]3(C)CC[C@H]5C4(C)C)C|StdInChI=1S/C32H43NO4/c1-27(2)11-13-32(26(36)37-8)14-12-31(7)24(20(32)17-27)21(34)15-23-29(5)16-19(18-33)25(35)28(3,4)22(29)9-10-30(23,31)6/h15-16,20,22,24H,9-14,17H2,1-8H3/t20-,22-,24-,29-,30+,31+,32-/m0/s1|StdInChI_Ref={{stdinchicite|correct|chemspider}}|StdInChI_comment=|StdInChIKey=WPTTVJLTNAWYAO-KPOXMGGZSA-N|StdInChIKey_Ref={{stdinchicite|correct|chemspider}}|density=|density_notes=|melting_point=|melting_high=|melting_notes=|boiling_point=|boiling_notes=|solubility=|specific_rotation=}}
"""

TEXT_OUTPUT = r"""{{Infobox drug
|verifiedrevid    =461217017
|image            =Omaveloxolone structure.svg
|width            =250
|alt              =
|caption          =

<!-- Names -->
|pronounce        =
|tradename        =Skyclarys
|synonyms         =RTA 408
|IUPAC_name       =N-((4aS,6aR,6bS,8aR,12aS,14aR,14bS)-1 1-cyano-2,2,6a,6b,9,9,12a-heptamethyl-10,14-dioxo-1,2,3,4,4a,5,6,6a,6b,7,8,8a,9,10,12a,14,14a,14b- octadecahydropicen-4a-yl)-2,2-difluoropropanamide

<!-- Clinical data -->
|pregnancy_AU     =<!-- A / B1 / B2 / B3 / C / D / X -->
|pregnancy_AU_comment=
|pregnancy_category=
|routes_of_administration=[[By mouth]]
|onset            =
|duration_of_action=
|Drugs.com        ={{Drugs.com|monograph|omaveloxolone}}
|MedlinePlus      =

<!-- Legal data -->
|legal_AU         =<!-- S2, S3, S4, S5, S6, S7, S8, S9 or Unscheduled -->
|legal_AU_comment =
|legal_CA         =<!-- OTC, Rx-only, Schedule I, II, III, IV, V, VI, VII, VIII -->
|legal_CA_comment =
|legal_DE         =<!-- Anlage I, II, III or Unscheduled -->
|legal_DE_comment =
|legal_EU         =
|legal_EU_comment =
|legal_NZ         =<!-- Class A, B, C -->
|legal_NZ_comment =
|legal_UN         =<!-- N I, II, III, IV / P I, II, III, IV -->
|legal_UN_comment =
|legal_UK         =<!-- GSL, P, POM, CD, CD Lic, CD POM, CD No Reg POM, CD (Benz) POM, CD (Anab) POM or CD Inv POM / Class A, B, C -->
|legal_UK_comment =
|legal_US         =Rx-only
|legal_US_comment =<ref name="Skyclarys FDA label">{{Cite web |url=https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/216718Orig1s000lbl.pdf |title=Archived copy |access-date=1 March 2023 |archive-date=1 March 2023 |archive-url=https://web.archive.org/web/20230301063942/https://www.accessdata.fda.gov/drugsatfda_docs/label/2023/216718Orig1s000lbl.pdf |url-status=live }}</ref>
|legal_status     =<!-- For countries not listed above -->
|DailyMedID       =Omaveloxolone

<!-- Pharmacokinetic data -->
|bioavailability  =
|protein_bound    =
|metabolism       =
|metabolites      =
|elimination_half-life=
|excretion        =

<!-- Chemical and physical data -->
|C                =33
|F                =2
|H                =44
|N                =2
|O                =3
|SMILES           =O=C4C(\C#N)=C/[C@@]5(/C3=C/C(=O)[C@H]2[C@](CC[C@@]1(NC(=O)C(F)(F)C)CCC(C)(C)C[C@H]12)(C)[C@]3(C)CC[C@H]5C4(C)C)C
|StdInChI         =1S/C32H43NO4/c1-27(2)11-13-32(26(36)37-8)14-12-31(7)24(20(32)17-27)21(34)15-23-29(5)16-19(18-33)25(35)28(3,4)22(29)9-10-30(23,31)6/h15-16,20,22,24H,9-14,17H2,1-8H3/t20-,22-,24-,29-,30+,31+,32-/m0/s1
|StdInChI_Ref     ={{stdinchicite|correct|chemspider}}
|StdInChI_comment =
|StdInChIKey      =WPTTVJLTNAWYAO-KPOXMGGZSA-N
|StdInChIKey_Ref  ={{stdinchicite|correct|chemspider}}
|density          =
|density_notes    =
|melting_point    =
|melting_high     =
|melting_notes    =
|boiling_point    =
|boiling_notes    =
|solubility       =
|specific_rotation=
}}
"""


def test_expend_new_simple_template():
    """Test expend_new with a simple template"""
    # Test with basic template
    result = expend_new(TEXT_INPUT).strip()
    assert result == TEXT_OUTPUT.strip()
