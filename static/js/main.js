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
// JavaScript for interactivity
