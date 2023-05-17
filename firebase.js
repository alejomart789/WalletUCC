// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAmPt3bAZG2nRGMYO63b73VKTTr742OPeg",
  authDomain: "henessy-8a4fa.firebaseapp.com",
  projectId: "henessy-8a4fa",
  storageBucket: "henessy-8a4fa.appspot.com",
  messagingSenderId: "332136735780",
  appId: "1:332136735780:web:56b1c940a1695a8f7d64b1",
  measurementId: "G-051GQ5QTJG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);