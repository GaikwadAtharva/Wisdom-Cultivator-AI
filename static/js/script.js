document.addEventListener("DOMContentLoaded", () => {

    const textarea = document.querySelector("textarea");
    const messages = document.querySelector(".chat-messages");
    const form = document.querySelector(".chat-input-area");
    const button = form ? form.querySelector("button") : null;
    const searchBox = document.getElementById("searchReflections");
    const menuBtn = document.getElementById("mobileMenuBtn");
    const sidebar = document.querySelector(".journal-sidebar");

    if (messages) {
        messages.scrollTop = messages.scrollHeight;
    }

    if (textarea) {
        textarea.focus();

        function resizeTextarea() {
            textarea.style.height = "auto";
            textarea.style.height = textarea.scrollHeight + "px";
        }

        resizeTextarea();

        textarea.addEventListener("input", resizeTextarea);

        form.addEventListener("submit", (e) => {

            if (textarea.value.trim() === "") {
                e.preventDefault();
                textarea.focus();
                return;
            }

            if (button) {
                button.innerText = "Reflecting...";
                button.disabled = true;
            }

        });

        textarea.addEventListener("keydown", function (e) {

            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                form.requestSubmit();
            }

        });
    }

    if (searchBox) {
        searchBox.addEventListener("input", () => {

            const searchText = searchBox.value.toLowerCase();
            const rows = document.querySelectorAll(".journal-row");

            rows.forEach(row => {
                const title = row.innerText.toLowerCase();

                row.style.display = title.includes(searchText) ? "flex" : "none";
            });

        });
    }

    if (menuBtn && sidebar) {

        menuBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            sidebar.classList.toggle("show");
        });

        sidebar.addEventListener("click", (e) => {
            e.stopPropagation();
        });

        document.addEventListener("click", () => {
            sidebar.classList.remove("show");
        });
    }

});