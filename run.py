from src.llm_agent import RFEBOT
from docLoaders.petition_loaders import petitionLoaders
from typing import TypedDict, Any, Dict, Optional

class SelectedCriterion(TypedDict, total=False):
    internationalAward: Optional[Dict[str, Any]]
    Criterion1Result: Optional[Dict[str, Any]]
    Criterion2Result: Optional[Dict[str, Any]]
    Criterion3Result: Optional[Dict[str, Any]]
    Criterion4Result: Optional[Dict[str, Any]]
    Criterion5Result: Optional[Dict[str, Any]]
    Criterion6Result: Optional[Dict[str, Any]]
    Criterion7Result: Optional[Dict[str, Any]]
    Criterion8Result: Optional[Dict[str, Any]]
    Criterion9Result: Optional[Dict[str, Any]]
    Criterion10Result: Optional[Dict[str, Any]]
    summary: Optional[Dict[str, Any]]

def main(file_path: str) -> Dict[str, Any]:
    selected_criterion: SelectedCriterion = {}

    try:
        petition_content: str = petitionLoaders.extract_text_from_file(file_path)

        if not petition_content:
            return {"error": "Couldn't extract text from the document"}

        international_award: Dict[str, Any] = RFEBOT.AgentpromptInternationalAward(petition_content)
        has_major_award = international_award.get("has_major_award")

        if isinstance(has_major_award, str) and has_major_award.lower() == "true":
            selected_criterion["internationalAward"] = international_award
            selected_criterion["summary"] = {
                "qualification_path": "major_international_award",
                "criteria_needed": 0,
                "criteria_met": 1,
                "status": "qualified"
            }
            return selected_criterion

        criteria_results = []
        criteria_functions = [
            ("Criterion1Result", RFEBOT.AgenticCriterionPrompt1, "meets_criterion_1"),
            ("Criterion2Result", RFEBOT.AgenticCriterionPrompt2, "meets_criterion_2"),
            ("Criterion3Result", RFEBOT.AgenticCriterionPrompt3, "meets_criterion_3"),
            ("Criterion4Result", RFEBOT.AgenticCriterionPrompt4, "meets_criterion_4"),
            ("Criterion5Result", RFEBOT.AgenticCriterionPrompt5, "meets_criterion_5"),
            ("Criterion6Result", RFEBOT.AgenticCriterionPrompt6, "meets_criterion_6"),
            ("Criterion7Result", RFEBOT.AgenticCriterionPrompt7, "meets_criterion_7"),
            ("Criterion8Result", RFEBOT.AgenticCriterionPrompt8, "meets_criterion_8"),
            ("Criterion9Result", RFEBOT.AgenticCriterionPrompt9, "meets_criterion_9"),
            ("Criterion10Result", RFEBOT.AgenticCriterionPrompt10, "meets_criterion_10")
        ]

        met_criteria_count = 0
        processed_criteria = []

        for criterion_name, criterion_function, criterion_key in criteria_functions:
            try:
                criterion_result: Dict[str, Any] = criterion_function(petition_content)
                selected_criterion[criterion_name] = criterion_result
                processed_criteria.append(criterion_name)

                meets = criterion_result.get(criterion_key)
                if isinstance(meets, str):
                    meets = meets.lower() == "true"
                elif isinstance(meets, bool):
                    meets = meets is True

                if meets:
                    met_criteria_count += 1
                    criteria_results.append(criterion_name)

            except AttributeError:
                selected_criterion[criterion_name] = {"error": "Function not implemented"}
                processed_criteria.append(criterion_name)
            except Exception as e:
                selected_criterion[criterion_name] = {"error": str(e)}
                processed_criteria.append(criterion_name)

        qualification_status = "qualified" if met_criteria_count >= 3 else "not_qualified"

        selected_criterion["summary"] = {
            "qualification_path": "ten_criteria",
            "criteria_needed": 3,
            "criteria_met": met_criteria_count,
            "met_criteria": criteria_results,
            "processed_criteria": processed_criteria,
            "total_criteria_checked": len(processed_criteria),
            "status": qualification_status,
            "early_qualification": met_criteria_count >= 3 and len(processed_criteria) < 10
        }
        background:dict = RFEBOT.Agentprompt(petition_content)
        selected_criterion["recognizable_components"] = background
        return selected_criterion

    except FileNotFoundError:
        return {"error": f"File not found: {file_path}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

result = main(file_path=r"C:\Users\miztu\Downloads\inkin.pdf")
def mainer(result:dict):
    criteria_results = ["Criterion1Result", "Criterion2Result", "Criterion3Result", "Criterion4Result", "Criterion5Result", "Criterion6Result", "Criterion7Result", "Criterion8Result", "Criterion9Result", "Criterion10Result"]

    criterion1 = result.get(criteria_results[0])
    criterion2 = result.get(criteria_results[1])
    criterion3 = result.get(criteria_results[2])
    criterion4 = result.get(criteria_results[3])
    criterion5 = result.get(criteria_results[4])
    criterion6 = result.get(criteria_results[5])
    criterion7 = result.get(criteria_results[6])
    criterion8 = result.get(criteria_results[7])
    criterion9 = result.get(criteria_results[8])
    criterion10 = result.get(criteria_results[9])
    summary = result.get("summary")
    
    return 


# print(result)
