document.addEventListener('DOMContentLoaded', function () {
    fetch('data/player_ranking.json')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('ranking-body');
            data.forEach((player, index) => {
                const row = document.createElement('tr');
                // Fügt eine Klasse gemäß dem Rang des Spielers hinzu (rank-1, rank-2, rank-3 für das Podium)
                if (index < 3) {
                    row.classList.add(`rank-${index + 1}`);
                }

                // Rank
                const rankCell = document.createElement('td');
                rankCell.textContent = (index + 1).toString();
                row.appendChild(rankCell);

                // Spieler-Spalte mit Trikotnummer und Name
                const playerCell = document.createElement('td');
                playerCell.innerHTML =
                    `<span class="shirt-number">${player.shirt_number}</span> ${player.player_name}`;
                row.appendChild(playerCell);

                // Spiele
                const gamesCell = document.createElement('td');
                gamesCell.textContent = player.games_played;
                row.appendChild(gamesCell);

                // Minuten
                const minutesCell = document.createElement('td');
                minutesCell.textContent = player.total_minutes;
                row.appendChild(minutesCell);

                // Punkte pro 90 Minuten
                const pointsPer90Cell = document.createElement('td');
                pointsPer90Cell.textContent = player.points_per_90_minutes ? player.points_per_90_minutes.toFixed(2) : 'n/a';
                row.appendChild(pointsPer90Cell);

                // Punkte
                const pointsCell = document.createElement('td');
                pointsCell.textContent = player.total_points;
                row.appendChild(pointsCell);

                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Fehler beim Laden der Daten:', error));
});