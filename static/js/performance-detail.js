document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('featuredCheck').addEventListener('change', function () {
        document.getElementById('featuredInput').value = this.checked ? '1' : '0';
    });
});