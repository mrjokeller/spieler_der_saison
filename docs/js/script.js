document.addEventListener('DOMContentLoaded', function () {
    // Standardmäßig die Gesamtplatzierung laden
    loadRankingData('total', 'player_ranking.json');

    // register tab-button-listener
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.style.display = 'none');

            // add active class to clicked tab
            button.classList.add('active');

            // show corresponding content
            const tabId = button.getAttribute('data-tab');
            console.log(tabId);
            document.getElementById(tabId).style.display = 'block';

            // load data for selected tab
            const jsonFiles = {
                total: 'player_ranking.json',
                community: 'player_ranking_community.json',
                riky: 'player_ranking_riky.json',
                sebastian: 'player_ranking_sebastian.json'
            };

            loadRankingData(tabId, jsonFiles[tabId]);
        });
    });
});

// load data and populate table
function loadRankingData(tabId, jsonFile) {
    fetch(`data/${jsonFile}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById(`ranking-body-${tabId}`);
            tableBody.innerHTML = '';

            data.forEach((player, index) => {
                const row = document.createElement('tr');
                if (index < 3) {
                    row.classList.add(`rank-${index + 1}`);
                }

                // Platz
                const rankCell = document.createElement('td');
                rankCell.textContent = (index + 1).toString();
                row.appendChild(rankCell);

                // Spieler
                const playerCell = document.createElement('td');
                playerCell.innerHTML = `<span class="shirt-number">${player.shirt_number}</span> ${player.player_name}`;
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
        .catch(error => console.error(`Fehler beim Laden der Daten für ${tabId}:`, error));
}