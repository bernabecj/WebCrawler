// Sort by date or name

document.querySelectorAll(".sort-option").forEach((item) => {
    item.addEventListener("click", function (e) {
        e.preventDefault();
        const value = this.getAttribute("data-value");
        document.getElementById("currentSort").textContent = value;
    });
});