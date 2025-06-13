document.addEventListener('DOMContentLoaded', function () {
    
    function filterPublishedPerformances() {
        const searchText = document.getElementById('searchPublished').value.toLowerCase();
        const dayFilter = document.getElementById('filterPublishedDay').value;
        const stageFilter = document.getElementById('filterPublishedStage').value;

        const rows = document.querySelectorAll('#publishedTable tbody tr');

        rows.forEach(row => {
            const artistText = row.getAttribute('data-artist');
            const dayValue = row.getAttribute('data-day');
            const stageValue = row.getAttribute('data-stage');

            const matchesSearch = artistText.includes(searchText);
            const matchesDay = dayFilter === '' || dayValue === dayFilter;
            const matchesStage = stageFilter === '' || stageValue === stageFilter;

            if (matchesSearch && matchesDay && matchesStage) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    function filterDraftPerformances() {
        const searchText = document.getElementById('searchDraft').value.toLowerCase();
        const dayFilter = document.getElementById('filterDraftDay').value;
        const stageFilter = document.getElementById('filterDraftStage').value;

        const rows = document.querySelectorAll('#draftTable tbody tr');

        rows.forEach(row => {
            if (!row.hasAttribute('data-artist')) return;

            const artistText = row.getAttribute('data-artist');
            const dayValue = row.getAttribute('data-day');
            const stageValue = row.getAttribute('data-stage');

            const matchesSearch = artistText.includes(searchText);
            const matchesDay = dayFilter === '' || dayValue === dayFilter;
            const matchesStage = stageFilter === '' || stageValue === stageFilter;

            if (matchesSearch && matchesDay && matchesStage) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    function sortPublishedPerformances() {
        const sortOption = document.getElementById('sortPublished').value;
        const tbody = document.querySelector('#publishedTable tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));

        rows.sort((a, b) => {
            if (sortOption === 'day_asc') {
                return parseInt(a.getAttribute('data-day')) - parseInt(b.getAttribute('data-day'));
            } else if (sortOption === 'day_desc') {
                return parseInt(b.getAttribute('data-day')) - parseInt(a.getAttribute('data-day'));
            } else if (sortOption === 'artist_asc') {
                return a.getAttribute('data-artist').localeCompare(b.getAttribute('data-artist'));
            } else if (sortOption === 'artist_desc') {
                return b.getAttribute('data-artist').localeCompare(a.getAttribute('data-artist'));
            } else if (sortOption === 'time_asc' || sortOption === 'time_desc') {
                const timeA = a.querySelector('td:nth-child(4)').textContent;
                const timeB = b.querySelector('td:nth-child(4)').textContent;
                return sortOption === 'time_asc' ?
                    timeA.localeCompare(timeB) :
                    timeB.localeCompare(timeA);
            }
            return 0;
        });

        while (tbody.firstChild) {
            tbody.removeChild(tbody.firstChild);
        }

        rows.forEach(row => {
            tbody.appendChild(row);
        });
    }

    function sortDraftPerformances() {
        const sortOption = document.getElementById('sortDraft').value;
        const tbody = document.querySelector('#draftTable tbody');
        const rows = Array.from(tbody.querySelectorAll('tr[data-artist]'));

        if (rows.length === 0) return;

        rows.sort((a, b) => {
            if (sortOption === 'day_asc') {
                return parseInt(a.getAttribute('data-day')) - parseInt(b.getAttribute('data-day'));
            } else if (sortOption === 'day_desc') {
                return parseInt(b.getAttribute('data-day')) - parseInt(a.getAttribute('data-day'));
            } else if (sortOption === 'artist_asc') {
                return a.getAttribute('data-artist').localeCompare(b.getAttribute('data-artist'));
            } else if (sortOption === 'artist_desc') {
                return b.getAttribute('data-artist').localeCompare(a.getAttribute('data-artist'));
            } else if (sortOption === 'created_asc' || sortOption === 'created_desc') {
                const dateA = a.getAttribute('data-created');
                const dateB = b.getAttribute('data-created');
                return sortOption === 'created_asc' ?
                    dateA.localeCompare(dateB) :
                    dateB.localeCompare(dateA);
            }
            return 0;
        });

        const noDataRow = Array.from(tbody.querySelectorAll('tr:not([data-artist])'));
        while (tbody.firstChild) {
            tbody.removeChild(tbody.firstChild);
        }

        rows.forEach(row => {
            tbody.appendChild(row);
        });

        if (noDataRow.length > 0 && rows.length === 0) {
            tbody.appendChild(noDataRow[0]);
        }
    }

    document.getElementById('searchPublished').addEventListener('input', filterPublishedPerformances);
    document.getElementById('filterPublishedDay').addEventListener('change', filterPublishedPerformances);
    document.getElementById('filterPublishedStage').addEventListener('change', filterPublishedPerformances);
    document.getElementById('sortPublished').addEventListener('change', sortPublishedPerformances);

    document.getElementById('searchDraft').addEventListener('input', filterDraftPerformances);
    document.getElementById('filterDraftDay').addEventListener('change', filterDraftPerformances);
    document.getElementById('filterDraftStage').addEventListener('change', filterDraftPerformances);
    document.getElementById('sortDraft').addEventListener('change', sortDraftPerformances);
});