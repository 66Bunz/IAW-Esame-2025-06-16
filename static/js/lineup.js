document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchArtist');
    const clearButton = document.getElementById('clearSearch');
    const genreFilter = document.getElementById('genreFilter');
    const stageFilter = document.getElementById('stageFilter');
    const resetFiltersBtn = document.getElementById('resetFilters');
    const noResultsMessage = document.getElementById('noResultsMessage');
    const performanceItems = document.querySelectorAll('.performance-item');

    const urlParams = new URLSearchParams(window.location.search);
    const dayParam = urlParams.get('day');
    const stageParam = urlParams.get('stage');
    const genreParam = urlParams.get('genre');

    function applyUrlParams() {
        if (stageParam) {
            stageFilter.value = stageParam;
        }
        
        if (genreParam) {
            genreFilter.value = genreParam;
        }
        
        if (dayParam) {
            // Attiva il tab corrispondente al giorno
            const tabToActivate = document.getElementById(`day-${dayParam}-tab`);
            if (tabToActivate) {
                const tab = new bootstrap.Tab(tabToActivate);
                tab.show();
            }
        }
        
        // Applica i filtri
        if (stageParam || genreParam) {
            filterPerformances();
        }
    }

    function updatePerformanceCounts() {
        const dayTabs = document.querySelectorAll('.tab-pane');

        dayTabs.forEach(tab => {
            const dayId = tab.id.split('-')[1];
            const visiblePerformances = tab.querySelectorAll('.performance-item:not([style*="display: none"])').length;
            const countBadge = document.querySelector(`.performance-count[data-day="${dayId}"]`);

            if (countBadge) {
                countBadge.textContent = visiblePerformances;
            }
            tab.querySelectorAll('.stage-container').forEach(stage => {
                const visibleInStage = stage.querySelectorAll('.performance-item:not([style*="display: none"])').length;
                const noPerformanceMsg = stage.querySelector('.no-performance-message');

                if (noPerformanceMsg) {
                    if (visibleInStage === 0) {
                        noPerformanceMsg.style.display = 'block';
                    } else {
                        noPerformanceMsg.style.display = 'none';
                    }
                }
            });
        });

        const totalVisible = document.querySelectorAll('.performance-item:not([style*="display: none"])').length;
        if (totalVisible === 0) {
            noResultsMessage.style.display = 'block';
        } else {
            noResultsMessage.style.display = 'none';
        }
    }

    function filterPerformances() {
        const searchText = searchInput.value.toLowerCase();
        const genreValue = genreFilter.value;
        const stageValue = stageFilter.value;

        performanceItems.forEach(item => {
            const artistName = item.getAttribute('data-artist');
            const genreId = item.getAttribute('data-genre');
            const stageId = item.getAttribute('data-stage');

            const matchesSearch = artistName.includes(searchText);
            const matchesGenre = genreValue === '' || genreId === genreValue;
            const matchesStage = stageValue === '' || stageId === stageValue;

            if (matchesSearch && matchesGenre && matchesStage) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });

        updatePerformanceCounts();
    }

    searchInput.addEventListener('input', filterPerformances);
    genreFilter.addEventListener('change', filterPerformances);
    stageFilter.addEventListener('change', filterPerformances);

    clearButton.addEventListener('click', function () {
        searchInput.value = '';
        filterPerformances();
    });

    resetFiltersBtn.addEventListener('click', function () {
        searchInput.value = '';
        genreFilter.value = '';
        stageFilter.value = '';
        filterPerformances();
    });

    applyUrlParams();
});