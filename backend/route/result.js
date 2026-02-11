const express = require("express");
const router = express.Router();
const db = require("../db");

router.get("/:studentId", (req, res) => {
  db.query(
    "SELECT * FROM results WHERE student_id=?",
    [req.params.studentId],
    (err, data) => {
      if (err) throw err;
      res.json(data);
    }
  );
});

module.exports = router;
