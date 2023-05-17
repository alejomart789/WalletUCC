const functions = require("firebase-functions");
const express = require("express");
const djangoExpress = require("django-express");
const app = express();

const djangoApp = djangoExpress({
  root: __dirname + "/walletucc", // Asegúrate de incluir "/" antes de "WalletUCC"
  djangoSettingsModule: "walletucc.settings",
});

app.all("**", (req, res) => {
  djangoApp(req, res, () => {
    res.status(404).send("Page not found");
  });
});

exports.yourDjangoFunction = functions.https.onRequest(app);
