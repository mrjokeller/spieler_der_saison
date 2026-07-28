function medalClass(rank) {
    if (rank === 1) return "rank-1";
    if (rank === 2) return "rank-2";
    if (rank === 3) return "rank-3";
    return "";
}

export function renderRankingTable(container, players) {
    container.innerHTML = "";

    players.forEach((player, index) => {
        const rank = index + 1;
        const row = document.createElement("tr");
        row.className = medalClass(rank);

        row.innerHTML = `
      <td class="td-rank">${rank}</td>
      <td class="td-player">
        <span class="shirt-number">#${player.shirt_number}</span>
        ${player.player_name}
      </td>
      <td class="td-points">${player.total_points}</td>
    `;

        container.appendChild(row);
    });
}