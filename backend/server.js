const express = require("express");
const bodyParser = require("body-parser");

const examRoutes = require("./route/exam");
const resultRoutes = require("./route/result");

const app = express();
app.use(bodyParser.json());

app.use("/exam", examRoutes);
app.use("/result", resultRoutes);

app.listen(3000, () => {
  console.log("Server running on port 3000 🚀");
});
