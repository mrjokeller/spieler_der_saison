const RANKING_FILES = {
    total: "total_ranking.json",
    community: "community_ranking.json",
    riky: "riky_ranking.json",
    sebastian: "sebastian_ranking.json",
};

export const state = {
    activeTab: "total",
    rankingFiles: RANKING_FILES,
};

export function setActiveTab(tab) {
    state.activeTab = tab;
}