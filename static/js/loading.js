const SmartWasteLoading = (() => {
    const screen = document.getElementById("loadingScreen");
    const progress = document.getElementById("loadingProgressBar");
    const percent = document.getElementById("loadingPercent");
    const status = document.getElementById("loadingStatus");
    const motivation = document.getElementById("loadingMotivation");
    const progressShell = document.querySelector(".loading-progress");

    const statuses = [
        "Loading Dashboard...",
        "Connecting Database...",
        "Loading AI Model...",
        "Preparing Maps...",
        "Initializing Smart Sensors...",
        "Almost Ready...",
    ];

    const motivations = [
        "Creating Cleaner Cities...",
        "Analyzing Waste...",
        "Optimizing Collection Routes...",
        "Preparing AI Detection...",
        "Smart City Ready...",
        "Making Environment Better...",
    ];

    const checkpoints = [0, 15, 30, 45, 60, 75, 90, 100];
    let current = 0;
    let intervalId;

    function setProgress(value) {
        current = Math.min(100, Math.max(current, value));
        if (progress) progress.style.width = `${current}%`;
        if (percent) percent.textContent = `${Math.round(current)}%`;
        progressShell?.setAttribute("aria-valuenow", String(Math.round(current)));
    }

    function start() {
        if (!screen) return;
        document.documentElement.classList.add("is-loading");
        setProgress(0);
        let index = 0;
        intervalId = setInterval(() => {
            index = Math.min(index + 1, checkpoints.length - 1);
            setProgress(checkpoints[index]);
            if (status) status.textContent = statuses[index % statuses.length];
            if (motivation) motivation.textContent = motivations[index % motivations.length];
            if (index >= checkpoints.length - 1) clearInterval(intervalId);
        }, 210);
    }

    function hide() {
        if (!screen) return;
        clearInterval(intervalId);
        setProgress(100);
        if (status) status.textContent = "Smart City Ready...";
        setTimeout(() => {
            screen.classList.add("hidden");
            document.documentElement.classList.remove("is-loading");
            document.body.classList.add("page-ready");
            clearSkeletons();
        }, 380);
    }

    function showForLogin() {
        if (!screen) return;
        screen.classList.remove("hidden");
        document.documentElement.classList.add("is-loading");
        document.body.classList.remove("page-ready");
        if (status) status.textContent = "Signing In...";
        if (motivation) motivation.textContent = "Preparing your command center...";
        setProgress(15);
    }

    function clearSkeletons() {
        document.querySelectorAll(".skeleton-loading").forEach((node) => {
            node.classList.remove("skeleton-loading");
        });
    }

    function primeSkeletons() {
        document.querySelectorAll(".stat-card, #statusChart, #wasteChart, #aiGauge, .map-box, .map-page, .table").forEach((node) => {
            node.classList.add("skeleton-loading");
        });
    }

    function buttonText(button) {
        if (button.dataset.loadingText) return button.dataset.loadingText;
        const label = button.textContent.toLowerCase();
        if (label.includes("login")) return "Signing In...";
        if (label.includes("prediksi")) return "Predicting...";
        if (label.includes("upload")) return "Uploading...";
        if (label.includes("export")) return "Processing...";
        if (label.includes("hapus")) return "Processing...";
        if (label.includes("update") || label.includes("ubah")) return "Saving...";
        if (label.includes("simpan") || label.includes("tambah")) return "Saving...";
        return "Processing...";
    }

    function attachButtonLoading() {
        document.querySelectorAll("form").forEach((form) => {
            form.addEventListener("submit", () => {
                const button = form.querySelector("button[type='submit']");
                if (!button || button.dataset.loadingActive === "true") return;
                button.dataset.loadingActive = "true";
                button.dataset.originalHtml = button.innerHTML;
                button.disabled = true;
                button.classList.add("button-loading");
                button.innerHTML = `<span class="button-spinner" aria-hidden="true"></span>${buttonText(button)}`;
                form.classList.add("form-processing");
                if (document.body.classList.contains("login-page")) {
                    showForLogin();
                }
            });
        });
    }

    function attachUploadProgress() {
        document.querySelectorAll("input[type='file']").forEach((input) => {
            const form = input.closest("form");
            if (!form || form.querySelector(".upload-progress")) return;
            const progressBox = document.createElement("div");
            progressBox.className = "upload-progress";
            progressBox.innerHTML = `<span></span><strong>0%</strong>`;
            input.insertAdjacentElement("afterend", progressBox);

            input.addEventListener("change", () => {
                if (!input.files?.length) return;
                progressBox.classList.add("show");
                progressBox.querySelector("span").style.width = "35%";
                progressBox.querySelector("strong").textContent = "35%";
            });

            form.addEventListener("submit", () => {
                progressBox.classList.add("show", "complete");
                progressBox.querySelector("span").style.width = "100%";
                progressBox.querySelector("strong").textContent = "100%";
            });
        });
    }

    function init() {
        start();
        primeSkeletons();
        attachButtonLoading();
        attachUploadProgress();
        window.addEventListener("load", () => {
            const elapsedBuffer = 1150;
            setTimeout(hide, elapsedBuffer);
        });
    }

    return { init, hide, showForLogin };
})();

SmartWasteLoading.init();
