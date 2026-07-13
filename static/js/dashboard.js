function parseJsonScript(id, fallback) {
    const node = document.getElementById(id);
    if (!node) return fallback;
    try {
        return JSON.parse(node.textContent);
    } catch (_error) {
        return fallback;
    }
}

const dashboardBins = parseJsonScript("dashboard-bins", []);
const statusCounts = parseJsonScript("status-counts", {});
const chartSeries = parseJsonScript("chart-series", []);

const palette = {
    kosong: "#4CAF50",
    sedang: "#FFC107",
    "hampir penuh": "#FF9800",
    penuh: "#E53935",
};

function markerColor(status) {
    return palette[status] || palette.kosong;
}

function makeIcon(status) {
    return L.divIcon({
        className: "smart-marker",
        html: `<span style="background:${markerColor(status)}"></span>`,
        iconSize: [22, 22],
        iconAnchor: [11, 11],
    });
}

let dashboardMap;
if (document.getElementById("dashboardMap")) {
    dashboardMap = L.map("dashboardMap", { scrollWheelZoom: false }).setView([-6.2, 106.816666], 12);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap",
    }).addTo(dashboardMap);

    dashboardBins.forEach((bin) => {
        L.marker([bin.latitude, bin.longitude], { icon: makeIcon(bin.status) })
            .addTo(dashboardMap)
            .bindPopup(`
                <div class="map-popup">
                    <strong>${bin.kode_bin}</strong>
                    <span>${bin.nama_lokasi}</span>
                    <small>${bin.status} - ${bin.persentase_isi}%</small>
                </div>
            `);
    });

    if (dashboardBins.length) {
        const bounds = dashboardBins.map((bin) => [bin.latitude, bin.longitude]);
        dashboardMap.fitBounds(bounds, { padding: [32, 32] });
    }
}

document.getElementById("refreshMap")?.addEventListener("click", () => {
    dashboardMap?.invalidateSize();
});

document.getElementById("mapFullscreen")?.addEventListener("click", async () => {
    const mapBox = document.getElementById("dashboardMap");
    if (mapBox && !document.fullscreenElement) {
        await mapBox.requestFullscreen();
        setTimeout(() => dashboardMap?.invalidateSize(), 250);
    }
});

function renderSparkline(id, data, color) {
    const node = document.querySelector(id);
    if (!node) return;
    new ApexCharts(node, {
        chart: { type: "area", height: 64, sparkline: { enabled: true }, toolbar: { show: false } },
        series: [{ data }],
        stroke: { curve: "smooth", width: 2 },
        colors: [color],
        fill: { type: "gradient", gradient: { opacityFrom: 0.36, opacityTo: 0 } },
        tooltip: { enabled: false },
    }).render();
}

renderSparkline("#sparkBins", [2, 3, 3, 4, 4, 5, 5], "#4CAF50");
renderSparkline("#sparkFill", [38, 42, 45, 49, 52, 58, 61], "#29B6F6");
renderSparkline("#sparkWaste", [98, 120, 112, 141, 136, 166, 175], "#FFC107");
renderSparkline("#sparkAlert", [1, 2, 1, 3, 2, 4, 2], "#E53935");

const statusNode = document.querySelector("#statusChart");
if (statusNode) {
    const labels = ["kosong", "sedang", "hampir penuh", "penuh"];
    new ApexCharts(statusNode, {
        chart: { type: "donut", height: 330, toolbar: { show: false } },
        labels,
        series: labels.map((label) => statusCounts[label] || 0),
        colors: labels.map((label) => palette[label]),
        legend: { position: "bottom", fontFamily: "Inter" },
        dataLabels: { enabled: true, formatter: (value) => `${value.toFixed(0)}%` },
        plotOptions: { pie: { donut: { size: "68%" } } },
        stroke: { width: 0 },
    }).render();
}

let wasteChart;
const wasteRanges = {
    day: chartSeries.map((item) => item.total),
    week: [612, 690, 725, 768, 742, 810, 846],
    month: [2380, 2560, 2490, 2750, 2890, 3010, 3180],
};

function renderWasteChart(range = "day") {
    const node = document.querySelector("#wasteChart");
    if (!node) return;
    if (wasteChart) wasteChart.destroy();
    wasteChart = new ApexCharts(node, {
        chart: { type: "area", height: 330, toolbar: { show: false } },
        series: [{ name: "Sampah", data: wasteRanges[range] }],
        xaxis: { categories: chartSeries.map((item) => item.tanggal), labels: { style: { fontFamily: "Inter" } } },
        yaxis: { labels: { formatter: (value) => `${value} kg` } },
        stroke: { curve: "smooth", width: 3 },
        colors: ["#2E7D32"],
        fill: { type: "gradient", gradient: { opacityFrom: 0.28, opacityTo: 0.02 } },
        grid: { borderColor: "rgba(148, 163, 184, 0.18)" },
        tooltip: { theme: document.body.classList.contains("dark-mode") ? "dark" : "light" },
    });
    wasteChart.render();
}

renderWasteChart();

document.querySelectorAll("#wasteRange button").forEach((button) => {
    button.addEventListener("click", () => {
        document.querySelectorAll("#wasteRange button").forEach((item) => item.classList.remove("active"));
        button.classList.add("active");
        renderWasteChart(button.dataset.range);
    });
});

const aiGaugeNode = document.querySelector("#aiGauge");
if (aiGaugeNode) {
    const filledBins = dashboardBins.filter((bin) => ["hampir penuh", "penuh"].includes(bin.status)).length;
    const confidence = Math.min(96, Math.max(72, 78 + filledBins * 6));
    new ApexCharts(aiGaugeNode, {
        chart: { type: "radialBar", height: 270, toolbar: { show: false } },
        series: [confidence],
        labels: ["Confidence"],
        colors: ["#4CAF50"],
        plotOptions: {
            radialBar: {
                startAngle: -120,
                endAngle: 120,
                hollow: { size: "58%" },
                dataLabels: {
                    value: { fontSize: "34px", fontWeight: 800, formatter: (value) => `${Math.round(value)}%` },
                    name: { fontSize: "13px", color: "#6D7C84" },
                },
            },
        },
    }).render();
}

async function loadWeather() {
    const temp = document.getElementById("weatherTemp");
    const meta = document.getElementById("weatherMeta");
    if (!temp || !meta) return;
    try {
        const response = await fetch("https://api.open-meteo.com/v1/forecast?latitude=-6.2&longitude=106.816666&current=temperature_2m,relative_humidity_2m,wind_speed_10m");
        const data = await response.json();
        temp.textContent = `${Math.round(data.current.temperature_2m)} C`;
        meta.textContent = `Kelembaban ${data.current.relative_humidity_2m}% | Angin ${data.current.wind_speed_10m} km/jam`;
    } catch (_error) {
        temp.textContent = "32 C";
        meta.textContent = "Data fallback Jakarta | Cuaca cerah berawan";
    }
}

loadWeather();
