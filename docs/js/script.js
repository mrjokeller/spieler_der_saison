document.addEventListener('DOMContentLoaded', function () {
    fetch('../../data/player_ranking.json')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('ranking-body');
            data.forEach((player, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
            <td>${index + 1}</td>
            <td>${player.player_name}</td>
            <td>${player.shirt_number}</td>
            <td>${player.total_points}</td>
            `;
                tableBody.appendChild(row);
            });
        });
});