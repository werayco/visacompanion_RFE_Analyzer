from docx import Document
import json

class utils:
    @staticmethod
    def CriterionDocCreator(result: dict) -> str:
        doc = Document()
        doc.add_heading("Criterion EB-1A Petition Assessment Summary", level=1)

        section_num = 1

        recognizable_components = result.get("recognizable_components", {})
        background = recognizable_components.get("personal_background", "")
        expert_letters = recognizable_components.get("expert_recommendation_letters", [])
        media_and_judging = recognizable_components.get("media_and_judging_roles", [])
        red_flags = recognizable_components.get("red_flags", {})
        evidence = recognizable_components.get("evidence", {})

        doc.add_heading(f"{section_num}. Personal Background", level=2)
        doc.add_paragraph(background)
        section_num += 1

        doc.add_heading(f"{section_num}. Expert Recommendation Letters", level=2)
        for letter in expert_letters:
            doc.add_paragraph(f"{letter}")
        section_num += 1

        doc.add_heading(f"{section_num}. Media and Judging Roles", level=2)
        for role in media_and_judging:
            doc.add_paragraph(role)
        section_num += 1

        doc.add_heading(f"{section_num}. Red Flags", level=2)
        for k, v in red_flags.items():
            title = k.replace("_", " ").title()
            doc.add_paragraph(f"{title}: {v}", style="List Bullet")
        section_num += 1

        internationalAward: dict = result.get("internationalAward", {})
        majorAwards: bool = internationalAward.get("has_major_award")
        justification: str = internationalAward.get("justification", "")
        award_names: list = internationalAward.get("award_names", [])
        missing_elements: list = internationalAward.get("missing_elements", [])
        suggested_supporting_evidence: list = internationalAward.get("suggested_supporting_evidence", [])

        doc.add_heading(f"{section_num}. International Award Evaluation", level=2)
        has_award_text = "Yes, a major internationally recognized award is present." if majorAwards else "No, a qualifying major internationally recognized award was not found."
        doc.add_paragraph(f"Has Major Award: {has_award_text}")

        if award_names:
            doc.add_paragraph("Award(s) Mentioned:")
            for name in award_names:
                doc.add_paragraph(f" {name}", style="List Bullet")

        if justification:
            doc.add_paragraph("Justification:")
            doc.add_paragraph(justification)

        if missing_elements:
            doc.add_paragraph("Missing Elements:")
            for item in missing_elements:
                doc.add_paragraph(f" {item}", style="List Bullet")

        if suggested_supporting_evidence:
            doc.add_paragraph("Suggested Supporting Evidence:")
            for item in suggested_supporting_evidence:
                doc.add_paragraph(f" {item}", style="List Bullet")
        section_num += 1

        doc.add_heading(f"{section_num}. Criteria-specific Evidence", level=2)
        roman_sections = [
            ("I. Lesser Awards", "lesser_awards"),
            ("II. Association Membership", "association_membership"),
            ("III. Published Material", "published_material"),
            ("IV. Judging Others Work", "judging_work_of_others"),
            ("V. Original Contributions", "original_contributions"),
            ("VI. Scholarly Articles", "scholarly_articles"),
            ("VII. Artistic Display", "artistic_display"),
            ("VIII. Leading Role", "leading_or_critical_role"),
            ("IX. High Salary", "high_salary_or_remuneration"),
            ("X. Commercial Success In Arts", "commercial_success_in_arts"),
        ]
        for title, key in roman_sections:
            doc.add_heading(title, level=2)
            if key in evidence:
                for item in evidence[key]:
                    doc.add_paragraph(item, style="List Bullet")
        section_num += 1

        summary = result.get("summary", {})
        doc.add_heading(f"{section_num}. Summary", level=2)
        doc.add_paragraph(f"Qualification Path: {summary.get('qualification_path', '')}")
        doc.add_paragraph(f"Status: {summary.get('status', '')}")
        doc.add_paragraph(f"Criteria Met: {summary.get('criteria_met', '')}")
        doc.add_paragraph(f"Total Criteria Checked: {summary.get('total_criteria_checked', '')}")
        section_num += 1

        criterionTitles = {
            "Criterion1Result": "Criterion 1: Documentation of the alien's receipt of lesser nationally or internationally recognized prizes or awards for excellence in the field of endeavor.",
            "Criterion2Result": "Criterion 2: Documentation of the alien's membership in associations in the field which demand outstanding achievement of their members.",
            "Criterion3Result": "Criterion 3: Published material about the alien in professional or major trade publications or other major media, relating to the alien's work in the field.",
            "Criterion4Result": "Criterion 4: Evidence of the alien's participation, either individually or on a panel, as a judge of the work of others in the same or an allied field.",
            "Criterion5Result": "Criterion 5: Evidence of the alien's original scientific, scholarly, artistic, athletic, or business-related contributions of major significance in the field.",
            "Criterion6Result": "Criterion 6: Evidence of the alien's authorship of scholarly articles in professional or major trade publications or other major media.",
            "Criterion7Result": "Criterion 7: Evidence of the display of the alien's work in exhibitions or showcases.",
            "Criterion8Result": "Criterion 8: Evidence that the alien has performed in a leading or critical role for organizations or establishments that have a distinguished reputation.",
            "Criterion9Result": "Criterion 9: Evidence that the alien has commanded a high salary or other significantly high remuneration for services in relation to others in the field.",
            "Criterion10Result": "Criterion 10: Evidence of commercial successes in the performing arts, as shown by box office receipts or record, cassette, compact disk, or video sales.",
        }

        doc.add_heading(f"{section_num}. Detailed Criterion Evaluation", level=2)

        for i in range(1, 11):
            criterion_key = f"Criterion{i}Result"
            criterion_data = result.get(criterion_key, {})
            doc.add_heading(criterionTitles.get(criterion_key, f"Criterion {i}"), level=3)

            if not criterion_data:
                doc.add_paragraph("No data provided.")
                continue

            if criterion_data.get("status") == "couldn't parse the content":
                doc.add_paragraph("Could not parse this criterion.")
                continue

            doc.add_paragraph(f"Meets Criterion: {criterion_data.get(f'meets_criterion_{i}', 'Unknown')}")

            reasoning = criterion_data.get("reasoning") or criterion_data.get("overall_reasoning", "")
            if reasoning:
                doc.add_paragraph(f"Reasoning:\n{reasoning}")

            for key in [
                "issues_detected", "award_names", "association_names",
                "salary_records", "articles", "judging_instances",
                "missing_elements", "suggested_supporting_evidence"
            ]:
                if key in criterion_data:
                    doc.add_paragraph(key.replace("_", " ").title() + ":")
                    for item in criterion_data[key]:
                        if isinstance(item, dict):
                            summary = ", ".join(f"{k}: {v}" for k, v in item.items())
                            doc.add_paragraph(f" {summary}", style="List Bullet")
                        else:
                            doc.add_paragraph(f" {item}", style="List Bullet")

            if "contributions" in criterion_data:
                doc.add_paragraph("Contributions:")
                for contrib in criterion_data["contributions"]:
                    title = contrib.get("title_or_description", "")
                    impact = contrib.get("impact_summary", "")
                    doc.add_paragraph(f" {title}", style="List Bullet")
                    if impact:
                        doc.add_paragraph(f"   Impact: {impact}")

        output_path = "Criterion_EB1A_Assessment_Summary.docx"
        doc.save(output_path)
        return output_path
    
    @staticmethod
    def jsonSaver(jsonObject: dict):
        with open("result.json", "w", encoding="utf-8") as result:
            json.dump(jsonObject, result, ensure_ascii=False, indent=2)

    def JsonLoader(jsonPath: str) -> dict:
        with open(jsonPath, "r") as result:
            data = json.load(result)
            return data