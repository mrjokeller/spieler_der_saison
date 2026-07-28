const DATA_PATH = "data/";
const cache = new Map();

export async function fetchJSON(filename) {
    if (cache.has(filename)) return cache.get(filename);

    const response = await fetch(`${DATA_PATH}${filename}`);
    if (!response.ok) {
        throw new Error(`Fehler beim Laden von ${filename}: ${response.status}`);
    }

    const data = await response.json();
    cache.set(filename, data);
    return data;
}