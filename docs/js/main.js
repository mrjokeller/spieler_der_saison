import { initTabs } from "./tabs.js";
import { initMobileMenu } from "./mobileMenu.js";
import { fetchJSON } from "./api.js";
import { renderCompactRanking } from "./render/compactCard.js";

async function initCompactRankings() {
    const [home, away, bl, el, dfb, votes, highest, streak] = await Promise.all([
        fetchJSON("home_ranking.json"),
        fetchJSON("away_ranking.json"),
        fetchJSON("bundesliga_ranking.json"),
        fetchJSON("euroleague_ranking.json"),
        fetchJSON("dfbpokal_ranking.json"),
        fetchJSON("votes_ranking.json"),
        fetchJSON("most_points_in_game_ranking.json"),
        fetchJSON("longest_streak_ranking.json"),
    ]);

    renderCompactRanking("compact-ranking-card-body-home", home, "total_points");
    renderCompactRanking("compact-ranking-card-body-away", away, "total_points");
    renderCompactRanking("compact-ranking-card-body-bundesliga", bl, "total_points");
    renderCompactRanking("compact-ranking-card-body-euroleague", el, "total_points");
    renderCompactRanking("compact-ranking-card-body-dfbpokal", dfb, "total_points");
    renderCompactRanking("compact-ranking-card-body-votes", votes, "total_votes");
    renderCompactRanking("compact-ranking-card-body-highestwin", highest, "game_points");
    renderCompactRanking("compact-ranking-card-body-streak", streak, "longest_streak");
}

document.addEventListener("DOMContentLoaded", () => {
    initMobileMenu();
    initTabs();
    initCompactRankings();
});