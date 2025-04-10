document.addEventListener("DOMContentLoaded", function () {
    // === Handle Sorting Option Clicks ===
    document.querySelectorAll(".sort-option").forEach((item) => {
        item.addEventListener("click", function (e) {
            e.preventDefault();

            // --- Get selected sort value and update the display ---
            const value = this.getAttribute("data-value");
            document.getElementById("currentSort").textContent = value;
        });
    });

    // === Handle Live Search & Filtering ===
    const searchInput = document.querySelector("#searchInput");

    // --- Listen for user typing in the search bar ---
    searchInput.addEventListener("input", function () {
        // === Prepare and clean the search term ===
        const searchTerm = searchInput.value
            .toLowerCase()
            .replace(/[^\w\s]/g, "")  // Remove punctuation and symbols
            .trim();

        const container = document.querySelector(".news-listings");
        const cards = Array.from(container.querySelectorAll(".news-card"));

        // --- Helper function to clean text ---
        const cleanText = (text) => text.replace(/[^\w\s]/g, "").trim();

        // === Collect data from each card ===
        const cardData = cards.map((card) => {
            const titleEl = card.querySelector(".card-title");
            const pointsEl = card.querySelector(".fw-bold");
            const commentsEl = card.querySelector(".tag-comments");

            const titleText = cleanText(titleEl.textContent.replace(/^\d+\.\s*/, ""));
            const originalTitleText = titleEl.textContent;
            const points = parseInt(pointsEl.textContent.trim()) || 0;
            const comments = parseInt(commentsEl.textContent.trim()) || 0;

            return {
                element: card,
                originalTitleText: originalTitleText,
                title: titleText,
                points: points,
                comments: comments,
            };
        });

        // === If input is empty, reset cards to original order ===
        if (searchTerm === "") {
            let sortedCardsByTitle = cardData.sort((a, b) => {
                const numA = parseInt(a.title.split(" ")[0]);
                const numB = parseInt(b.title.split(" ")[0]);
                return numA - numB;
            });

            // --- Hide all cards ---
            cards.forEach((card) => card.style.display = "none");

            // --- Reattach and show sorted cards in original order ---
            sortedCardsByTitle.forEach((item) => {
                item.element.style.display = "block";
                container.appendChild(item.element);
            });

            return;
        }

        // === Filter cards by whether their title includes the search term ===
        const filteredCards = cardData.filter((item) =>
            item.title.toLowerCase().includes(searchTerm)
        );

        // === Sort logic based on number of words in search term ===
        const searchWordCount = searchTerm.split(/\s+/).length;

        let sortedCards;
        if (searchWordCount > 5) {
            // --- Sort by number of comments if more than 5 words ---
            sortedCards = filteredCards.sort((a, b) => b.comments - a.comments);
        } else {
            // --- Sort by number of points if 5 or fewer words ---
            sortedCards = filteredCards.sort((a, b) => b.points - a.points);
        }

        // === Display the sorted and filtered cards ===
        cards.forEach((card) => card.style.display = "none");

        sortedCards.forEach((item) => {
            item.element.style.display = "block";
            container.appendChild(item.element);
        });
    });
});
