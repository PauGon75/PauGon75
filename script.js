/* =====================================================
   1) POPUPS ("View details" buttons)
   A button with data-dialog="job1" opens the <dialog id="job1">.
   ===================================================== */
document.querySelectorAll("[data-dialog]").forEach(function (button) {
  button.addEventListener("click", function () {
    var dialog = document.getElementById(button.dataset.dialog);
    if (dialog) dialog.showModal();
  });
});

document.querySelectorAll("dialog").forEach(function (dialog) {
  // Close with the X button
  var closeButton = dialog.querySelector(".dialog-close");
  if (closeButton) closeButton.addEventListener("click", function () { dialog.close(); });

  // Close by clicking the dark area outside the popup
  dialog.addEventListener("click", function (event) {
    if (event.target === dialog) dialog.close();
  });
  // (The Esc key closes it automatically.)
});


/* =====================================================
   2) MOBILE MENU
   ===================================================== */
var menuButton = document.querySelector(".nav-toggle");
var menuLinks = document.getElementById("nav-links");

menuButton.addEventListener("click", function () {
  var isOpen = menuLinks.classList.toggle("open");
  menuButton.setAttribute("aria-expanded", isOpen);
});

// Close the menu after tapping a link
menuLinks.querySelectorAll("a").forEach(function (link) {
  link.addEventListener("click", function () {
    menuLinks.classList.remove("open");
    menuButton.setAttribute("aria-expanded", "false");
  });
});


/* =====================================================
   3) COUNTING NUMBERS
   Numbers count up once, when they scroll into view.
   Set the final number in the HTML with data-target="12".
   Add data-prefix="+" if you want a "+" in front.
   ===================================================== */
var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function countUp(element) {
  var target = Number(element.dataset.target);
  var prefix = element.dataset.prefix || "";

  if (reduceMotion) {
    element.textContent = prefix + target;
    return;
  }

  var duration = 1200; // milliseconds
  var start = null;

  function step(timestamp) {
    if (start === null) start = timestamp;
    var progress = Math.min((timestamp - start) / duration, 1);
    element.textContent = prefix + Math.round(progress * target);
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

var observer = new IntersectionObserver(function (entries) {
  entries.forEach(function (entry) {
    if (entry.isIntersecting) {
      countUp(entry.target);
      observer.unobserve(entry.target); // only run once
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll(".stat-number").forEach(function (number) {
  observer.observe(number);
});
