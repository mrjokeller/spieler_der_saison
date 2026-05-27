document.addEventListener('DOMContentLoaded', function () {
    // Standardmäßig die Gesamtplatzierung laden
    loadRankingData('total', 'player_ranking.json');
    loadRankingData('community', 'player_ranking_community.json');
    loadRankingData('riky', 'player_ranking_riky.json');
    loadRankingData('sebastian', 'player_ranking_sebastian.json');
    loadCompactRankingData('defense', 'defense_ranking.json');
    loadCompactRankingData('midfield', 'midfield_ranking.json');
    loadCompactRankingData('attack', 'attack_ranking.json');
    loadCompactRankingData('home', 'home_ranking.json');
    loadCompactRankingData('away', 'away_ranking.json');
    loadCompactRankingData('bundesliga', 'bundesliga_ranking.json');
    loadCompactRankingData('euroleague', 'euroleague_ranking.json');
    loadCompactRankingData('dfbpokal', 'dfbpokal_ranking.json');
    loadCompactRankingData('votes', 'votes_ranking.json');
    loadCompactRankingData('highestwin', 'most_points_in_game_ranking.json');
    loadCompactRankingData('streak', 'longest_streak_ranking.json');

    // load data for selected tab
    const jsonFiles = {
        total: 'player_ranking.json',
        community: 'player_ranking_community.json',
        riky: 'player_ranking_riky.json',
        sebastian: 'player_ranking_sebastian.json'
    };

    addTabButtonFunction('total-ranking', jsonFiles);
});

function addTabButtonFunction(htmlClass, jsonFiles) {
    // register tab-button-listener
    document.querySelectorAll(`.tab-button.${htmlClass}`).forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll(`.tab-button.${htmlClass}`).forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll(`.tab-content.${htmlClass}`).forEach(content => content.style.display = 'none');

            // add active class to clicked tab
            button.classList.add('active');

            // show corresponding content
            const tabId = button.getAttribute('data-tab');
            console.log(tabId);
            document.getElementById(tabId).style.display = 'block';

            loadRankingData(tabId, jsonFiles[tabId]);
        });
    });
}

// Load data and populate table with expand functionality
function loadRankingData(tabId, jsonFile) {
    fetch(`data/${jsonFile}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById(`ranking-body-${tabId}`);
            const expandButton = document.getElementById(`expand-button-${tabId}`);
            tableBody.innerHTML = '';

            // Show only first 10 players initially
            const initialRows = Math.min(10, data.length);
            let isExpanded = false;

            function renderTable(limit = initialRows) {
                tableBody.innerHTML = '';
                const rowsToShow = limit === 'all' ? data.length : limit;

                for (let i = 0; i < rowsToShow; i++) {
                    const row = document.createElement('tr');
                    const player = data[i];

                    if (i < 3) {
                        row.classList.add(`rank-${i + 1}`);
                    }

                    // Platz
                    const rankCell = document.createElement('td');
                    rankCell.classList.add('td-rank');
                    rankCell.textContent = (i + 1).toString();
                    row.appendChild(rankCell);

                    // Spieler
                    const playerCell = document.createElement('td');
                    playerCell.classList.add('td-player');
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
                    pointsCell.classList.add('td-points');
                    pointsCell.textContent = player.total_points;
                    row.appendChild(pointsCell);

                    tableBody.appendChild(row);
                }

                // Button text anpassen
                if (rowsToShow === data.length) {
                    expandButton.textContent = 'Weniger ▲';
                } else if (data.length <= 10) {
                    expandButton.display = 'none';
                } else {
                    expandButton.textContent = 'Mehr ▼';
                }
            }

            // Initial nur 10 Zeilen anzeigen
            renderTable(initialRows);

            // Button-Klick-Event
            expandButton.onclick = function () {
                isExpanded = !isExpanded;
                if (isExpanded) {
                    renderTable('all');
                } else {
                    renderTable(initialRows);
                }
            };
        })
        .catch(error => console.error(`Fehler beim Laden der Daten für ${tabId}:`, error));
}

function loadCompactRankingData(tabId, jsonFile) {
    fetch(`data/${jsonFile}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById(`compact-ranking-card-body-${tabId}`);
            tableBody.innerHTML = '';
            const rowsToShow = 3;

            for (let i = 0; i < rowsToShow; i++) {
                const row = document.createElement('tr');
                const player = data[i];

                if (i < 3) {
                    row.classList.add(`rank-${i + 1}`);
                }

                // Platz
                const rankCell = document.createElement('td');
                rankCell.classList.add('td-rank-compact');
                rankCell.textContent = (i + 1).toString();
                row.appendChild(rankCell);

                // Spieler
                const playerCell = document.createElement('td');
                playerCell.classList.add('td-player-compact');
                playerCell.innerHTML = player.player_name;
                row.appendChild(playerCell);

                // Punkte
                const pointsCell = document.createElement('td');
                pointsCell.classList.add('td-points-compact');
                if (jsonFile === "votes_ranking.json") {
                    pointsCell.textContent = player.total_votes;
                } else if (jsonFile === "longest_streak_ranking.json") {
                    pointsCell.textContent = player.longest_streak;
                } else {
                    pointsCell.textContent = player.total_points;
                }
                row.appendChild(pointsCell);

                tableBody.appendChild(row);
            }
        })
        .catch(error => console.error(`Fehler beim Laden der Daten für ${tabId}:`, error));
}