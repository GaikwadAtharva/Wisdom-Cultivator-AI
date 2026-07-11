document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".chat-input-area");
    const textarea = form
        ? form.querySelector('textarea[name="message"]')
        : null;

    const messages = document.querySelector(".chat-messages");
    const button = form ? form.querySelector('button[type="submit"]') : null;
    const searchBox = document.getElementById("searchReflections");
    const menuBtn = document.getElementById("mobileMenuBtn");
    const sidebar = document.querySelector(".journal-sidebar");

    if (messages) {
        messages.scrollTop = messages.scrollHeight;
    }

    if (form && textarea) {

        textarea.focus();

        function resizeTextarea() {
            textarea.style.height = "auto";
            textarea.style.height = `${textarea.scrollHeight}px`;
        }

        resizeTextarea();

        textarea.addEventListener("input", resizeTextarea);

        form.addEventListener("submit", (event) => {

            const message = textarea.value.trim();

            if (message === "") {
                event.preventDefault();
                textarea.focus();
                return;
            }

            if (button) {
                button.textContent = "Reflecting...";
                button.disabled = true;
            }
        });

        textarea.addEventListener("keydown", (event) => {

            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();

                if (typeof form.requestSubmit === "function") {
                    form.requestSubmit();
                } else if (button) {
                    button.click();
                }
            }
        });
    }

    if (searchBox) {

        searchBox.addEventListener("input", () => {

            const searchText = searchBox.value
                .trim()
                .toLowerCase();

            const rows = document.querySelectorAll(".journal-row");

            rows.forEach((row) => {
                const title = row.innerText.toLowerCase();

                row.style.display = title.includes(searchText)
                    ? "flex"
                    : "none";
            });
        });
    }

    if (menuBtn && sidebar) {

        menuBtn.addEventListener("click", (event) => {
            event.stopPropagation();
            sidebar.classList.toggle("show");
        });

        sidebar.addEventListener("click", (event) => {
            event.stopPropagation();
        });

        document.addEventListener("click", () => {
            sidebar.classList.remove("show");
        });
    }
});