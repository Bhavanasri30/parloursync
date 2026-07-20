/* calendar.js - Visual Appointment Calendar picker & availability helper */

document.addEventListener('DOMContentLoaded', () => {
    const timeInput = document.getElementById('appointment_time');
    if (!timeInput) return; // Only run on pages with appointment_time input

    // Create container for our luxury visual picker
    const container = document.createElement('div');
    container.className = 'mt-4 border border-slate-100 rounded-2xl p-4 bg-slate-50 shadow-inner space-y-4';
    
    // Header for the calendar picker
    const header = document.createElement('div');
    header.className = 'flex items-center justify-between border-b border-slate-200 pb-2';
    
    const title = document.createElement('h3');
    title.className = 'font-semibold text-sm text-slate-800 flex items-center gap-2';
    title.innerHTML = '<i data-lucide="calendar" class="w-4 h-4 text-indigo-600"></i> Premium Date & Time Picker';
    
    header.appendChild(title);
    container.appendChild(header);

    // Grid of dates
    const gridContainer = document.createElement('div');
    gridContainer.className = 'grid grid-cols-7 gap-1.5 text-center text-xs';
    
    // Add day names headers
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    days.forEach(day => {
        const dayHeader = document.createElement('div');
        dayHeader.className = 'font-semibold text-slate-500 py-1';
        dayHeader.innerText = day;
        gridContainer.appendChild(dayHeader);
    });

    // Populate current and next 14 days
    const today = new Date();
    const selectedDate = {
        date: today,
        time: "09:00"
    };

    const dateButtons = [];

    for (let i = 0; i < 14; i++) {
        const date = new Date();
        date.setDate(today.getDate() + i);
        
        // Pad days at start of grid if necessary to align days
        if (i === 0) {
            const startDay = date.getDay();
            for (let d = 0; d < startDay; d++) {
                const emptyCell = document.createElement('div');
                gridContainer.appendChild(emptyCell);
            }
        }

        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'py-2 rounded-lg font-medium border border-slate-200/60 bg-white hover:border-indigo-600 hover:bg-indigo-50/50 transition flex flex-col items-center justify-center';
        
        const dateNum = document.createElement('span');
        dateNum.className = 'text-sm font-bold text-slate-800';
        dateNum.innerText = date.getDate();
        
        const monthLabel = document.createElement('span');
        monthLabel.className = 'text-[9px] uppercase tracking-wider text-slate-400';
        monthLabel.innerText = date.toLocaleDateString('en-US', { month: 'short' });

        btn.appendChild(dateNum);
        btn.appendChild(monthLabel);

        // Highlight today initially
        if (i === 0) {
            btn.classList.add('border-indigo-600', 'bg-indigo-50/50', 'ring-2', 'ring-indigo-600/20');
        }

        btn.addEventListener('click', () => {
            dateButtons.forEach(b => b.classList.remove('border-indigo-600', 'bg-indigo-50/50', 'ring-2', 'ring-indigo-600/20'));
            btn.classList.add('border-indigo-600', 'bg-indigo-50/50', 'ring-2', 'ring-indigo-600/20');
            selectedDate.date = date;
            updateTimeInputValue();
        });

        dateButtons.push(btn);
        gridContainer.appendChild(btn);
    }

    container.appendChild(gridContainer);

    // Time Slot Selector
    const timeSlotsHeader = document.createElement('div');
    timeSlotsHeader.className = 'pt-2 border-t border-slate-200';
    timeSlotsHeader.innerHTML = '<p class="text-xs font-semibold text-slate-500 mb-2">Available Daily Slots</p>';
    container.appendChild(timeSlotsHeader);

    const slotsGrid = document.createElement('div');
    slotsGrid.className = 'grid grid-cols-4 gap-2';
    
    const slots = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'];
    const slotButtons = [];

    slots.forEach((time, index) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'py-1.5 rounded-lg text-xs font-medium border border-slate-200 bg-white hover:border-indigo-600 hover:bg-indigo-50/50 transition';
        btn.innerText = time;

        if (index === 0) {
            btn.classList.add('border-indigo-600', 'bg-indigo-50/50');
        }

        btn.addEventListener('click', () => {
            slotButtons.forEach(b => b.classList.remove('border-indigo-600', 'bg-indigo-50/50'));
            btn.classList.add('border-indigo-600', 'bg-indigo-50/50');
            selectedDate.time = time;
            updateTimeInputValue();
        });

        slotButtons.push(btn);
        slotsGrid.appendChild(btn);
    });

    container.appendChild(slotsGrid);

    // Insert visual calendar right below the timeInput label
    timeInput.parentNode.insertBefore(container, timeInput);
    
    // Hide standard browser input but keep it for form submit
    timeInput.style.display = 'none';

    function updateTimeInputValue() {
        const year = selectedDate.date.getFullYear();
        const month = String(selectedDate.date.getMonth() + 1).padStart(2, '0');
        const day = String(selectedDate.date.getDate()).padStart(2, '0');
        const formatted = `${year}-${month}-${day}T${selectedDate.time}`;
        timeInput.value = formatted;
    }

    // Trigger initial set
    updateTimeInputValue();

    // Re-trigger Lucide Icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});
