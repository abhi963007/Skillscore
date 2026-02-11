const express = require("express");
const router = express.Router();
const db = require("../db");
const evaluate = require("../evaluation");

router.post("/submit", (req, res) => {
  const { studentId, answers } = req.body;

  db.query("SELECT * FROM questions", (err, questions) => {
    if (err) throw err;

    const result = evaluate(questions, answers);

    db.query(
      "INSERT INTO results (student_id, total_marks, scored_marks, skill_score, placement_status) VALUES (?,?,?,?,?)",
      [studentId, result.total, result.scored, result.skillScore, result.status]
    );

    res.json(result);
  });
});

module.exports = router;
