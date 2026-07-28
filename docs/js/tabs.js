import { state, setActiveTab } from "./state.js";
import { fetchJSON } from "./api.js";
import { renderRankingTable } from "./render/rankingTable.js";

export function initTabs(onTabChange) {
    const buttons = document.querySelectorAll(".tab-button");
    const tableBody = document.getElementById("ranking-body-total");

    async function loadTab(tab) {
        setActiveTab(tab);
        buttons.forEach((btn) => btn.classList.toggle("active", btn.dataset.tab === tab));

        const filename = state.rankingFiles[tab];
        const data = await fetchJSON(filename);
        renderRankingTable(tableBody, data);
    }

    buttons.forEach((btn) => {
        btn.addEventListener("click", () => loadTab(btn.dataset.tab));
    });

    loadTab(state.activeTab);
}