document.addEventListener("DOMContentLoaded", function () {
    // Sort by date or name
    document.querySelectorAll(".sort-option").forEach((item) => {
        item.addEventListener("click", function (e) {
            e.preventDefault();
            const value = this.getAttribute("data-value");
            document.getElementById("currentSort").textContent = value;
        });
    });

    // on change of the search input
    const searchInput = document.querySelector("#searchInput");

    // track input event
    searchInput.addEventListener("input", function () {
        // Clean the search term: remove non-word characters and trim spaces
        const searchTerm = searchInput.value
            .toLowerCase()
            .replace(/[^\w\s]/g, "")  // Remove symbols and punctuation
            .trim();

        const container = document.querySelector(".news-listings");
        const cards = Array.from(container.querySelectorAll(".news-card"));

        const cleanText = (text) => text.replace(/[^\w\s]/g, "").trim(); // Remove symbols from titles

        // Extract card data (title, points, comments, etc.)
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

        // If the search input is empty, reset all cards to their original state
        if (searchTerm === "") {
            let sortedCardsByTitle = cardData.sort((a, b) => {
                const numA = parseInt(a.title.split(" ")[0]);
                const numB = parseInt(b.title.split(" ")[0]);
            
                return numA - numB;
            });

            // Hide all cards first
            cards.forEach((card) => card.style.display = "none");

            // Show only the matching and sorted cards
            sortedCardsByTitle.forEach((item) => {
                item.element.style.display = "block";
                container.appendChild(item.element);  // Reattach them to reorder
            });

            return; 
        }

        // Filter cards based on whether the title contains the search term
        const filteredCards = cardData.filter((item) =>
            item.title.toLowerCase().includes(searchTerm)
        );

        // Separate and sort based on word count condition of the search term
        let sortedCards;
        const searchWordCount = searchTerm.split(/\s+/).length;  // Count words in the searchTerm
        if (searchWordCount > 5) {
            sortedCards = filteredCards.sort((a, b) => b.comments - a.comments);
        } else {
            sortedCards = filteredCards.sort((a, b) => b.points - a.points);
        }

        // Hide all cards first
        cards.forEach((card) => card.style.display = "none");

        // Show only the matching and sorted cards
        sortedCards.forEach((item) => {
            item.element.style.display = "block";
            container.appendChild(item.element);  // Reattach them to reorder
        });
    });
});
