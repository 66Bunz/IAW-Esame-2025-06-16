document.addEventListener('DOMContentLoaded', function () {
    const ticketTypeInputs = document.querySelectorAll('input[name="ticket_type_id"]');
    const daySelectionContainer = document.getElementById('daySelectionContainer');
    const singleDaySelection = document.getElementById('singleDaySelection');
    const twoDaySelection = document.getElementById('twoDaySelection');
    const fullPassSelection = document.getElementById('fullPassSelection');
    const ticketSummary = document.getElementById('ticketSummary');
    const summaryTicketType = document.getElementById('summaryTicketType');
    const summaryDays = document.getElementById('summaryDays');
    const summaryPrice = document.getElementById('summaryPrice');
    const buyButton = document.getElementById('buyButton');
    const ticketForm = document.getElementById('ticketForm');

    function updateSummary() {
        let selectedDays = [];
        let daysText = "";
        
        const selectedTicketTypeInput = document.querySelector('input[name="ticket_type_id"]:checked');
        
        if (selectedTicketTypeInput) {
            const selectedTypeId = parseInt(selectedTicketTypeInput.value);
            const selectedType = ticketTypesData[selectedTypeId];

            if (selectedType.daysCount === 1) {
                const selectedDay = document.querySelector('input[name="days"]:checked');
                if (selectedDay) {
                    const dayId = parseInt(selectedDay.value);
                    selectedDays.push(dayId);
                    daysText = eventDays[dayId] ? eventDays[dayId].name : "Giorno " + dayId;
                }
            } else if (selectedType.daysCount === 2) {
                const selectedPair = document.querySelector('input[name="days_pair"]:checked');
                if (selectedPair) {
                    const dayIds = selectedPair.value.split(',').map(Number);
                    selectedDays = dayIds;
                    daysText = (eventDays[dayIds[0]] ? eventDays[dayIds[0]].name : "Giorno " + dayIds[0]) + 
                               " + " + 
                               (eventDays[dayIds[1]] ? eventDays[dayIds[1]].name : "Giorno " + dayIds[1]);
                }
            } else if (selectedType.daysCount === 3) {
                selectedDays = [1, 2, 3];
                daysText = "Venerdì + Sabato + Domenica";

                if (fridayFull || saturdayFull || sundayFull) {
                    buyButton.disabled = true;
                    return;
                }
            }
        }

        if (selectedDays.length > 0) {
            ticketSummary.style.display = "block";
            const selectedTicketTypeInput = document.querySelector('input[name="ticket_type_id"]:checked');
            const selectedTypeId = parseInt(selectedTicketTypeInput.value);
            summaryTicketType.textContent = ticketTypesData[selectedTypeId].name;
            summaryDays.textContent = daysText;
            summaryPrice.textContent = parseFloat(ticketTypesData[selectedTypeId].price).toFixed(2);

            buyButton.disabled = false;

            const selectedType = ticketTypesData[selectedTypeId];
            
            if (selectedType.daysCount === 1) {
            } else if (selectedType.daysCount === 2 || selectedType.daysCount === 3) {
                document.querySelectorAll('input[name="days"]').forEach(input => {
                    if (input.type === 'hidden') input.remove();
                });

                selectedDays.forEach(dayId => {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'days';
                    input.value = dayId;
                    ticketForm.appendChild(input);
                });
            }
        } else {
            ticketSummary.style.display = "none";
            buyButton.disabled = true;
        }
    }

    ticketTypeInputs.forEach(input => {
        input.addEventListener('change', function() {
            const selectedTypeId = parseInt(this.value);
            const selectedType = ticketTypesData[selectedTypeId];
            
            daySelectionContainer.style.display = "block";
            
            singleDaySelection.style.display = selectedType.daysCount === 1 ? "block" : "none";
            twoDaySelection.style.display = selectedType.daysCount === 2 ? "block" : "none";
            fullPassSelection.style.display = selectedType.daysCount === 3 ? "block" : "none";

            document.querySelectorAll('input[name="days"]:checked, input[name="days_pair"]:checked').forEach(input => {
                input.checked = false;
            });
                        
            updateSummary();
        });
    });

    document.querySelectorAll('input[name="days"]').forEach(input => {
        input.addEventListener('change', updateSummary);
    });

    document.querySelectorAll('input[name="days_pair"]').forEach(input => {
        input.addEventListener('change', updateSummary);
    });
});
