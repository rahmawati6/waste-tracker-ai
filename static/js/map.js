function readMapBins() {
    const node = document.getElementById("map-bins");
    if (!node) return [];
    try {
        return JSON.parse(node.textContent);
    } catch (_error) {
        return [];
    }
}

function routeMarkerColor(status) {
    return {
        "kosong": "#27ae60",
        "sedang": "#f1c40f",
        "hampir penuh": "#f6a623",
        "penuh": "#e74c3c",
    }[status] || "#27ae60";
}

function routeIcon(status) {
    return L.divIcon({
        className: "smart-marker",
        html: `<span style="background:${routeMarkerColor(status)}"></span>`,
        iconSize: [20, 20],
        iconAnchor: [10, 10],
    });
}

const routeBins = readMapBins();
const routeMapNode = document.getElementById("routeMap");

if (routeMapNode) {
    const map = L.map("routeMap").setView([-6.2, 106.816666], 12);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap",
    }).addTo(map);

    routeBins.forEach((bin) => {
        L.marker([bin.latitude, bin.longitude], { icon: routeIcon(bin.status) })
            .addTo(map)
            .bindPopup(`
                <strong>${bin.kode_bin}</strong><br>
                ${bin.nama_lokasi}<br>
                ${bin.alamat}<br>
                Status: ${bin.status}<br>
                Isi: ${bin.persentase_isi}%
            `);
    });

    if (routeBins.length) {
        map.fitBounds(routeBins.map((bin) => [bin.latitude, bin.longitude]), { padding: [34, 34] });
    }
}
