document.addEventListener('DOMContentLoaded', function () {
    populateTimeline();
});

function populateTimeline() {
    fetch("data/historie.json")
        .then(response => response.json())
        .then(data => {
            const timeline = document.getElementById('history-timeline');
            timeline.innerHTML = '';

            data.forEach(item => {
                const timelineItem = document.createElement('div');
                timelineItem.className = 'timeline-item';

                const season = document.createElement('div');
                season.className = 'timeline-season';
                season.textContent = item.season;

                const playerCard = document.createElement('div');
                playerCard.className = 'player-card';

                const avatar = document.createElement('div');
                avatar.className = 'player-number';
                avatar.textContent = `#${item.shirt_number}`;

                const playerInfo = document.createElement('div');
                playerInfo.className = 'player-info';

                const name = document.createElement('div');
                name.className = 'player-name';
                name.textContent = item.player_name;

                const points = document.createElement('div');
                points.className = 'player-points';
                if (item.total_points !== null && item.total_points !== undefined) {
                    points.textContent = `${item.total_points} Punkte`;
                } else {
                    points.innerHTML = '<span class="no-data">Ohne Punkte</span>';
                }

                playerInfo.appendChild(name);
                playerInfo.appendChild(points);

                playerCard.appendChild(avatar);
                playerCard.appendChild(playerInfo);

                timelineItem.appendChild(season);
                timelineItem.appendChild(playerCard);

                timeline.appendChild(timelineItem);
            });
        })
        .catch(error => console.error(`Fehler beim Laden der Daten für ${tabId}:`, error));
}