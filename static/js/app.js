const sidebar = document.getElementById("sidebar");
const toggle = document.getElementById("sidebarToggle");
const themeToggle = document.getElementById("themeToggle");
const fullscreenToggle = document.getElementById("fullscreenToggle");
const notificationMenu = document.getElementById("notificationMenu");
const notificationToggle = document.getElementById("notificationToggle");

toggle?.addEventListener("click", () => {
    sidebar?.classList.toggle("open");
});

function applyTheme(theme) {
    document.body.classList.toggle("dark-mode", theme === "dark");
    const icon = themeToggle?.querySelector("i");
    if (icon) {
        icon.className = theme === "dark" ? "bi bi-sun" : "bi bi-moon-stars";
    }
}

const savedTheme = localStorage.getItem("smartwaste-theme") || "light";
applyTheme(savedTheme);

themeToggle?.addEventListener("click", () => {
    const nextTheme = document.body.classList.contains("dark-mode") ? "light" : "dark";
    localStorage.setItem("smartwaste-theme", nextTheme);
    applyTheme(nextTheme);
});

fullscreenToggle?.addEventListener("click", async () => {
    if (!document.fullscreenElement) {
        await document.documentElement.requestFullscreen();
    } else {
        await document.exitFullscreen();
    }
});

notificationToggle?.addEventListener("click", (event) => {
    event.stopPropagation();
    notificationMenu?.classList.toggle("open");
    notificationToggle.setAttribute("aria-expanded", notificationMenu?.classList.contains("open") ? "true" : "false");
});

document.addEventListener("click", (event) => {
    if (!notificationMenu?.contains(event.target)) {
        notificationMenu?.classList.remove("open");
        notificationToggle?.setAttribute("aria-expanded", "false");
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        notificationMenu?.classList.remove("open");
        notificationToggle?.setAttribute("aria-expanded", "false");
    }
});

function updateClock() {
    const now = new Date();
    const clock = document.getElementById("liveClock");
    const date = document.getElementById("liveDate");
    if (clock) {
        clock.textContent = now.toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" });
    }
    if (date) {
        date.textContent = now.toLocaleDateString("id-ID", { weekday: "short", day: "2-digit", month: "short" });
    }
}

updateClock();
setInterval(updateClock, 1000);

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".toast").forEach((toast) => {
        new bootstrap.Toast(toast, { delay: 4200 }).show();
    });

    AOS?.init({
        duration: 550,
        easing: "ease-out-cubic",
        once: true,
    });
});

function tableToCsv(table) {
    return [...table.querySelectorAll("tr")]
        .map((row) => [...row.children].map((cell) => `"${cell.innerText.replaceAll('"', '""').trim()}"`).join(","))
        .join("\n");
}

function enhanceTables() {
    document.querySelectorAll(".table").forEach((table, index) => {
        if (table.dataset.enhanced) return;
        table.dataset.enhanced = "true";

        const wrapper = document.createElement("div");
        wrapper.className = "table-toolbar";
        wrapper.innerHTML = `
            <label class="search-box">
                <i class="bi bi-search"></i>
                <input type="search" placeholder="Cari di tabel...">
            </label>
            <div class="d-flex align-items-center gap-2">
                <span class="table-count"></span>
                <button class="btn btn-outline-success btn-sm" type="button"><i class="bi bi-download"></i> Export</button>
            </div>
        `;
        table.parentElement?.insertBefore(wrapper, table);

        const input = wrapper.querySelector("input");
        const count = wrapper.querySelector(".table-count");
        const rows = [...table.querySelectorAll("tbody tr")];

        function applyFilter() {
            const keyword = input.value.toLowerCase();
            let visible = 0;
            rows.forEach((row) => {
                const match = row.innerText.toLowerCase().includes(keyword);
                row.style.display = match ? "" : "none";
                if (match) visible += 1;
            });
            count.textContent = `${visible} data`;
        }

        input.addEventListener("input", applyFilter);
        wrapper.querySelector("button")?.addEventListener("click", () => {
            const blob = new Blob([tableToCsv(table)], { type: "text/csv;charset=utf-8" });
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = `smartwaste-table-${index + 1}.csv`;
            link.click();
            URL.revokeObjectURL(url);
        });
        applyFilter();
    });
}

enhanceTables();
