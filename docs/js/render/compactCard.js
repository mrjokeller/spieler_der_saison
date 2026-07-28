export function renderCompactRanking(containerId, data, valueKey, limit = 5) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = "";

    data.slice(0, limit).forEach((entry, index) => {
        const rank = index + 1;
        const row = document.createElement("tr");
        row.className = rank <= 3 ? `rank-${rank}` : "";

        row.innerHTML = `
      <td>${rank}</td>
      <td class="td-player-compact">${entry.player_name}</td>
      <td>${entry[valueKey]}</td>
    `;

        container.appendChild(row);
    });
}