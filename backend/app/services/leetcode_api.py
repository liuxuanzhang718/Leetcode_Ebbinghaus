import requests
from typing import Optional, Dict, Any
from ..models.models import DifficultyEnum

class LeetCodeAPI:
    BASE_URL = "https://leetcode.com/api"
    GRAPHQL_URL = "https://leetcode.com/graphql"

    @staticmethod
    def get_problem_details(problem_number: int) -> Optional[Dict[str, Any]]:
        """
        Fetch problem details from LeetCode API using problem number.
        Returns None if problem not found or API error occurs.
        """
        # First, get the title slug from the problem number
        try:
            problems_response = requests.get(
                f"{LeetCodeAPI.BASE_URL}/problems/all/"
            )
            problems_response.raise_for_status()
            problems_data = problems_response.json()

            # Find the problem by stat_id (problem number)
            problem_stat = next(
                (p for p in problems_data["stat_status_pairs"] 
                 if p["stat"]["frontend_question_id"] == problem_number),
                None
            )

            if not problem_stat:
                return None

            title_slug = problem_stat["stat"]["question__title_slug"]

            # Get detailed problem information using GraphQL
            graphql_query = {
                "query": """
                query getQuestionDetail($titleSlug: String!) {
                    question(titleSlug: $titleSlug) {
                        questionId
                        title
                        titleSlug
                        difficulty
                        topicTags {
                            name
                        }
                    }
                }
                """,
                "variables": {"titleSlug": title_slug}
            }

            detail_response = requests.post(
                LeetCodeAPI.GRAPHQL_URL,
                json=graphql_query
            )
            detail_response.raise_for_status()
            detail_data = detail_response.json()

            question_data = detail_data["data"]["question"]
            
            return {
                "leetcode_number": problem_number,
                "title": question_data["title"],
                "difficulty": DifficultyEnum[question_data["difficulty"].upper()],
                "topics": [tag["name"] for tag in question_data["topicTags"]]
            }

        except (requests.RequestException, KeyError, StopIteration) as e:
            print(f"Error fetching problem details: {str(e)}")
            return None

    @staticmethod
    def validate_problem_number(problem_number: int) -> bool:
        """
        Validate if a problem number exists on LeetCode.
        """
        try:
            problem_details = LeetCodeAPI.get_problem_details(problem_number)
            return problem_details is not None
        except Exception:
            return False 