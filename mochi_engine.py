def calculate_match(user_skills, job_skills):

    if not user_skills or not job_skills:
        return 0, "No skill data available"

    user_set = set(user_skills.lower().split(","))
    job_set = set(job_skills.lower().split(","))

    common = user_set.intersection(job_set)

    if not job_set:
        return 0, "No job skills defined"

    score = int((len(common) / len(job_set)) * 100)

    reason = f"Matched skills: {', '.join(common)}" if common else "No direct skill match"

    return score, reason