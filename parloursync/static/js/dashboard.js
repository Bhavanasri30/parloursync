/* dashboard.js - Interactions for Owner/Customer Dashboards, Sidebar, Filters, Modals */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Sidebar Toggle (Mobile and Tablet)
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('-translate-x-full');
            if (mainContent) {
                mainContent.classList.toggle('lg:pl-64');
            }
        });
    }

    // 2. Tab or Filter click state styling
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('bg-indigo-600', 'text-white'));
            btn.classList.add('bg-indigo-600', 'text-white');
        });
    });

    // 3. Customer Details Modal
    const modalTriggers = document.querySelectorAll('[data-customer-id]');
    const customerModal = document.getElementById('customer-modal');
    const closeModalButtons = document.querySelectorAll('.close-modal');

    if (customerModal) {
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', () => {
                // Fetch/extract data attributes from clicked item
                const id = trigger.getAttribute('data-customer-id');
                const name = trigger.getAttribute('data-customer-name');
                const email = trigger.getAttribute('data-customer-email');
                const phone = trigger.getAttribute('data-customer-phone');
                const bookings = trigger.getAttribute('data-customer-bookings') || '0';
                const lastVisit = trigger.getAttribute('data-customer-last-visit') || 'N/A';

                // Fill modal contents
                document.getElementById('modal-customer-name').innerText = name;
                document.getElementById('modal-customer-email').innerText = email;
                document.getElementById('modal-customer-phone').innerText = phone;
                document.getElementById('modal-customer-bookings').innerText = bookings;
                document.getElementById('modal-customer-last-visit').innerText = lastVisit;

                // Open modal
                customerModal.classList.remove('hidden');
                customerModal.classList.add('flex');
            });
        });

        // Close logic
        closeModalButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                customerModal.classList.add('hidden');
                customerModal.classList.remove('flex');
            });
        });

        // Close on clicking backdrop
        customerModal.addEventListener('click', (e) => {
            if (e.target === customerModal) {
                customerModal.classList.add('hidden');
                customerModal.classList.remove('flex');
            }
        });
    }

    // 4. Quick Actions Form submission confirmation
    const actionForms = document.querySelectorAll('.action-form');
    actionForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const confirmMsg = form.getAttribute('data-confirm-message') || 'Are you sure you want to perform this action?';
            if (!confirm(confirmMsg)) {
                e.preventDefault();
            }
        });
    });
});
