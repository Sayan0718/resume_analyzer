// main.js - AI-Powered Resume Analyzer

document.addEventListener("DOMContentLoaded", () => {
    console.log("AI Resume Analyzer Loaded Successfully!");

    // Smooth scroll effect (optional enhancement)
    const links = document.querySelectorAll("a[href^='/']");
    links.forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            window.location.href = this.getAttribute("href");
        });
    });
});

window.addEventListener("load", function () {
    const loader = document.getElementById("loader-wrapper");
    loader.style.opacity = "0";
    setTimeout(() => loader.style.display = "none", 500); // Smooth fade out
  });
// JavaScript for interactivity
