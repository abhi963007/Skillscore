function evaluate(questions, answers) {
  let total = 0, scored = 0;
  let categoryScore = { aptitude: 0, technical: 0, verbal: 0 };

  questions.forEach(q => {
    total += q.marks;
    const studentAnswer = answers[q.id];

    if (
      studentAnswer &&
      studentAnswer.toLowerCase().trim() ===
      q.correct_answer.toLowerCase().trim()
    ) {
      scored += q.marks;
      categoryScore[q.category] += q.marks;
    }
  });

  const skillScore =
    categoryScore.aptitude * 0.3 +
    categoryScore.technical * 0.4 +
    categoryScore.verbal * 0.3;

  let status =
    skillScore >= 75 ? "Placement Ready" :
    skillScore >= 50 ? "Almost Ready" :
    "Needs Training";

  return { total, scored, skillScore, status };
}

module.exports = evaluate;
