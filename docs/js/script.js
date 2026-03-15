document.addEventListener('DOMContentLoaded', function () {
    fetch('data/player_ranking.json')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('ranking-body');
            data.forEach((player, index) => {
                const row = document.createElement('tr');
                // inserts a class according to the rank of the player (rank-1, rank-2, rank-3 for the podium)
                if (index < 3) {
                    row.classList.add(`rank-${index + 1}`);
                } else if (index % 2 == 0) {
                    row.classList.add('rank-even');
                } else {
                    row.classList.add('rank-uneven');
                }
                // html insertion
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