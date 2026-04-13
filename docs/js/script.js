document.addEventListener('DOMContentLoaded', function () {
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

// Load data and populate table with expand functionality
function loadRankingData(tabId, jsonFile) {
    if ($.fn.DataTable.isDataTable(`#${tabId}-ranking`)) {
        return -1;
    }
    let table = new DataTable(`#${tabId}-ranking`, {
        paging: false,
        scrollY: 400,
        searching: false,
        ordering: true,
        responsive: true,
        autoWidth: true,
        data: [],
        columns: [
            {
                data: null, title: 'Rang', className: 'rank-cell', orderable: false, responsivePriority: 2, render: function (data, type, row, meta) {
                    return meta.row + 1;
                }
            },
            {
                data: null,
                title: 'Spieler',
                className: 'player-cell',
                width: '50%',
                orderable: false,
                responsivePriority: 3,
                render: function (data, type, row) {
                    if (type === 'display') {
                        return `<span class="shirt-number">${row.shirt_number}</span> ${row.player_name}`;
                    }
                    return `${row.shirt_number} ${row.player_name}`;
                }
            },
            { data: 'games_played', title: 'Spiele', className: 'games-cell' },
            { data: 'total_minutes', title: 'Minuten', className: 'minutes-cell' },
            {
                data: 'points_per_90_minutes', title: 'Punkte/90 Min', className: 'points-per-90-cell',
                render: function (data, type, row) {
                    return data !== null ? data !== 0 ? data.toFixed(2) : 0 : 0;
                }
            },
            { data: 'total_points', title: 'Punkte', className: 'points-cell', responsivePriority: 1 }
        ],
        rowCallback: function (row, data) {
            if (data.rank <= 3) {
                row.classList.add(`rank-${data.rank}`);
            }
        }
    });

    fetch(`data/${jsonFile}`)
        .then(response => response.json())
        .then(data => {
            data.forEach((player, index) => {
                player.rank = index + 1;
            });

            table.clear();
            table.rows.add(data).draw();
        })
        .catch(error => {
            console.error(`Fehler beim Laden der Daten für ${tabId}:`, error);
            table.clear().draw();
        });
}